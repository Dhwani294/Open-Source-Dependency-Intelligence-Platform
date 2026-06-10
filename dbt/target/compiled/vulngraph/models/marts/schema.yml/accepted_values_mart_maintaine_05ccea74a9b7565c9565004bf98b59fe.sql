
    
    

with all_values as (

    select
        risk_band as value_field,
        count(*) as n_records

    from `erudite-river-423507-n3`.`vulngraph`.`mart_maintainer_risk`
    group by risk_band

)

select *
from all_values
where value_field not in (
    'LOW','MEDIUM','HIGH','CRITICAL'
)


