{{ config(materialized='table') }}

WITH package_risk AS (

    SELECT

        p.package_id,

        p.name,

        p.ecosystem,

        p.maintainer_id,

        COUNT(f.vuln_id) AS vulnerability_count,

        MAX(f.severity_score) AS max_severity,

        AVG(f.days_to_patch) AS avg_days_to_patch

    FROM {{ ref('dim_packages') }} p

    LEFT JOIN {{ ref('fact_vulnerability_exposure') }} f
        ON p.package_id = f.package_id

    GROUP BY
        p.package_id,
        p.name,
        p.ecosystem,
        p.maintainer_id

)

SELECT

    package_id,

    name,

    ecosystem,

    maintainer_id,

    vulnerability_count,

    max_severity,

    avg_days_to_patch,

    CASE
        WHEN max_severity >= 9.0
        THEN 'CRITICAL'

        WHEN max_severity >= 7.0
        THEN 'HIGH'

        WHEN max_severity >= 4.0
        THEN 'MEDIUM'

        ELSE 'LOW'
    END AS risk_band

FROM package_risk