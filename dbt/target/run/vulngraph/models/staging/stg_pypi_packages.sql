

  create or replace view `erudite-river-423507-n3`.`vulngraph`.`stg_pypi_packages`
  OPTIONS()
  as CREATE TABLE IF NOT EXISTS `vulngraph.stg_pypi_packages`
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
CLUSTER BY package_id;;

