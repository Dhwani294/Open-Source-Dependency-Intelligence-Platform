{{ config(materialized='table') }}

WITH exposure AS (

    SELECT
        f.vuln_id,
        f.days_to_patch,
        f.exposure_date,

        p.ecosystem

    FROM {{ ref('fact_vulnerability_exposure') }} f

    INNER JOIN {{ ref('dim_packages') }} p
        ON f.package_id = p.package_id

),

daily_metrics AS (

    SELECT

        ecosystem,

        exposure_date,

        AVG(days_to_patch) AS avg_days_to_patch

    FROM exposure

    GROUP BY
        ecosystem,
        exposure_date

)

SELECT

    ecosystem,

    exposure_date,

    avg_days_to_patch,

    AVG(avg_days_to_patch)
    OVER (
        PARTITION BY ecosystem
        ORDER BY exposure_date
        ROWS BETWEEN 29 PRECEDING
                 AND CURRENT ROW
    ) AS rolling_30_day_avg

FROM daily_metrics