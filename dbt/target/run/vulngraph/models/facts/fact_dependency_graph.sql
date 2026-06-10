
  
    

    create or replace table `erudite-river-423507-n3`.`vulngraph`.`fact_dependency_graph`
      
    
    

    
    OPTIONS()
    as (
      

SELECT
    MD5(package_name) AS dependent_package_id,

    MD5(dependency_name) AS dependency_id,

    version_constraint,

    ecosystem,

    depth_level,

    snapshot_date

FROM `erudite-river-423507-n3`.`vulngraph`.`stg_libraries_io`
    );
  