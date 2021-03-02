
use rm
go
Create procedure dbo.first_locate_activity_insert
as 
drop table #Activity
insert into rm.dbo.activity
select [Account_Number] clientreference	
	, Activity
	, CONVERT(NVARCHAR(255),CONVERT(date, date,105)) date
	, ass.AssignmentID
--select *
from #Activity		act
join rm.dbo.Assignment ass on ass.ClientReference = act.[Account_Number] and ass.dca = 'first locate'

