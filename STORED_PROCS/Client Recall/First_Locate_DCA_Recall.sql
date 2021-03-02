use rm
go 

create procedure dbo.First_Locate_DCA_Recall
as

UPDATE	rm.dbo.assignment
SET		RecallReason = acc.recallreason
		, recalldate = getdate()

FROM	rm.dbo.Account acc
JOIN	rm.dbo.assignment ass	ON	acc.ClientReference = ass.[ClientReference] and ass.closuredate is null
where	acc.RecallDate is not null 
and		acc.closuredate is null
and		ass.recalldate is null
and		ass.closuredate is null


--drop table rm_files.dbo.[20201202_JUST_CLS]
select acc.ClientReference		as acc_no
		, acc.RecallReason			as outcome
		, null					as comment
		, getdate()				as recalldate
		, getdate()				as ClosureDate

into rm_files.dbo.[TEMP_ToFL_JUST_CLS]

--select *
from rm.dbo.account	acc
left join rm.dbo.Assignment ass on ass.ClientReference = acc.ClientReference and ass.closuredate is null and ass.dca = 'first locate'
where	cast(ass.recalldate as date) = cast(getdate() as date) 


