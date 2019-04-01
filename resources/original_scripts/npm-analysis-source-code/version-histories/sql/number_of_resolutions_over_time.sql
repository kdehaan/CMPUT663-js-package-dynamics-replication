SELECT
    EXTRACT(YEAR_MONTH FROM `started`) AS `year_month`,
    AVG(`num_versions` / DATEDIFF(`ended`, `started`)) AS `avg_versions_per_day`
FROM
    version_resolution_counts
GROUP BY
    `year_month`
ORDER BY
    `year_month`
;


