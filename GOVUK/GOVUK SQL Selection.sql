select * from DASNY_raw;

update DASNY_raw set resultText = substring(resultText, 0, CHARINDEX('-', resultText)) where labelText like '%Due%';

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

select * from DASNY_pvt;

truncate table DASNY_raw;



update DASNY_pvt set [Due Date:] = replace([Due Date:], '/', '-') from DASNY_pvt;
update DASNY_pvt set [Issue Date:] = replace([Issue Date:], '/', '-') from DASNY_pvt;

select convert(varchar(max),cast([Issue Date:] as datetime),101) from DASNY_pvt;

select try_convert(date, ltrim(rtrim([Issue Date:]))), [Issue Date:] from DASNY_pvt;

select try_convert(datetime, [Due Date:])from DASNY_pvt;

select try_convert(datetime, '06/11/2019 ')from DASNY_pvt;

select [Issue Date:], [Due Date:] from DASNY_pvt;


Select convert(varchar(max),cast(replace(replace( [Issue Date:], char(10), ''), char(13), '') as date),101) from DASNY_PVT;

update NYSCR_raw set resultText = replace(replace( resultText, char(10), ''), char(13), '');