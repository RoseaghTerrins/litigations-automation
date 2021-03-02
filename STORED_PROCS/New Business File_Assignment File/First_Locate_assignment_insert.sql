use rm
go 

create procedure dbo.FIRST_LOCATE_assignment_insert
as

INSERT  into rm.dbo.assignment
select		ac.[ClientReference]						
		,	ac.Accountid
		,	newid()									Assignmentid
		,	'YU_Blended'							Segment									
		,	getdate()								AssignedDate
		,	'First Locate'							DCA
		,	OriginalBalance							AssignedAmount
		,	NULL									CLOsuredate
		,	null									recallreason
		,	null									recalldate
		,	null										closurereason

from rm.dbo.account					ac
left join rm.dbo.Assignment			ass			on ass.AccountID=ac.Accountid
WHERE CAST(AC.RECEIVEDDATE AS DATE) = cast(getdate() as date)
and ass.AccountID is null




SELECT * 
FROM RM.DBO.ASSIGNMENT
WHERE CAST(ASSIGNEDDATE AS DATE) = CAST(GETDATE() AS DATE)
	
select clientreference, LastPaymentAmount,* from  #InsertTable










