{{ config(materialized='table') }}

WITH package_health AS (

    SELECT

        ecosystem,

        COUNT(*) AS total_packages,

        COUNTIF(is_deprecated)
            AS deprecated_packages

    FROM {{ ref('dim_packages') }}

    GROUP BY ecosystem

),

patch_health AS (

    SELECT

        p.ecosystem,

        AVG(f.days_to_patch)
            AS avg_days_to_patch

    FROM {{ ref('fact_vulnerability_exposure') }} f

    INNER JOIN {{ ref('dim_packages') }} p
        ON f.package_id = p.package_id

    WHERE
        f.exposure_date >=
        DATE_SUB(
            CURRENT_DATE(),
            INTERVAL 90 DAY
        )

    GROUP BY p.ecosystem

)

SELECT

    ph.ecosystem,

    ph.total_packages,

    ph.deprecated_packages,

    SAFE_DIVIDE(
        ph.deprecated_packages,
        ph.total_packages
    ) AS abandonment_rate,

    pa.avg_days_to_patch

FROM package_health ph

LEFT JOIN patch_health pa
    ON ph.ecosystem = pa.ecosystem