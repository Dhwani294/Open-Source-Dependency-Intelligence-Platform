{{ config(materialized='table') }}

WITH RECURSIVE dependency_tree AS (

    -- 1. Seed: directly vulnerable packages
    SELECT
        f.vuln_id,
        f.package_id AS root_package_id,
        f.package_id AS impacted_package_id,
        0 AS depth_level

    FROM {{ ref('fact_vulnerability_exposure') }} f

    UNION ALL

    -- 2. Recursive expansion
    SELECT
        dt.vuln_id,
        dt.root_package_id,
        d.dependency_id AS impacted_package_id,
        dt.depth_level + 1 AS depth_level

    FROM dependency_tree dt

    INNER JOIN {{ ref('fact_dependency_graph') }} d
        ON dt.impacted_package_id = d.dependent_package_id

    WHERE dt.depth_level < 5

),

deduplicated AS (

    SELECT DISTINCT
        vuln_id,
        impacted_package_id,
        depth_level
    FROM dependency_tree

),

final AS (

    SELECT

        vuln_id,

        COUNT(DISTINCT impacted_package_id)
            AS total_impacted_packages,

        MAX(depth_level)
            AS max_depth_reached

    FROM deduplicated

    GROUP BY vuln_id

)

SELECT
    *
FROM final