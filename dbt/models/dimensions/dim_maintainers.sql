MERGE `vulngraph.dim_maintainers` T
USING source_data S
ON T.maintainer_id = S.maintainer_id

WHEN MATCHED THEN
UPDATE SET
    handle = S.handle,
    org = S.org,
    verified = S.verified

WHEN NOT MATCHED THEN
INSERT
(
    maintainer_id,
    handle,
    org,
    verified
)
VALUES
(
    S.maintainer_id,
    S.handle,
    S.org,
    S.verified
);

{{ config(materialized='table') }}

SELECT DISTINCT
    maintainer_id,
    handle,
    org,
    verified
FROM {{ source('raw', 'stg_pypi_maintainers') }}