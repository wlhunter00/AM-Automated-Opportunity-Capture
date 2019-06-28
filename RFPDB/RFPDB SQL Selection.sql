create table RFPDB_raw (jobID int, labelText nvarchar(max), resultText nvarchar(max), Website nvarchar(max));

select * from RFPDB_raw;

select distinct ltrim(labelText) from RFPDB_raw;


SELECT jobID, Website, [Categories], [dateInserted:], [description], [endDate], [Location], [Title:], [URL:]
into RFPDB_pvt
FROM    (   SELECT A.jobID, resultText, labelText, Website
            FROM RFPDB_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Categories], [dateInserted:], [description], [endDate], [Location], [Title:], [URL:])
        ) AS  PVT

select * from RFPDB_pvt order by jobID;

insert into RFPDB_pvt
SELECT jobID, Website, [Categories], [dateInserted:], [description], [endDate], [Location], [Title:], [URL:]
FROM    (   SELECT A.jobID, resultText, labelText, Website
            FROM RFPDB_raw A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Categories], [dateInserted:], [description], [endDate], [Location], [Title:], [URL:])
        ) AS  PVT

update RFPDB_raw set resultText = substring(resultText,0, 11) where labelText = 'endDate';

truncate table rfpdb_pvt;
