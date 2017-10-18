drop temporary table if exists ct1;

drop temporary table if exists ct2;

create temporary table ct1 as select
  region, year,
  coalesce(sum(case when database_url = 'http://www.ggdc.net/maddison/Historical_Statistics/horizontal-file_02-2010.xls' and metric = 'GDP per capita' then `value` else 0 end), 0) as gdppc_maddison_2010,
  coalesce(sum(case when database_url = 'http://www.ggdc.net/maddison/maddison-project/data/mpd_2013-01.xlsx' and metric = 'GDP per capita' then `value` else 0 end), 0) as gdppc_maddison_2013,
  coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt61_data.xlsx' and metric = 'Real GDP per capita (Constant Prices: Chain series)' then `value` else 0 end), 0) as gdppc_pwt61,
  coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt62_data.xlsx' and metric = 'Real GDP per capita (Constant Prices: Chain series)' then `value` else 0 end), 0) as gdppc_pwt62,
  coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt63_data.xlsx' and metric = 'Real GDP per capita (Constant Prices: Chain series)' then `value` else 0 end), 0) as gdppc_pwt63,
  coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt70_06032011version.zip' and metric = 'PPP Converted GDP Per Capita (Chain Series), at 2005 constant prices' then `value` else 0 end), 0) as gdppc_pwt70,
  coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt71_11302012version.zip' and metric = 'PPP Converted GDP Per Capita (Chain Series), at 2005 constant prices' then `value` else 0 end), 0) as gdppc_pwt71
from data group by region, year;
