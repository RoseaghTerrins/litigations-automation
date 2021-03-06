USE [RM]
GO
/****** Object:  StoredProcedure [dbo].[AJJB_CLOSURE]    Script Date: 3/2/2021 8:23:38 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER procedure [dbo].[AJJB_CLOSURE]
as
SELECT CLIENT_REFERENCE [Reference]
		, CRS_REFERENCE
		, CLOSURE_DATE [Date]
		, cc.closurecode
into ##closures1
FROM ##Closures c
join rm.dbo.closurecodes cc on cc.closurereason = c.closure_reason

--Checks for any invalid or new closure codes
select			* 
from			##closures c
left join		##closures1 cc on cc.reference = c.CLIENT_REFERENCE 
where			cc.reference is null

--Checks if account has already been closed back to the client
select			'account' as [table], acc.clientreference, acc.RecallDate, acc.Recallreason, acc.ClosureDate , acc.ClosureReason
from			##closures1	cl
join			rm.dbo.account acc on acc.ClientReference=cl.Reference 
									and (acc.ClosureDate is not null)

--Checks if the assignment has already been closed
select			'assignment' as [table], ass.clientreference, ass.RecallDate, ass.Recallreason, ass.ClosureDate , ass.ClosureReason
from			##closures1	cl
join			rm.dbo.Assignment ass on ass.ClientReference=cl.Reference 
									and dca <> 'first locate' 
									and (ass.ClosureDate is not null)

--update assignment table
UPDATE	rm.dbo.ASSIGNMENT
SET		ClosureReason = act.closurecode
		, ClosureDate = getdate()
--select *
FROM	##closures1 act
JOIN	rm.dbo.ASSIGNMENT ass	ON	ass.ClientReference = act.Reference 
									and ass.dca <> 'first locate' 
									and ass.ClosureDate is null