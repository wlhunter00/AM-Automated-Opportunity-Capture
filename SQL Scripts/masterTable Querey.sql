truncate table master_table;

select * from master_table;

-- Moving from individual pivot tables to Master Table
insert into master_table(JobDescription, Website, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category)
select [Title:], [Website], cast([Due Date:] as datetime), cast(replace(replace( [Issue Date:], char(10), ''), char(13), '') as date),cast([dateInserted:] as datetime), [Type:], [URL:], [Location:], [Classification:] from DASNY_pvt;

insert into master_table(JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category)
select [Title:], [Website], [Company:], cast([Due Date:] as datetime), cast([Issue Date:] as datetime), cast([dateInserted:] as datetime), [Ad Type:], [URL:], [Location:], [Category:] from NYSCR_pvt;


select * from current_table;

truncate table current_table;


-- Moving from Main Table to Current Table
delete from current_table where DueDate < getdate();
update current_table set Status = 'Old';
INSERT INTO current_table (JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, Status)
SELECT JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category, 'New'
FROM master_table
WHERE NOT EXISTS (Select JobID, JobDescription From current_table WHERE current_table.JobDescription = master_table.JobDescription)
and master_table.DueDate > GETDATE();
