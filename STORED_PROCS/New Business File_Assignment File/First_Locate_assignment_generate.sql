use rm
go 

create procedure dbo.FIRST_LOCATE_assignment_generate
as

DROP TABLE RM_FILES.dbo.JUST_ASS_TEMP 
SELECT ACC.ClientReference
		, ASS.ASSIGNMENTID					AS [Auxiliary Reference]
		, ASS.Segment			
		, NB.SALUTATION	[Salutation]
		, NB.FIRSTNAME						AS [First Name]
		, NB.[Surname]
		, NB.CUSTOMERNAME					AS [Full Name]
		, nb.dateofbirth								AS [Date of Birth]
		, NB.MAILINGADDRESSLINE1			AS [Mailing Address Line 1]
		, NB.MAILINGADDRESSLINE2			AS [Mailing Address Line 2]
		, NB.MAILINGADDRESSLINE3			AS [Mailing Address Line 3]
		, NB.MAILINGADDRESSLINE4			AS [Mailing Address Line 4]
		, NB.MAILINGADDRESSLINE5			AS [Mailing Address Line 5]
		, NB.MAILINGADDRESSPOSTCODE			AS [Mailing Address Post code]
		, NB.SUPPLYADDRESSLINE1 			AS [Supply Address Line 1]
		, NB.SUPPLYADDRESSLINE2				AS [Supply Address Line 2]
		, NB.SUPPLYADDRESSLINE3				AS [Supply Address Line 3]
		, NB.SUPPLYADDRESSLINE4				AS [Supply Address Line 4]
		, NB.SUPPLYADDRESSLINE5				AS [Supply Address Line 5]
		, NB.SUPPLYADDRESSPOSTCODE			AS [Supply Address Post code]
		, NB.telephone1						AS [Telephone 1]
		, NB.telephone2						AS [Telephone 2]
		, NB.telephone3						AS [Telephone 3]
		, sup.[E-mail]
		, ass.assignedamount				as [Balance]
		, null								as 	[Interest]
		, [Last Payment Date]		 
		, [Last Payment Amount]
		, [Product Name]
		, [Supply Date From]
		, [Supply Date To]
INTO RM_FILES.dbo.JUST_ASS_TEMP 
FROM RM.DBO.ACCOUNT						ACC
JOIN RM.DBO.ASSIGNMENT					ASS		ON ASS.ACCOUNTID=ACC.ACCOUNTID
JOIN #InsertTable	NB		ON cast(cast(cast(nb.clientreference as float) as int) as nvarchar(50)) = ACC.CLIENTREFERENCE
join rm.dbo.supplementarydata		sup on 	sup.clientreference=acc.clientreference

WHERE CAST(RECEIVEDDATE AS DATE) = CAST(GETDATE() AS DATE)















