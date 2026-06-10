CREATE TABLE IF NOT EXISTS `vulngraph.stg_pypi_packages`
(
    batch_id STRING,
    package_id STRING,
    name STRING,
    ecosystem STRING,
    latest_version STRING,
    maintainer_id STRING,
    is_deprecated BOOL,
    ingested_at TIMESTAMP
)
PARTITION BY DATE(ingested_at)
CLUSTER BY package_id;