





with validation_errors as (

    select
        ecosystem, exposure_date
    from `erudite-river-423507-n3`.`vulngraph`.`mart_patch_velocity`
    group by ecosystem, exposure_date
    having count(*) > 1

)

select *
from validation_errors


