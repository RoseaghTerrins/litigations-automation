USE RM
GO
create procedure dbo.LIT_PLACEMENT_PROCESS_2
as
--3) collating append								
--5) insert into assignment table					
--6) producing placement file						
--7) accounts that can be closed back to the client

--3) collating append								
--on the desktop there is a folder with sample data back from enrichment "Sample of data that comes back from enrichment"
-- Might be worth checking if Kieran has data schema's to load these in as there are a lot of fields, if not then I can select a few fields that we definitely need
SELECT			ds.CLIENTREFERENCE
				, cs.[DC_COMPANY_TYPE]
				, cs.[DC_SIC_DESC]
				, cs.[DC_SIC_2_DESC]
				, cs.[DC_CCJ_COUNT]
				, cs.[DC_CCJ_VALUE]
				, cs.[DC_IS_ACTIVE]
				, cs.[DC_SCORE_DATE]
				, cs.[DC_CREDIT_SCORE]
				, cs.[DC_CREDIT_SCORE_DESC]
				, cs.[DC_INTERNATIONAL_SCORE]
				, cs.[DC_CREDIT_SCORE_PREVIOUS]
				, cs.[DC_CREDIT_SCORE_DESC_PREVIOUS]
				, cs.[DC_SCORE_DATE_PREVIOUS]
				, cs.[DC_LTD_FLAG]
				, cs.[DC_SAFE_NUMBER]
				, cs.[DC_ALGORITHM]
				, cs.[DC_ALGORITHM_BANDING]
				, cs.[DC_ALGORITHM_DESCRIPTION]
				, tu.[DataDNA]
				, tu.[AddressType]
				, tu.[MatchLevel]
				, tu.[P2PScore]
				, tu.baiordertype
				, tu.baiordernumber
				, tu.baicourt
				, tu.judgementactivecount
				, tu.judgementtotalamount
				, case when pay30.clientreference is not null then 1 else 0 end as pay30flag
				, case when pay.clientreference is not null then 1 else 0 end as payflag
				, case when rpc.clientreference is not null then 1 else 0 end as rpc_flag
				, case when amg.Reference is not null then 1 else 0 end as arrangement_flag

--SELECT		COUNT(DS.CLIENTREFERENCE), COUNT(DISTINCT DS.CLIENTREFERENCE)
INTO			#DATASET
--select tu.*
FROM			rm_files.[dbo].[LIT_TEMP_ORIGINAL]	DS
LEFT JOIN		rm_files.[dbo].[TEMP_TO_CS]	CS ON CS.CLIENTID=DS.CLIENTREFERENCE
left JOIN		rm_files.[dbo].[TEMP_TO_TU]	TU ON TU.CLIENTID=DS.CLIENTREFERENCE
left join		(select clientreference from rm.dbo.AccountTransaction where datediff(dd,dtstamp,getdate())<30 and adjustmenttypecode = 'pay'  group by clientreference) pay30 on pay30.ClientReference=ds.CLIENTREFERENCE
left join		(select clientreference from rm.dbo.AccountTransaction where datediff(dd,dtstamp,getdate())>=30 and adjustmenttypecode = 'pay' group by clientreference) pay on pay.ClientReference=ds.CLIENTREFERENCE
left join		(select clientreference from rm.dbo.activity where activity like '%rpc%' group by clientreference) rpc on rpc.clientreference=ds.CLIENTREFERENCE
left join		(select reference from rm.dbo.arrangements group by reference) amg on amg.reference = ds.CLIENTREFERENCE
left join		rm.dbo.account	acc on acc.ClientReference = ds.CLIENTREFERENCE



--==================================================================================================================================================================================================
--4) finalising list of accounts for placement		
drop table		#lit
select			*
into			rm_files.[dbo].[TEMP_PLACEMENT_FILE]
from			#DATASET
where			isnull(DC_CREDIT_SCORE_DESC,'') not in ('Company is dissolved','Dissolution','In Liquidation','Voluntary Arrangement','Bankrupt')
and				pay30flag = '0'