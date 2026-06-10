
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select vuln_id
from `erudite-river-423507-n3`.`vulngraph`.`mart_blast_radius`
where vuln_id is null



  
  
      
    ) dbt_internal_test