
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select avg_days_to_patch
from `erudite-river-423507-n3`.`vulngraph`.`mart_patch_velocity`
where avg_days_to_patch is null



  
  
      
    ) dbt_internal_test