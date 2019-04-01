SELECT
    *,
    DATEDIFF(`ended`, `started`) AS `days`,
    `num_versions` / DATEDIFF(`ended`, `started`) AS `ratio`
FROM
    `version_resolution_counts`
GROUP BY
    `package_name`, `started`, `ended`
ORDER BY `ratio` DESC
LIMIT 0,10;

