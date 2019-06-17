IF OBJECT_ID('dbo.NYSCRuncleaned', 'U') IS NOT NULL
DROP TABLE dbo.NYSCRuncleaned
GO
-- Create the table in the specified schema
CREATE TABLE dbo.NYSCRuncleaned
(
   JobID        INT IDENTITY NOT NULL   PRIMARY KEY, -- primary key column
   BodyText      [NVARCHAR](MAX)  NOT NULL
);
GO