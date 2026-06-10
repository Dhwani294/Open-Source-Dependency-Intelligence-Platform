
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ecosystem
from `erudite-river-423507-n3`.`vulngraph`.`mart_ecosystem_health`
where ecosystem is null



  
  
      
    ) dbt_internal_test