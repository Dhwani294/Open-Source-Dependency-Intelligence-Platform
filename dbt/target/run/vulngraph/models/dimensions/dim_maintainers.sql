
  
    

    create or replace table `erudite-river-423507-n3`.`vulngraph`.`dim_maintainers`
      
    
    

    
    OPTIONS()
    as (
      MERGE `vulngraph.dim_maintainers` T
USING source_data S
ON T.maintainer_id = S.maintainer_id

WHEN MATCHED THEN
UPDATE SET
    handle = S.handle,
    org = S.org,
    verified = S.verified

WHEN NOT MATCHED THEN
INSERT
(
    maintainer_id,
    handle,
    org,
    verified
)
VALUES
(
    S.maintainer_id,
    S.handle,
    S.org,
    S.verified
);



SELECT DISTINCT
    maintainer_id,
    handle,
    org,
    verified
FROM `erudite-river-423507-n3`.`vulngraph`.`stg_pypi_maintainers`
    );
  