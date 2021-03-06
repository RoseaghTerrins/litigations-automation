USE [RM]
GO
/****** Object:  StoredProcedure [dbo].[TO_AJJB_PAY]    Script Date: 3/2/2021 8:25:42 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


ALTER procedure [dbo].[TO_AJJB_PAY]
as
select		act.clientreference	 as ACC_NUM
			, cus.[Full Name] ACC_NAME
			, date	PAYMENT_DATE
			, act.Amount PAYMENT_AMOUNT
into		rm_files.dbo.ToAJJB_TEMP_JUST_PAY
from		rm.dbo.AccountTransaction	act
join		rm.dbo.account				acc		on acc.accountid=act.accountid
join		rm.dbo.Assignment			ass		on ass.AssignmentID=act.assignmentid and ass.dca='ajjb'
join		rm.dbo.Customer				cus		on cus.accountid=acc.Accountid	
where		source = 'YU'
and			adjustmenttypecode = 'pay'
and			cast(act.dtstamp as date) = cast(getdate() as date)
and			act.amount <>0