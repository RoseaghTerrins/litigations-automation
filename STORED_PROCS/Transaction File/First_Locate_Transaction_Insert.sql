use rm
go 

create procedure dbo.First_Locate_Transaction_Insert
as

insert into rm.dbo.AccountTransaction
SELECT  acc.Accountid
		, Newid() TransactionID
		, [UID] FL_TransactionID
		, [Client Ref] as clientreference
		, [Date]
		, [Amount]	
		--, [Total Payments]
		--, [Balance]
		, [Commission Rate] FL_CommissionRate
		, [Commission] FL_Commission
		, 5 as JDM_CommissionRate
		, round([Amount] * .05,2) as JDM_Commission
		, 'First Locate' as source
		, getdate() as dtstampe
		, ass.ASSIGNMENTID
		, 'pay' as adjustmenttypecode

FROM #Transaction ap
join rm.dbo.account acc on acc.ClientReference=ap.[Client Ref]
join rm.dbo.ASSIGNMENT	ass on ass.accountid=acc.Accountid 
;
--===========================================================================================================================================================================================================================
--===========================================================================================================================================================================================================================
-- update balance
--===========================================================================================================================================================================================================================
--===========================================================================================================================================================================================================================
update		rm.dbo.Account
set			OutstandingBalance = (acc.OriginalBalance - act.colls)
-- select *
from		rm.dbo.Account acc
join		(
			select acc.Accountid
					, sum(act.Amount) colls
			from rm.dbo.account					acc
			join rm.dbo.AccountTransaction		act		on acc.ClientReference=act.ClientReference
			group by acc.Accountid
			) act on act.Accountid= acc.Accountid
join #Transaction tr on tr.[Client Ref] = acc.ClientReference
