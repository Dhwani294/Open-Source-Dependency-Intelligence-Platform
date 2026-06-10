UPDATE `vulngraph.dim_packages`
SET
    effective_to = CURRENT_DATE(),
    is_current = FALSE
WHERE
    package_id = @package_id
    AND is_current = TRUE
    AND (
        maintainer_id <> @maintainer_id
        OR
        is_deprecated <> @is_deprecated
    );

INSERT INTO `vulngraph.dim_packages`
(
    package_id,
    name,
    ecosystem,
    latest_version,
    maintainer_id,
    is_deprecated,
    effective_from,
    effective_to,
    is_current
)
VALUES
(
    @package_id,
    @name,
    @ecosystem,
    @latest_version,
    @maintainer_id,
    @is_deprecated,
    CURRENT_DATE(),
    NULL,
    TRUE
);
