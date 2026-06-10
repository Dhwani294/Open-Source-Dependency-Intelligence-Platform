
  
    

    create or replace table `erudite-river-423507-n3`.`vulngraph`.`dim_packages`
      
    
    

    
    OPTIONS()
    as (
      

WITH latest_package_state AS (

    SELECT
        package_id,
        name,
        ecosystem,
        latest_version,
        maintainer_id,
        is_deprecated,

        ROW_NUMBER() OVER (
            PARTITION BY package_id
            ORDER BY ingested_at DESC
        ) AS rn

    FROM `erudite-river-423507-n3`.`vulngraph`.`stg_pypi_packages`

)

SELECT
    package_id,
    name,
    ecosystem,
    latest_version,
    maintainer_id,
    is_deprecated
FROM latest_package_state
WHERE rn = 1
    );
  