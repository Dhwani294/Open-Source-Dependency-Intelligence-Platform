SELECT
    package_id,
    name,
    ecosystem,
    latest_version,
    maintainer_id,
    is_deprecated
FROM {{ source('raw', 'stg_pypi_packages') }}