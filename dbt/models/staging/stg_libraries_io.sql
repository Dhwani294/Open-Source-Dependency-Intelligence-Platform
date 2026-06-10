CREATE TABLE IF NOT EXISTS `vulngraph.stg_libraries_io`
(
    batch_id STRING,
    package_name STRING,
    dependency_name STRING,
    ecosystem STRING,
    version_constraint STRING,
    depth_level INT64,
    maintainer_handle STRING,
    deprecated_flag BOOL,
    snapshot_date DATE,
    ingested_at TIMESTAMP
)
PARTITION BY snapshot_date
CLUSTER BY package_name;

SELECT
    package_name,
    dependency_name,
    ecosystem,
    version_constraint,
    depth_level,
    maintainer_handle,
    deprecated_flag,
    snapshot_date
FROM {{ source('raw', 'stg_libraries_io') }}