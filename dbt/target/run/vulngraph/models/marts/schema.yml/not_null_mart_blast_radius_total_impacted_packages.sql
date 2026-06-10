
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_impacted_packages
from `erudite-river-423507-n3`.`vulngraph`.`mart_blast_radius`
where total_impacted_packages is null



  
  
      
    ) dbt_internal_test