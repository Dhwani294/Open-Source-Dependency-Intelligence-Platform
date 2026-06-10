MERGE `vulngraph.dim_versions` T
USING source_data S
ON T.version_id = S.version_id

WHEN MATCHED THEN
UPDATE SET
    semver = S.semver,
    release_date = S.release_date,
    yanked_flag = S.yanked_flag

WHEN NOT MATCHED THEN
INSERT
(
    version_id,
    package_id,
    semver,
    release_date,
    yanked_flag
)
VALUES
(
    S.version_id,
    S.package_id,
    S.semver,
    S.release_date,
    S.yanked_flag
);

{{ config(materialized='table') }}

SELECT DISTINCT
    version_id,
    package_id,
    semver,
    release_date,
    yanked_flag
FROM {{ source('raw', 'stg_pypi_versions') }}