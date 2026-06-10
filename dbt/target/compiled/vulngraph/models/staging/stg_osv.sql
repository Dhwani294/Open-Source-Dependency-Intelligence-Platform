CREATE TABLE IF NOT EXISTS `vulngraph.stg_osv`
(
    batch_id STRING,
    vuln_id STRING,
    ecosystem STRING,
    package_name STRING,
    severity_score FLOAT64,
    severity_bucket STRING,
    affected_version STRING,
    fixed_version STRING,
    published_date TIMESTAMP,
    ingested_at TIMESTAMP
)
PARTITION BY DATE(published_date)
CLUSTER BY vuln_id;

SELECT
    vuln_id,
    ecosystem,
    package_name,
    severity_score,
    severity_bucket,
    affected_version,
    fixed_version,
    published_date
FROM `erudite-river-423507-n3`.`vulngraph`.`stg_osv`