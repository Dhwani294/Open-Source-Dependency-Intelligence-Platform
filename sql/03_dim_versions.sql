CREATE TABLE IF NOT EXISTS `vulngraph.dim_versions`
(
    version_id STRING NOT NULL,
    package_id STRING NOT NULL,

    semver STRING NOT NULL,
    release_date DATE,

    yanked_flag BOOL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY release_date
CLUSTER BY package_id;