use rm
go 

create procedure dbo.YU_NB_Production_Insert
as

--=====================================================================================
--=====================================================================================
--==		Insert into production
--=====================================================================================
--=====================================================================================	
insert into rm.dbo.account				 select * from rm_staging.dbo.account	
insert into rm.dbo.customer				 select * from rm_staging.dbo.customer			
insert into rm.dbo.customeraddress		 select * from rm_staging.dbo.customeraddress	
insert into rm.dbo.customertelephone	 select * from rm_staging.dbo.customertelephone	
insert into rm.dbo.supplementarydata	 select * from rm_staging.dbo.supplementarydata	

--=====================================================================================
--=====================================================================================
--==		Clear Staging Tables
--=====================================================================================
--=====================================================================================

delete from rm_staging.dbo.account	
delete from rm_staging.dbo.customer			
delete from rm_staging.dbo.customeraddress	
delete from rm_staging.dbo.customertelephone	
delete from rm_staging.dbo.supplementarydata	

--=====================================================================================
--=====================================================================================











