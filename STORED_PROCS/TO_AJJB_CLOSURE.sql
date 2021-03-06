USE [RM]
GO
/****** Object:  StoredProcedure [dbo].[TO_AJJB_CLOSURE]    Script Date: 3/2/2021 8:25:27 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER procedure [dbo].[TO_AJJB_CLOSURE]

as




UPDATE	rm.dbo.assignment
SET		RecallReason = acc.recallreason
		, recalldate = getdate()
--select *		
FROM	rm.dbo.Account acc
JOIN	rm.dbo.assignment ass	ON	acc.ClientReference = ass.[ClientReference] and ass.closuredate is null
where	acc.RecallDate is not null 
and		acc.closuredate is null
and		ass.recalldate is null
and		ass.closuredate is null
and		ass.dca = 'ajjb'



select acc.ClientReference		as acc_num
		, getdate()				as closure_date
		, ass.RecallReason			as outcome

into rm_files.dbo.[ToAJJB_TEMP_JUST_CLOSURE]
from rm.dbo.account	acc
left join rm.dbo.Assignment ass on ass.ClientReference = acc.ClientReference and ass.closuredate is null and ass.dca = 'AJJB'
where	cast(ass.recalldate as date) = cast(getdate() as date) 