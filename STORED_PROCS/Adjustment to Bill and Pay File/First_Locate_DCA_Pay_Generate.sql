use rm
go 

create procedure dbo.FIRST_LOCATE_DCA_Pay_Generate
as


select		act.clientreference	 as acc_no
			, date
			, act.Amount 
into		rm_files.dbo.ToFL_Temp_JUST_PAY
from		rm.dbo.AccountTransaction	act
join		rm.dbo.account				acc		on acc.accountid=act.accountid
join		rm.dbo.Assignment			ass		on ass.AssignmentID=act.assignmentid and ass.dca='first locate'
where		source = 'YU'
and			adjustmenttypecode = 'pay'
and			cast(dtstamp as date) = cast(getdate() as date)
and			act.amount <>0

