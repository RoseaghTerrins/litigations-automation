use rm
go


create procedure dbo.first_locate_agmts_insert as 

insert into rm.dbo.arrangements

select arr.*

from #agmts arr
join rm.dbo.account acc on acc.ClientReference=arr.Reference
where	[Agreement_Type] <> 'full on'
and		OutstandingBalance > 0
