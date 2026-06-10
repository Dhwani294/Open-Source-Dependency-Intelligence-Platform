CREATE TABLE IF NOT EXISTS `vulngraph.stg_github_advisory`
(
    batch_id STRING,
    ghsa_id STRING,
    cve_id STRING,
    package_name STRING,
    ecosystem STRING,
    severity STRING,
    cvss_score FLOAT64,
    patched_version STRING,
    published_date TIMESTAMP,
    ingested_at TIMESTAMP
)
PARTITION BY DATE(published_date)
CLUSTER BY ghsa_id;

SELECT
    ghsa_id,
    cve_id,
    package_name,
    ecosystem,
    severity,
    cvss_score,
    patched_version,
    published_date
FROM `erudite-river-423507-n3`.`vulngraph`.`stg_github_advisory`