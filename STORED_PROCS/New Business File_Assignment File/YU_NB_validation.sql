use rm
go 

create procedure dbo.YU_NB_validation
as

DROP TABLE RM_FILES.dbo.DuplicatesInPlacement
DROP TABLE RM_FILES.dbo.DuplicatesInSystem

select		count(clientreference) vol
			, sum(CAST(Balance as Decimal(10,2))) val
from		#InsertTable

select		count(clientreference) DuplicatesInPlacement
INTO		RM_FILES.dbo.DuplicatesInPlacement 
from		#inserttable
group by	clientreference
having		count(clientreference)>1


select		count(a.clientreference) DuplicateOnSystem
INTO		RM_FILES.dbo.DuplicatesInSystem
from		#InsertTable		a
join		rm.dbo.account		acc			on a.ClientReference=acc.ClientReference


select		acc.*, cus.*
from		#InsertTable		a
join		rm.dbo.account		acc	on a.ClientReference=acc.ClientReference
join		rm.dbo.Customer		cus	on cus.accountid=acc.accountid












