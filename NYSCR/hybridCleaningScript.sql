select * from NYSCRhybrid order by jobid;

update NYSCRhybrid set labelText = 'Due Date:' where labelText like '%Due%';
update NYSCRhybrid set labelText = 'Due Date:' where labelText like '%End%';
update NYSCRhybrid set labelText = 'Company:' where labelText like '%Agency%';

select jobID, resultText, right(labelText,36) from NYSCRhybrid;

truncate table nyscrhybrid;

select distinct labelText from NYSCRhybrid;

SELECT jobID, Website, [Title:], [Company:], [Category:], [dateInserted:], [Due Date:], [Issue Date:], [Location:], [URL:], [Ad Type:] 
FROM    (   SELECT A.jobID, resultText,  labelText, Website
            FROM NYSCRhybrid A 
        ) AS P
        PIVOT 
        (   MAX(resultText) 
            FOR labeltext in ([Title:], [Company:], [Category:], [dateInserted:], [Due Date:], [Issue Date:], [Location:], [URL:], [Ad Type:])
        ) AS  PVT

select max(jobID) from NYSCRhybrid;

select * from NYSCRhybrid;