
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select max_depth_reached
from `erudite-river-423507-n3`.`vulngraph`.`mart_blast_radius`
where max_depth_reached is null



  
  
      
    ) dbt_internal_test