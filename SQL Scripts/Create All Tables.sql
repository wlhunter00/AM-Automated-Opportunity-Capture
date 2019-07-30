CREATE TABLE [DASNY_pvt](
	[jobID] [int] NULL,
	[Website] [nvarchar](max) NULL,
	[Title:] [nvarchar](max) NULL,
	[Solicitation #:] [nvarchar](max) NULL,
	[Issue Date:] [nvarchar](max) NULL,
	[Due Date:] [nvarchar](max) NULL,
	[Classification:] [nvarchar](max) NULL,
	[Location:] [nvarchar](max) NULL,
	[Type:] [nvarchar](max) NULL,
	[Goals (%):] [nvarchar](max) NULL,
	[Status:] [nvarchar](max) NULL,
	[dateInserted:] [nvarchar](max) NULL,
	[URL:] [nvarchar](max) NULL
);

CREATE TABLE [DASNY_raw](
	[jobID] [int] NULL,
	[labelText] [nvarchar](max) NULL,
	[resultText] [nvarchar](max) NULL,
	[Website] [nvarchar](max) NULL
);

CREATE TABLE [event_current_table](
	[eventID] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](max) NULL,
	[shortSummary] [nvarchar](max) NULL,
	[URL] [nvarchar](max) NULL,
	[eventStart] [datetime] NULL,
	[eventEnd] [datetime] NULL,
	[publishDate] [datetime] NULL,
	[insertDate] [datetime] NULL,
	[address] [nvarchar](max) NULL,
	[category] [nvarchar](max) NULL,
	[site] [nvarchar](max) NULL,
	[recent] [nvarchar](max) NULL,
	[masterTableID] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[eventID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
);


CREATE TABLE [eventBrite_raw](
	[eventID] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](max) NULL,
	[shortSummary] [nvarchar](max) NULL,
	[longSummary] [nvarchar](max) NULL,
	[URL] [nvarchar](max) NULL,
	[eventStart] [datetime] NULL,
	[eventEnd] [datetime] NULL,
	[publishDate] [datetime] NULL,
	[insertDate] [datetime] NULL,
	[status] [nvarchar](max) NULL,
	[onlineEvent] [nvarchar](max) NULL,
	[address] [nvarchar](max) NULL,
	[category] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[eventID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
);

CREATE TABLE [GOVUK_pvt](
	[jobID] [int] NULL,
	[Website] [nvarchar](max) NULL,
	[Closing date] [nvarchar](max) NULL,
	[Company:] [nvarchar](max) NULL,
	[Contract location] [nvarchar](max) NULL,
	[Contract value (high)] [nvarchar](max) NULL,
	[Contract value (low)] [nvarchar](max) NULL,
	[dateInserted:] [nvarchar](max) NULL,
	[Notice status] [nvarchar](max) NULL,
	[Notice type] [nvarchar](max) NULL,
	[Publication date] [nvarchar](max) NULL,
	[Title:] [nvarchar](max) NULL,
	[URL:] [nvarchar](max) NULL,
	[Description:] [nvarchar](max) NULL
);

CREATE TABLE [GOVUK_raw](
	[jobID] [int] NULL,
	[labelText] [nvarchar](max) NULL,
	[resultText] [nvarchar](max) NULL,
	[Website] [nvarchar](max) NULL
);


CREATE TABLE [jobDescriptions_tbl](
	[pay] [int] NULL,
	[description] [nvarchar](max) NULL
);

CREATE TABLE [jobs_current_table](
	[JobID] [int] IDENTITY(1,1) NOT NULL,
	[JobDescription] [nvarchar](450) NOT NULL,
	[Website] [nvarchar](max) NOT NULL,
	[Company] [nvarchar](max) NULL,
	[DueDate] [date] NULL,
	[IssueDate] [date] NULL,
	[InsertDate] [date] NULL,
	[RequestType] [nvarchar](max) NULL,
	[JobURL] [nvarchar](max) NULL,
	[JobLocation] [nvarchar](max) NULL,
	[Category] [nvarchar](max) NULL,
	[Status] [nvarchar](max) NOT NULL,
	[masterJobId] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[JobID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[JobDescription] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
);

CREATE TABLE [jobs_master_table](
	[JobID] [int] IDENTITY(1,1) NOT NULL,
	[JobDescription] [nvarchar](max) NOT NULL,
	[Website] [nvarchar](max) NOT NULL,
	[Company] [nvarchar](max) NULL,
	[DueDate] [date] NULL,
	[IssueDate] [date] NULL,
	[InsertDate] [date] NULL,
	[RequestType] [nvarchar](max) NULL,
	[JobURL] [nvarchar](max) NULL,
	[JobLocation] [nvarchar](max) NULL,
	[Category] [nvarchar](max) NULL,
	[LongDescription] [nvarchar](max) NULL,
	[MaxValue] [nvarchar](max) NULL,
	[Expired] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[JobID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
);

CREATE TABLE [NYSCR_pvt](
	[jobID] [int] NULL,
	[Website] [nvarchar](max) NULL,
	[Title:] [nvarchar](max) NULL,
	[Company:] [nvarchar](max) NULL,
	[Category:] [nvarchar](max) NULL,
	[dateInserted:] [nvarchar](max) NULL,
	[Due Date:] [nvarchar](max) NULL,
	[Issue Date:] [nvarchar](max) NULL,
	[Location:] [nvarchar](max) NULL,
	[URL:] [nvarchar](max) NULL,
	[Ad Type:] [nvarchar](max) NULL
);


CREATE TABLE [NYSCR_raw](
	[jobID] [int] NULL,
	[labelText] [nvarchar](max) NULL,
	[resultText] [nvarchar](max) NULL,
	[Website] [nvarchar](max) NULL
);

CREATE TABLE [RFPDB_pvt](
	[jobID] [int] NULL,
	[Website] [nvarchar](max) NULL,
	[Categories] [nvarchar](max) NULL,
	[dateInserted:] [nvarchar](max) NULL,
	[description] [nvarchar](max) NULL,
	[endDate] [nvarchar](max) NULL,
	[Location] [nvarchar](max) NULL,
	[Title:] [nvarchar](max) NULL,
	[URL:] [nvarchar](max) NULL
);

CREATE TABLE [RFPDB_raw](
	[jobID] [int] NULL,
	[labelText] [nvarchar](max) NULL,
	[resultText] [nvarchar](max) NULL,
	[Website] [nvarchar](max) NULL
);

