--==================================================================================================================================================================================================
--==================================================================================================================================================================================================
-- AJJB PLACEMENT FILE PROCESS
--==================================================================================================================================================================================================
USE RM
GO

--1) CREATE LIST OF ACCOUNTS THAT QUALIFY
--2) CREATE OUTPUT FILES FOR TU AND CREDITSAFE


--==================================================================================================================================================================================================
--==================================================================================================================================================================================================
CREATE PROCEDURE dbo.LIT_PLACEMENT_PROCESS_1
AS
--1) CREATE LIST OF ACCOUNTS THAT QUALIFY


SELECT			ACC.CLIENTREFERENCE
INTO			rm_files.[dbo].[LIT_TEMP_ORIGINAL]
FROM			RM.DBO.ACCOUNT			ACC
JOIN			RM.DBO.Assignment		ASS			ON ASS.ClientReference=ACC.ClientReference		AND ASS.DCA<>'AJJB'
LEFT JOIN		RM.DBO.Assignment		ASSL		ON ASSL.ClientReference=ACC.ClientReference		AND ASSL.DCA='AJJB'
WHERE			ASSL.ClientReference IS NULL								-- NOT PREVIOUSLY BEEN TO LITIGATION
AND				ACC.ClosureDate IS NULL										-- ACCOUNT HASNT BEEN CLOSED BACK TO THE CLIENT
AND				ACC.RecallDate IS NULL										-- ACCOUNT HASNT BEEN RECALLED BY THE CLIENT
AND				ASS.ClosureDate IS NOT NULL									-- ACCOUNT HAS BEEN CLOSED BY FIRST LOCATE
AND				ASS.ClosureReason IN ('EXH')								-- FIRST LOCATE CLOSED THE ACCOUNT AS EFFORTS EXHAUSTED
AND				ISNULL(ACC.OutstandingBalance,ACC.ORIGINALBALANCE) > 200	-- BALANCE IS GREATER THAN £200

--==================================================================================================================================================================================================
--2) CREATE OUTPUT FILES FOR TU AND CREDITSAFE

--TU
SELECT			AJJB.ClientReference ClientId
				,	'1'				as	Passive
				,	'0'				as	Duration
				,	'Y'				as	AddressLinks
				,	'E'				as	ProductType
				,	'Y'				as	LivingAsStated
				,	'Y'				as	CreditActive
				,	'Y'				as	SearchDeceased
				,	'Y'				as	SearchLandRegistry
				,	'Y'				as	SearchOccupancyStatus
				,	'N'				as	OccupierLookup
				,	''				as	ServiceStartDate
				,	''				as	ServiceEndDate
				,	'Y'				as	DataCleanseAddress
				,	'Y'				as	DataCleanseJointNames
				,	'Y'				as	SearchTelephone 
				,	'3'				as	TeleSources
				,	'P'				as	SearchP2PScore
				,	'Y'				as	SearchAccountTypes
				,	'Y'				as	SearchBAI
				,	'Y'				as	SearchJudgments
				,	'Y'				as	DOBMLookup
				,	'Y'				as	ReconciliationFile
				,	'Y'				as	SearchDataDNA
				,	'Y'				as	SearchCohabiting
				,	'Y'				as	TransiencyIndexAppend
				,	'7'				as	InTouchContact
				,	'Y'				as	InTouchRecency
				,	'7'				as	InTouchAdditional
				,	''			as	ValueAddedService
				,	''			as	InputDataDNA
				,	cUS.firstname + ' ' + cUS.surname    	as	Name
				,	''    		as	Title
				,	''    		as	Forename
				,	''    		as	Othername
				,	''    		as	Surname
				,	isnull(cUS.dateofbirth  ,'')  	as	DateOfBirth
				,	isnull(caM.addressline1 ,'')   	as	Address1
				,	isnull(caM.addressline2 ,'')   	as	Address2
				,	isnull(caM.addressline3	,'') as	Address3
				,	isnull(caM.addressline4 ,'')   	as	Address4
				,	isnull(caM.addressline5	,'') as	Address5
				,	''	    as	Address6
				,	''	    as	Address7
				,	isnull(caM.addresspostcode,'')    as	Postcode
				,	''    	as	StartDateAtAddress
				,	''    	as	EndDateAtAddress
				,	''		as	[P1_ Address1]
				,	''		as	[P1_ Address2]
				,	''		as	[P1_ Address3]
				,	''		as	[P1_ Address4]
				,	''		as	[P1_ Address5]
				,	''		as	[P1_ Address6]
				,	''		as	[P1_ Address7]
				,	''		as	[P1_ Postcode]
				,	''		as	[P1_ StartDateAtAddress]
				,	''		as	[P1_ EndDateAtAddress]
INTO			rm_files.[dbo].[TEMP_TO_TU]
--SELECT		COUNT(AJJB.CLIENTREFERENCE), COUNT(DISTINCT AJJB.CLIENTREFERENCE)
FROM			rm_files.[dbo].[LIT_TEMP_ORIGINAL]				AJJB
JOIN			RM.DBO.Account			ACC			ON ACC.ClientReference=AJJB.ClientReference
JOIN			RM.DBO.Customer			CUS			ON CUS.accountid=ACC.Accountid
JOIN			RM.DBO.CustomerAddress	CAM			ON CAM.accountid=ACC.Accountid AND CAM.AddressType = 'MAILING'
JOIN			RM.DBO.CustomerAddress	CAS			ON CAS.accountid=ACC.Accountid AND CAS.AddressType <> 'MAILING'
WHERE			cUS.firstname + ' ' + cUS.surname  IS NOT NULL 

--CS
SELECT			AJJB.clientreference	ClientId
				, cUS.[Full Name]
				, cUS.firstname 
				, cUS.surname    	
				, isnull(cUS.dateofbirth   		,''	) as	DateOfBirth
				, isnull(caM.addressline1   	,''	) as	Mailing_Address1
				, isnull(caM.addressline2   	,''	) as	Mailing_Address2
				, isnull(caM.addressline3		,''	) as	Mailing_Address3
				, isnull(caM.addressline4   	,''	) as	Mailing_Address4
				, isnull(caM.addressline5		,''	) as	Mailing_Address5
				, isnull(caM.addresspostcode	,''	) as	Mailing_Postcode
				, isnull(caS.addressline1   	,''	) as	supply_Address1
				, isnull(caS.addressline2   	,''	) as	supply_Address2
				, isnull(caS.addressline3		,''	) as	supply_Address3
				, isnull(caS.addressline4   	,''	) as	supply_Address4
				, isnull(caS.addressline5		,''	) as	supply_Address5
				, isnull(caS.addresspostcode	,''	) as	supply_Postcode
INTO			rm_files.[dbo].[TEMP_TO_CS]
--SELECT		COUNT(AJJB.CLIENTREFERENCE), COUNT(DISTINCT AJJB.CLIENTREFERENCE)
FROM			rm_files.[dbo].[LIT_TEMP_ORIGINAL]				AJJB
JOIN			RM.DBO.Account			ACC			ON ACC.ClientReference=AJJB.ClientReference
JOIN			RM.DBO.Customer			CUS			ON CUS.accountid=ACC.Accountid
JOIN			RM.DBO.CustomerAddress	CAM			ON CAM.accountid=ACC.Accountid AND CAM.AddressType = 'MAILING'
JOIN			RM.DBO.CustomerAddress	CAS			ON CAS.accountid=ACC.Accountid AND CAS.AddressType <> 'MAILING'