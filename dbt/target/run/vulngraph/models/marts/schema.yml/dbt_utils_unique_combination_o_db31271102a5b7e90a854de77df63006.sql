
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  





with validation_errors as (

    select
        ecosystem, exposure_date
    from `erudite-river-423507-n3`.`vulngraph`.`mart_patch_velocity`
    group by ecosystem, exposure_date
    having count(*) > 1

)

select *
from validation_errors



  
  
      
    ) dbt_internal_test