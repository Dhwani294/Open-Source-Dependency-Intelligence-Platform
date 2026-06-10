CREATE TABLE IF NOT EXISTS `vulngraph.fact_dependency_graph`
(
    dependent_package_id STRING NOT NULL,

    dependency_id STRING NOT NULL,

    version_constraint STRING,

    ecosystem STRING,

    depth_level INT64,

    snapshot_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY snapshot_date
CLUSTER BY dependent_package_id, dependency_id;