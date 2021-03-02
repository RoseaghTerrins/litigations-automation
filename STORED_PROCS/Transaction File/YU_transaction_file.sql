use rm
go 

create procedure dbo.YU_transaction_file
as
select		acc.ClientReference
			, transactionid
			, amount as paymentamount
			, cast(date as date) as transactiondate
			, 'PAY' as transactiontypecode
			, JDM_CommissionRate+FL_CommissionRate as  JustCommissionRate
			, cast(amount*((JDM_CommissionRate+FL_CommissionRate)/100) as decimal(10,2))as JustCommissionvalue
			, amount - (cast(amount*((JDM_CommissionRate+FL_CommissionRate)/100) as decimal(10,2))) as NetCollections
			, dtstamp
			, source
into		rm_files.dbo.ToYU_PAY_TEMP

-- select *
from		rm.dbo.account acc
join		rm.dbo.AccountTransaction at on at.Accountid=acc.Accountid and source = 'first locate'
join		rm.dbo.assignment			ass on ass.assignmentid=at.assignmentid 
where		cast(at.dtstamp as date) = cast(getdate() as date)
