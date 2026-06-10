{{ config(materialized='table') }}

SELECT
    MD5(package_name) AS dependent_package_id,

    MD5(dependency_name) AS dependency_id,

    version_constraint,

    ecosystem,

    depth_level,

    snapshot_date

FROM {{ source('raw', 'stg_libraries_io') }}