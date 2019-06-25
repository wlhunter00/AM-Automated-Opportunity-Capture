select * from NYSCR_raw order by jobid;

update NYSCR_raw set labelText = 'Due Date:' where labelText like '%Due%';
update NYSCR_raw set labelText = 'Due Date:' where labelText like '%End%';
update NYSCR_raw set labelText = 'Company:' where labelText like '%Agency%';

select jobID, resultText, right(labelText,36) from NYSCR_raw;

truncate table NYSCR_raw;

select distinct labelText from NYSCR_raw;

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

select * from NYSCR_pvt;



select max(jobID) from NYSCR_raw;

select * from NYSCR_raw;