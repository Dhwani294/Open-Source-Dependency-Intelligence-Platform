

  create or replace view `erudite-river-423507-n3`.`vulngraph`.`stg_nvd`
  OPTIONS()
  as CREATE TABLE IF NOT EXISTS `vulngraph.stg_nvd`
(
    batch_id STRING,
    cve_id STRING,
    published_date TIMESTAMP,
    last_modified_date TIMESTAMP,
    severity_score FLOAT64,
    cvss_vector STRING,
    description STRING,
    ingested_at TIMESTAMP
)
PARTITION BY DATE(ingested_at)
CLUSTER BY cve_id;

SELECT
    cve_id,
    published_date,
    last_modified_date,
    severity_score,
    cvss_vector,
    description
FROM `erudite-river-423507-n3`.`vulngraph`.`stg_nvd`;

