

create table GOVUK_raw (jobID int, labelText nvarchar(max), resultText nvarchar(max), Website nvarchar(max));

select * from GOVUK_raw;

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
