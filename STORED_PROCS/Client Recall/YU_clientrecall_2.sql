use rm
go 

create procedure dbo.YU_clientrecall_2
as

UPDATE	rm.dbo.Account
SET		RecallReason = act.recallreason
		, recalldate = getdate()
--select *		
FROM	##Clientclosure act
JOIN	rm.dbo.Account acc	ON	acc.ClientReference = act.[ClientReference] and acc.RecallDate is null;


select *
from rm.dbo.Account
where cast(recalldate as date) = cast(getdate() as date)


