
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select package_id
from `erudite-river-423507-n3`.`vulngraph`.`mart_maintainer_risk`
where package_id is null



  
  
      
    ) dbt_internal_test