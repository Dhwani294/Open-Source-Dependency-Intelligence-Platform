CREATE TABLE IF NOT EXISTS `vulngraph.dim_packages`
(
    package_id STRING NOT NULL,
    name STRING NOT NULL,
    ecosystem STRING NOT NULL,
    latest_version STRING,

    maintainer_id STRING,

    is_deprecated BOOL,

    effective_from DATE NOT NULL,
    effective_to DATE,

    is_current BOOL NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY effective_from
CLUSTER BY package_id, ecosystem;