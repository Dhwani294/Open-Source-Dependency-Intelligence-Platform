
  
    

    create or replace table `erudite-river-423507-n3`.`vulngraph`.`dim_versions`
      
    
    

    
    OPTIONS()
    as (
      MERGE `vulngraph.dim_versions` T
USING source_data S
ON T.version_id = S.version_id

WHEN MATCHED THEN
UPDATE SET
    semver = S.semver,
    release_date = S.release_date,
    yanked_flag = S.yanked_flag

WHEN NOT MATCHED THEN
INSERT
(
    version_id,
    package_id,
    semver,
    release_date,
    yanked_flag
)
VALUES
(
    S.version_id,
    S.package_id,
    S.semver,
    S.release_date,
    S.yanked_flag
);



SELECT DISTINCT
    version_id,
    package_id,
    semver,
    release_date,
    yanked_flag
FROM `erudite-river-423507-n3`.`vulngraph`.`stg_pypi_versions`
    );
  