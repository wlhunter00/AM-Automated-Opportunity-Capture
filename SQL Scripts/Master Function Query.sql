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

insert into master_table(JobDescription, Website, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category)
select [Title:], [Website], cast([Due Date:] as datetime), cast(replace(replace( [Issue Date:], char(10), ''), char(13), '') as date),cast([dateInserted:] as datetime), [Type:], [URL:], [Location:], [Classification:]
from DASNY_pvt
WHERE DASNY_pvt.[Title:] not in(select JobDescription from master_table);

insert into master_table(JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category)
select [Title:], [Website], [Company:], cast([Due Date:] as datetime), cast([Issue Date:] as datetime), cast([dateInserted:] as datetime), [Ad Type:], [URL:], [Location:], [Category:]
from NYSCR_pvt
WHERE NYSCR_pvt.[Title:] not in(select JobDescription from master_table);

insert into master_table(JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, LongDescription, MaxValue)
select [Title:], [Website], [Company:], cast([Closing date] as datetime), cast([Publication date] as datetime), cast([dateInserted:] as datetime), [Notice Type], [URL:], [Contract location], [Description:], [Contract value (high)]
from GOVUK_pvt
WHERE GOVUK_pvt.[Title:] not in(select JobDescription from master_table);


insert into master_table(JobDescription, Website, DueDate, InsertDate, RequestType, JobURL, JobLocation, LongDescription, Category)
select [Title:], [Website], cast([endDate] as datetime), cast([dateInserted:] as datetime), 'RFP', [URL:], [Location], [description], [Categories]
from RFPDB_pvt
WHERE RFPDB_pvt.[Title:] not in(select JobDescription from master_table);


delete from current_table where DueDate < getdate();
update current_table set Status = 'Old';

delete from master_table where jobID not in(
select max(jobID) from master_table group by JobDescription);

INSERT INTO current_table (JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, Status, masterJobId)
SELECT distinct JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, 'New', master_table.JobID
FROM master_table
WHERE master_table.JobDescription not in(select JobDescription from current_table) and master_table.DueDate > GETDATE();

select * from current_table order by jobID;
