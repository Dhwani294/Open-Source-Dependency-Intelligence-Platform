CREATE TABLE IF NOT EXISTS `vulngraph.dim_maintainers`
(
    maintainer_id STRING NOT NULL,
    handle STRING NOT NULL,
    org STRING,
    verified BOOL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY maintainer_id, handle;