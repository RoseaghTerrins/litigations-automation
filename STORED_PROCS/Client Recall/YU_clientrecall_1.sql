use rm
go 

create procedure dbo.YU_clientrecall_1
as

SELECT cl.[ClientReference]
		,cl.[ClosureCode] recallreason
		,case when  cl.[ClosureDate] = '' then null else CONVERT(NVARCHAR(255),CONVERT(date, cl.[ClosureDate],105))								end as recalldate
		,cl.[Comments]
into ##Clientclosure
--select *
FROM #Closure cl
join rm.dbo.account acc on acc.clientreference = cl.clientreference and acc.closurereason is null
where cl.clientreference <> ''


-- check closure already exists
select *
from ##Clientclosure cc
join rm.dbo.account acc	on acc.ClientReference=cc.ClientReference and acc.RecallDate is not null



