drop table master_table;

create table current_table(JobID int primary key identity(1,1), JobDescription nvarchar(450) unique not null, Website nvarchar(max) not null, Company nvarchar(max), DueDate date, IssueDate date, InsertDate date, RequestType nvarchar(max), JobURL nvarchar(max), JobLocation nvarchar(max), Category nvarchar(max));

truncate table master_table;

select * from master_table order by DueDate;

insert into master_table(JobDescription, Website, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category)
select [Title:], [Website], cast([Due Date:] as datetime), cast(replace(replace( [Issue Date:], char(10), ''), char(13), '') as date),cast([dateInserted:] as datetime), [Type:], [URL:], [Location:], [Classification:] from DASNY_pvt;

insert into master_table(JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category)
select [Title:], [Website], [Company:], cast([Due Date:] as datetime), cast([Issue Date:] as datetime), cast([dateInserted:] as datetime), [Ad Type:], [URL:], [Location:], [Category:] from NYSCR_pvt;

select * from master_table where DueDate > GETDATE();

insert into current_table(JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category)
select JobDescription, Website, Company, DueDate, IssueDate, InsertDate, RequestType, JobURL, JobLocation, Category from master_table where DueDate > GETDATE();