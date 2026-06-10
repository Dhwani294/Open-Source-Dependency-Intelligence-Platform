
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select abandonment_rate
from `erudite-river-423507-n3`.`vulngraph`.`mart_ecosystem_health`
where abandonment_rate is null



  
  
      
    ) dbt_internal_test