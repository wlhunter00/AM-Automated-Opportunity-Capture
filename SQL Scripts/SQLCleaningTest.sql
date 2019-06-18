select 
	REPLACE(REPLACE(REPLACE(BodyText,'<div class="labelText">','|'),'</div>','|'),'<div class="resultText">','')
from 
	NYSCRuncleaned



TRUNCATE TABLE NYSCRuncleaned







SELECT compatibility_level  
FROM sys.databases WHERE name = 'Opportunity Hunter';

SELECT JobID, value
from NYSCRuncleaned
	CROSS APPLY string_split(BodyText, ':');

SELECT RIGHT(BodyText, 6)   
FROM NYSCRuncleaned
ORDER BY JobID;  
GO 

select JobID, BodyText, CHARINDEX('Title:', BodyText) from NYSCRuncleaned;

--Going to need an if statement for issue date and end Date and location and category
--Going to need a way to trim begining and end of each statement IE how to cut out title and agency in a manner that works

 29   Title:Debt Management/Investments  Agency:Dormitory Authority of the State of New York Issue Date:06/17/2019                              Due Date:                            08/09/2019 Location:Albany Category:Miscellaneous - Consulting & Other Services Ad Type:General     Log in to view ad Register to view ad   URL:https://www.nyscr.ny.gov/adsOpen.cfm?startnum=1&orderBy=55&numPer=50&myAdsOnly=2&adClass=b&adCat=&adCounty=&adType=&mbe=0&wbe=0&dbe=0&keyword=
 32   Title:18260-Ithaca Arthaus   Company:Vecino Construction Issue Date:06/17/2019                              Due Date:                            07/19/2019 Location:Ithaca NY  Category:Construction Vertical: Building Construction; Rehabilitation & New Construction - Construction Ad Type:Contractor Ads     Log in to view ad Register to view ad   URL:https://www.nyscr.ny.gov/adsOpen.cfm?startnum=1&orderBy=55&numPer=50&myAdsOnly=2&adClass=b&adCat=&adCounty=&adType=&mbe=0&wbe=0&dbe=0&keyword=

select JobID, BodyText, 
CHARINDEX('Title:', BodyText) as StartNumber, 
CHARINDEX('Agency:', BodyText) as endNumber, 
(CHARINDEX('Agency:', BodyText)-CHARINDEX('Title:', BodyText)) as DifferenceNumber,
SUBSTRING(BodyText, CHARINDEX('Title:', BodyText), 10) as Title
--Trim('Agency:' from SUBSTRING(bodyText, CHARINDEX('Agency:', BodyText), CHARINDEX('Issue Date', BodyText))) as Agency,
--SUBSTRING(bodyText, CHARINDEX('Ad Type:', BodyText), CHARINDEX('Log', BodyText)) as AdType
from NYSCRuncleaned;

truncate table NYSCRclean1;

SET IDENTITY_INSERT NYSCRclean1 on;
INSERT INTO NYSCRclean1(JobID, BodyText, TitleNumber, AgencyNumber, CompanyNumber)
SELECT JobID, BodyText,
CHARINDEX('Title:', BodyText),
CHARINDEX('Agency:', BodyText),
CHARINDEX('Company:', BodyText)
from NYSCRuncleaned;
SET IDENTITY_INSERT NYSCRclean1 off;

Select * from NYSCRclean1;

