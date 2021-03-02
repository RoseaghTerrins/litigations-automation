use RM
go

create procedure first_locate_agmts_insert

as
insert into rm.dbo.arrangements

select  arr.[Reference]
      , arr.[1LocRef]
	  , CONVERT(NVARCHAR(255),CONVERT(date, arr.[Date Set],105)) [Date Set]
      , arr.[Set by]
      , arr.[Client]
      , arr.[Segment]
      , arr.[Balance]
      , arr.[Method]
      , arr.[Agreement Type]
      , arr.[Frequency]
	  , CONVERT(NVARCHAR(255),CONVERT(date, arr.[First Payment Date],105)) [First Payment Date]
      , arr.[First Payment Amount]
      , arr.[Ongoing Payment Amount]

from #agmts arr
join rm.dbo.account acc on acc.ClientReference=arr.Reference
where	[Agreement Type] <> 'full on'
and		OutstandingBalance > 0