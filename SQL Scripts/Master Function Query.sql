truncate table NYSCR_pvt;

insert into NYSCR_pvt
SELECT jobID, Website, [Title:], [Company:], [Category:], [dateInserted:], [Due Date:], [Issue Date:], [Location:], [URL:], [Ad Type:] 
FROM    (   SELECT A.jobID, resultText,  labelText, Website
            FROM NYSCR_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Title:], [Company:], [Category:], [dateInserted:], [Due Date:], [Issue Date:], [Location:], [URL:], [Ad Type:])
        ) AS  PVT


truncate table DASNY_pvt;

insert into DASNY_pvt
SELECT jobID, Website, [Title:], [Solicitation #:], [Issue Date:], [Due Date:], [Classification:], [Location:], [Type:], [Goals (%):], [Status:], [dateInserted:], [URL:]
FROM    (   SELECT A.jobID, resultText,  labelText, Website
            FROM DASNY_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Title:], [Solicitation #:], [Issue Date:], [Due Date:], [Classification:], [Location:], [Type:], [Goals (%):], [Status:], [dateInserted:], [URL:])
        ) AS  PVT


truncate table GOVUK_pvt;

insert into GOVUK_pvt
SELECT jobID, Website, [Closing date], [Company:], [Contract location], [Contract value (high)], [Contract value (low)], [dateInserted:], [Notice status], [Notice type], [Publication date], [Title:], [URL:], [Description:]
FROM    (   SELECT A.jobID, resultText, labelText, Website
            FROM GOVUK_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Closing date], [Company:], [Contract location], [Contract value (high)], [Contract value (low)], [dateInserted:], [Notice status], [Notice type] , [Publication date], [Title:], [URL:], [Description:])
        ) AS  PVT


truncate table RFPDB_pvt;

insert into RFPDB_pvt
SELECT jobID, Website, [Categories], [dateInserted:], [description], [endDate], [Location], [Title:], [URL:]
FROM    (   SELECT A.jobID, resultText, labelText, Website
            FROM RFPDB_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Categories], [dateInserted:], [description], [endDate], [Location], [Title:], [URL:])
        ) AS  PVT


insert into master_table(JobDescription, Website, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, Expired)
select [Title:], [Website], cast([Due Date:] as datetime), cast(replace(replace( [Issue Date:], char(10), ''), char(13), '') as date),cast([dateInserted:] as datetime), [Type:], [URL:], [Location:], [Classification:], 'No'
from DASNY_pvt
WHERE DASNY_pvt.[Title:] not in(select JobDescription from master_table);

insert into master_table(JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, Expired)
select [Title:], [Website], [Company:], cast([Due Date:] as datetime), cast([Issue Date:] as datetime), cast([dateInserted:] as datetime), [Ad Type:], [URL:], [Location:], [Category:], 'No'
from NYSCR_pvt
WHERE NYSCR_pvt.[Title:] not in(select JobDescription from master_table);

insert into master_table(JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, LongDescription, MaxValue, Expired)
select [Title:], [Website], [Company:], cast([Closing date] as datetime), cast([Publication date] as datetime), cast([dateInserted:] as datetime), [Notice Type], [URL:], [Contract location], [Description:], [Contract value (high)], 'No'
from GOVUK_pvt
WHERE GOVUK_pvt.[Title:] not in(select JobDescription from master_table);

insert into master_table(JobDescription, Website, DueDate, InsertDate, RequestType, JobURL, JobLocation, LongDescription, Category, Expired)
select [Title:], [Website], cast([endDate] as datetime), cast([dateInserted:] as datetime), 'RFP', [URL:], [Location], [description], [Categories], 'No'
from RFPDB_pvt
WHERE RFPDB_pvt.[Title:] not in(select JobDescription from master_table);

update master_table set Expired = 'Yes' where DueDate < GETDATE();


delete from current_table where DueDate < getdate();
update current_table set Status = 'Old';

delete from master_table where jobID not in(
select max(jobID) from master_table group by JobDescription);

update master_table set jobDescription = substring(jobDescription, 0, 300) where len(jobDescription) > 300;

INSERT INTO current_table (JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, Status, masterJobId)
SELECT distinct JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, 'New', master_table.JobID
FROM master_table
WHERE master_table.JobDescription not in(select JobDescription from current_table) and master_table.DueDate > GETDATE();

truncate table NYSCR_raw;
truncate table DASNY_raw;
truncate table GOVUK_raw;
truncate table RFPDB_raw;

insert into event_master_table(Title, shortSummary, longSummary, URL, eventStart, eventEnd, publishDate, insertDate, status, onlineEvent, address, category, site, Expired)
select [Title], [shortSummary], [longSummary], [URL], [eventStart], [eventEnd], [publishDate], [insertDate], [status], [onlineEvent], [address], [category], 'eventBrite', 'No'
from eventBrite_raw
WHERE eventBrite_raw.[Title] not in(select Title from event_master_table);

truncate table eventBrite_raw;

update event_master_table set Expired = 'Yes' where eventEnd < GETDATE();

delete from event_current_table where eventEnd < getdate();
update event_current_table set recent = 'Old';

update event_master_table set shortSummary = substring(shortSummary, 0, 300) where len(shortSummary) > 300;

insert into event_current_table(title, shortSummary, URL, eventStart, eventEnd, publishDate, insertDate, address, category, site, recent, masterTableID)
select distinct Title, shortSummary, URL, eventStart, eventEnd, publishDate, insertDate, address, category, site, 'New', eventID
from event_master_table
WHERE event_master_table.Title not in(select Title from event_current_table) and event_master_table.eventEnd > GETDATE();

