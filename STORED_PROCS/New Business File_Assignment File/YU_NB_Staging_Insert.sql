use rm
go 

create procedure dbo.YU_NB_Staging_Insert
as

--=====================================================================================
--==		Clear Staging Tables
--=====================================================================================

delete from rm_staging.dbo.account	
delete from rm_staging.dbo.customer			
delete from rm_staging.dbo.customeraddress	
delete from rm_staging.dbo.customertelephone	
delete from rm_staging.dbo.supplementarydata	

--=====================================================================================
--==		Insert into staging tables
--=====================================================================================

--==		Account Insert
--=====================================================================================
insert into rm_staging.dbo.Account
SELECT		newid()										Accountid
			, cast(cast(cast(clientreference as float) as int) as nvarchar(50))							ClientReference
			, CAST(Balance as Decimal(10,2)) as 			OriginalBalance
			, CAST(Balance as Decimal(10,2)) as				OutstandingBalance
			, 'YU' as										ClientName
			, getdate()										ReceivedDate
			, null as										closurereason
			, null as										closuredate
			, null as										recalldate
			, null as										recallreason
--into rm_staging.dbo.Account
FROM		#InsertTable


--==		Customer Insert
--=====================================================================================
insert into rm_staging.dbo.Customer
select		acc.accountid
			, newid()	CustomerID
			,case when  FirstName					= '' then null else CAST(FirstName as Varchar(50))										end as [FirstName]
			,case when	Surname						= '' then null else CAST(Surname as Varchar(50))										end as [Surname]
			,case when	CustomerName				= '' then null else CAST(CustomerName as Varchar (100))									end as [Full Name]
			,case when  dateofbirth = '' then null else CONVERT(NVARCHAR(255),CONVERT(date, dateofbirth,105))								end as [DateofBirth]
			, getdate() DTStamp
--into rm_staging.dbo.Customer		
--select *
from		#InsertTable							Cf
join		RM_Staging.dbo.account							acc on acc.ClientReference=cf.ClientReference

 

 --==		Address Insert
--=====================================================================================	
insert into rm_staging.dbo.CustomerAddress
select		acc.accountid
			, newid()	AddressID
			, ad.AddressType
			, ad.[AddressLine1]
			, ad.[AddressLine2]
			, ad.[AddressLine3]
			, ad.[AddressLine4]
			, ad.[AddressLine5]
			, ad.[AddressPostcode]
			, getdate() as DTStamp
--into rm.dbo.CustomerAddress
from		#InsertTable		Cf
join		rm_staging.dbo.account							acc on acc.ClientReference=cf.ClientReference
left join
		(
			select accountid, cf.ClientReference, 'Mailing' as AddressType
			,case when	MailingAddressLine1			= '' then null else cAST(MailingAddressLine1 as Varchar(80))							end as [AddressLine1]
			,case when	MailingAddressLine2			= '' then null else CAST(MailingAddressLine2 as Varchar(80))							end as [AddressLine2]
			,case when	MailingAddressLine3			= '' then null else CAST(MailingAddressLine3 as Varchar(80))							end as [AddressLine3]
			,case when	MailingAddressLine4			= '' then null else CAST(MailingAddressLine4 as Varchar(80))							end as [AddressLine4]
			,case when	MailingAddressLine5			= '' then null else CAST(MailingAddressLine5 as Varchar(80))							end as [AddressLine5]
			,case when	MailingAddressPostcode		= '' then null else CAST(MailingAddressPostcode as Varchar(15)) 						end as [AddressPostcode]
			from #InsertTable		Cf
			join rm_staging.dbo.account							acc on acc.ClientReference=cf.ClientReference
		union
			select accountid, cf.ClientReference, 'Supply' as AddressType
			,case when	SupplyAddressLine1 			= '' then null else CAST(SupplyAddressLine1 as Varchar(80)) 							end as [AddressLine1]
			,case when	SupplyAddressLine2 			= '' then null else CAST(SupplyAddressLine2 as Varchar(80)) 							end as [AddressLine2]
			,case when	SupplyAddressLine3 			= '' then null else CAST(SupplyAddressLine3 as Varchar(80)) 							end as [AddressLine3]
			,case when	SupplyAddressLine4 			= '' then null else CAST(SupplyAddressLine4 as Varchar(80)) 							end as [AddressLine4]
			,case when	SupplyAddressLine5 			= '' then null else CAST(SupplyAddressLine5 as Varchar(80)) 							end as [AddressLine5]
			,case when	SupplyAddressPostcode		= '' then null else CAST(SupplyAddressPostcode as Varchar(15)) 							end as [AddressPostcode]
			from #InsertTable		Cf
			join rm_staging.dbo.account							acc on acc.ClientReference=cf.ClientReference
		) ad on ad.ClientReference=acc.ClientReference
