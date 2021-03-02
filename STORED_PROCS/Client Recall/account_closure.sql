use rm
go 

create procedure dbo.account_closure
as

update		rm.dbo.account
set			ClosureDate = getdate()
			, ClosureReason = ass.ClosureReason
--select		*
from		rm.dbo.account				acc
join		rm.dbo.Assignment			ass		on ass.AccountID=acc.Accountid and ass.DCA = 'first locate'
left join	rm.dbo.Assignment			assl	on assl.AccountID=acc.Accountid and assl.DCA <> 'first locate'

where		ass.ClosureDate is not null and acc.ClosureDate is null and assl.AccountID is null
and			ass.ClosureReason  in ('BKT','CRQ','DIS','GWY','INS','IVA','PIF','PPA','SET', 'dan')

select		ClientReference
			, ClosureReason closurecode
			, closuredate 
			, null as comment
into		rm_files.dbo.[ToYU_TEMP_JUST_CLS]
from		rm.dbo.account
where		cast(closuredate as date) = cast(getdate() as date)



