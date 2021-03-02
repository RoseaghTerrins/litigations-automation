use rm
go 

create procedure dbo.first_locate_activity_insert
as

insert into rm.dbo.activity
select [Account Number] clientreference	
	, Activity
	, CONVERT(NVARCHAR(255),CONVERT(date, Date,105)) date
	, ass.AssignmentID
--select *
from #Activity		act
join rm.dbo.Assignment ass on ass.ClientReference = act.[Account Number] and ass.dca = 'first locate'

