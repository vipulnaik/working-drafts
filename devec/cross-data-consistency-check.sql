drop temporary table if exists ct1;

drop temporary table if exists ct2;

create temporary table ct1 as select
  region, year,
  cast(coalesce(sum(case when database_url = 'http://www.ggdc.net/maddison/Historical_Statistics/horizontal-file_02-2010.xls' and metric = 'GDP per capita' then `value` else 0 end), 0) as unsigned) as gdppc_maddison_2010,
  cast(coalesce(sum(case when database_url = 'http://www.ggdc.net/maddison/maddison-project/data/mpd_2013-01.xlsx' and metric = 'GDP per capita' then `value` else 0 end), 0) as unsigned) as gdppc_maddison_2013,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt61_data.xlsx' and metric = 'Real GDP per capita (Constant Prices: Chain series)' then `value` else 0 end), 0) as unsigned) as gdppc_pwt61,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt61_data.xlsx' and metric = 'Real GDP per capita (Constant Prices: Laspeyres), derived from growth rates of c, g, i' then `value` else 0 end), 0) as unsigned) as gdppc_pwt61_l,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt62_data.xlsx' and metric = 'Real GDP per capita (Constant Prices: Chain series)' then `value` else 0 end), 0) as unsigned) as gdppc_pwt62,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt62_data.xlsx' and metric = 'Real GDP per capita (Constant Prices: Laspeyres), derived from growth rates of c, g, i' then `value` else 0 end), 0) as unsigned) as gdppc_pwt62_l,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt63_nov182009version.zip' and metric = 'Real GDP per capita (Constant Prices: Chain series)' then `value` else 0 end), 0) as unsigned) as gdppc_pwt63,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt63_nov182009version.zip' and metric = 'Real GDP per capita (Constant Prices: Laspeyres), derived from growth rates of c, g, i' then `value` else 0 end), 0) as unsigned) as gdppc_pwt63_l,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt70_06032011version.zip' and metric = 'PPP Converted GDP Per Capita (Chain Series), at 2005 constant prices' then `value` else 0 end), 0) as unsigned) as gdppc_pwt70,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt71_11302012version.zip' and metric = 'PPP Converted GDP Per Capita (Chain Series), at 2005 constant prices' then `value` else 0 end), 0) as unsigned) as gdppc_pwt71,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt80.xlsx' and metric = 'Real GDP at constant 2005 national prices' then `value` else 0 end), 0)/coalesce(1 + sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt80.xlsx' and metric = 'Population' then `value` else 0 end), 1) as unsigned) as gdppc_pwt80,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt81.xlsx' and metric = 'Real GDP at constant 2005 national prices' then `value` else 0 end), 0)/coalesce(1 + sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt81.xlsx' and metric = 'Population' then `value` else 0 end), 1) as unsigned) as gdppc_pwt81,
  cast(coalesce(sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt90.xlsx' and metric = 'Real GDP at constant 2011 national prices' then `value` else 0 end), 0)/coalesce(1 + sum(case when database_url = 'http://www.rug.nl/ggdc/docs/pwt90.xlsx' and metric = 'Population' then `value` else 0 end), 1) as unsigned) as gdppc_pwt90
from data group by region, year;
