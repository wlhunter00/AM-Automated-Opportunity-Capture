

create table GOVUK_raw (jobID int, labelText nvarchar(max), resultText nvarchar(max), Website nvarchar(max));

select * from GOVUK_raw;

select distinct jobID from GOVUK_raw order by jobID desc;

select distinct ltrim(labelText) from GOVUK_raw;


SELECT jobID, Website, [Closing date], [Company:], [Contract location], [Contract value (high)], [Contract value (low)], [dateInserted:], [Notice status], [Notice type], [Publication date], [Title:], [URL:], [Description:]
into GOVUK_pvt
FROM    (   SELECT A.jobID, resultText, labelText, Website
            FROM GOVUK_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Closing date], [Company:], [Contract location], [Contract value (high)], [Contract value (low)], [dateInserted:], [Notice status], [Notice type] , [Publication date], [Title:], [URL:], [Description:])
        ) AS  PVT

select * from GOVUK_pvt order by jobID;

insert into GOVUK_pvt
SELECT jobID, Website, [Closing date], [Company:], [Contract location], [Contract value (high)], [Contract value (low)], [dateInserted:], [Notice status], [Notice type], [Publication date], [Title:], [URL:], [Description:]
FROM    (   SELECT A.jobID, resultText, labelText, Website
            FROM GOVUK_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Closing date], [Company:], [Contract location], [Contract value (high)], [Contract value (low)], [dateInserted:], [Notice status], [Notice type] , [Publication date], [Title:], [URL:], [Description:])
        ) AS  PVT


	select [closing date], substring([closing date], 2, 2) from GOVUK_pvt;
	select [closing date], substring([closing date], 5, 2) from GOVUK_pvt;
	select [closing date], substring([closing date], 8, 4) from GOVUK_pvt;

	select [closing date], substring([closing date], 5, 2) + '/' + substring([closing date], 2, 2) + '/' + substring([closing date], 8, 4) from GOVUK_pvt;

	update GOVUK_raw set [resultText] = substring([resultText], 5, 2) + '/' + substring([resultText], 2, 2) + '/' + substring([resultText], 8, 4) where [labelText] like '%Closing%' or [labelText] like '%Publication%';

	select * from current_table;