CREATE TABLE IF NOT EXISTS `vulngraph.stg_pypi_versions`
(
    batch_id STRING,
    version_id STRING,
    package_id STRING,
    semver STRING,
    release_date DATE,
    yanked_flag BOOL,
    ingested_at TIMESTAMP
)
PARTITION BY release_date
CLUSTER BY package_id;