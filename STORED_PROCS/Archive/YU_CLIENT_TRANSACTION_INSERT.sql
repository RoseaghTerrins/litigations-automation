USE RM
GO

create procedure	DBO.CLIENT_TRANSACTION_INSERT as 

drop table			#transaction
select				ClientReference
					, cast(TransactionValue as float) as transactionvalue
					, transactiondate
					, AdjustmentTypeCode
					, PreviousBalance
					, BalanceAfter
					, cast(TransactionValue as float) as paymentamount
into				#transaction
from				#trans
where				ClientReference is not null



-- insert into live table
insert into	rm.dbo.AccountTransaction
SELECT		acc.Accountid
			, Newid() TransactionID
			, null as FL_TransactionID
			, acc.ClientReference 
			, d.transactiondate as [Date]
			, case when adjustmenttypecode = 'pay'	then d.transactionvalue
					when adjustmenttypecode = 'prv' then d.transactionvalue*-1
					when adjustmenttypecode = 'nba' then d.transactionvalue
					when adjustmenttypecode = 'pba' then d.transactionvalue*-1 
					end as amount	
			, case when AdjustmentTypeCode in ('pay','prv') then
													case when ass.segment ='YU_Backbook' then '30'
														 when ass.segment = 'YU_Blended' then '17' 
														 when ass.segment = 'Litigation' then '35'
					else null end end as FL_CommissionRate
			, cast(round(			
							case	when adjustmenttypecode = 'pay'	then d.transactionvalue
									when adjustmenttypecode = 'prv' then d.transactionvalue*-1
									else 0 
									end 	
					* 
										(
											case	when ass.segment =	'YU_Backbook'	then '30'
													when ass.segment =	'YU_Blended'	then '17' 
													 when ass.segment = 'Litigation'	then '35'
											else null end																									 																						
										)
					,2 )as decimal (10,2)) FL_Commission
			, case when AdjustmentTypeCode in ('pay','prv')  and segment in ('YU_Backbook','YU_Blended') then '5'
					when AdjustmentTypeCode in ('pay','prv')  and segment in ('Litigation') then '2.5'
					else 0 end as JDM_CommissionRate

			, cast(round(			
							case	when adjustmenttypecode = 'pay'	then d.transactionvalue
									when adjustmenttypecode = 'prv' then d.transactionvalue*-1
									else 0 
									end 	
					* 
							case when AdjustmentTypeCode in ('pay','prv')  and segment in ('YU_Backbook','YU_Blended') then '5'
								when AdjustmentTypeCode in ('pay','prv')  and segment in ('Litigation') then '2.5'					
								else 0 end 	
								
					,2 )as decimal (10,2)) JDM_Commission

			, 'YU' as source
			, getdate() as dtstamp
			, ASSIGNMENTID
			, d.AdjustmentTypeCode  
from		#transaction	d
join		rm.dbo.account		acc on acc.ClientReference=d.ClientReference
left join	rm.dbo.ASSIGNMENT	ass	on ass.ACCOUNTID=acc.Accountid	and ass.ClosureDate is null



-- Update Outstanding Balance

update		rm.dbo.Account
set			OutstandingBalance = (acc.OriginalBalance - act.colls)
-- select *
from		rm.dbo.Account acc
join		(
			select acc.Accountid
					, sum(act.Amount) colls
			from rm.dbo.account					acc
			join rm.dbo.AccountTransaction		act		on acc.ClientReference=act.ClientReference
			group by acc.Accountid
			) act on act.Accountid= acc.Accountid