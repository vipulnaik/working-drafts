create temporary table ct3 as select
  region, year,
  cast(coalesce(max(case when metric = 'Real GDP at constant 2005 national prices' and database_url = 'http://www.rug.nl/ggdc/docs/pwt80.xlsx' then value else 0 end),0) as unsigned) as value_2005id_80,
  cast(coalesce(max(case when metric = 'Real GDP at constant 2005 national prices' and database_url = 'http://www.rug.nl/ggdc/docs/pwt81.xlsx' then value else 0 end),0) as unsigned) as value_2005id_81,
  cast(coalesce(max(case when metric = 'Real GDP at constant 2011 national prices' and database_url = 'http://www.rug.nl/ggdc/docs/pwt90.xlsx' then value else 0 end),0) as unsigned) as value_2011id_90
  from data where metric in ('Real GDP at constant 2005 national prices', 'Real GDP at constant 2011 national prices') group by region, year;

create temporary table mm as select
  region,
  max(value_2005id_80 / value_2005id_81) as max_consistency,
  min(value_2005id_80 / value_2005id_81) as min_consistency,
  max(value_2005id_81 / value_2011id_90) as max_adjustment,
  min(value_2005id_81 / value_2011id_90) as min_adjustment
  from ct3 where value_2005id_80 > 0 and value_2005id_81 > 0 and value_2011id_90 > 0 group by region;
  