where		[AddressLine1] is not null and [AddressPostcode] is not null


--==		Contact Insert
--=====================================================================================
insert into rm_staging.dbo.CustomerTelephone
select		accountid
			, newid() as TelephoneID
			, Number 
--into rm.dbo.CustomerTelephone
from
	(
		select		accountid, 
					case when	Telephone1	= '' then null else CAST(Telephone1 as Varchar(35)) 									end as [Number] 
		from		#InsertTable Cf			
		join		rm_staging.dbo.account	acc on acc.ClientReference=cf.ClientReference
		where		telephone1 <> '' 
		and			Telephone1 <>'0'
	union
		select		accountid, 
					case when	Telephone2	= '' then null else CAST(Telephone2 as Varchar(35)) 									end as [Number] 
		from		#InsertTable Cf			
		join		rm_staging.dbo.account	acc on acc.ClientReference=cf.ClientReference
		where		telephone2 <> ''
		and			Telephone2 <>'0'
	union
		select		accountid, 
					case when	Telephone3	= '' then null else CAST(Telephone3 as Varchar(35)) 									end as [Number] 
		from		#InsertTable Cf			
		join		rm_staging.dbo.account	acc on acc.ClientReference=cf.ClientReference
		where		telephone3 <> ''
		and			Telephone3 <>'0'
	) a


--==		Supplementary Data
--=====================================================================================
insert into rm_staging.dbo.supplementarydata
SELECT	ACC.ClientReference	
		, CAST(Balance as Decimal(10,2)) as [Balance]
		, case when	NB.LastPaymentDate				= '' then null else CONVERT(NVARCHAR(255),CONVERT(date, LastPaymentDate,105)) 				end as [Last Payment Date]		
		, case when	NB.LastPaymentAmount			= '' then null else cASE WHEN Isnumeric(NB.LastPaymentAmount) = 1 THEN CONVERT(DECIMAL(18,2),NB.LastPaymentAmount) ELSE 0 END	end as [Last Payment Amount]
		, case when	ProductName						= '' then null else CAST(ProductName as Varchar(40)) 										end as [Product Name]
		, case when	SupplyDateFrom					= '' then null else CONVERT(NVARCHAR(255),CONVERT(date, SupplyDateFrom,105)) 				end as [Supply Date From]
		, case when	SupplyDateTo					= '' then null else CONVERT(NVARCHAR(255),CONVERT(date, SupplyDateTo,105)) 					end as [Supply Date To]
		, [E-mail]  [e-mail]
		, [productname]
		, case when	[defaultdate]					= '' then null else CONVERT(NVARCHAR(255),CONVERT(date, [defaultdate],105)) 					end as [defaultdate]	
		, [LPC/FeesAddedtoBalance] [lpc/feesaddedtobalance]
		, nb.terminationreason
		, nb.accountsource
		, nb.parentaccountid
--select nb.*
FROM	rm_staging.DBO.ACCOUNT						ACC
JOIN	#InsertTable						NB		ON nb.clientreference = ACC.CLIENTREFERENCE










