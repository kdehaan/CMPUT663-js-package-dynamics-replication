SELECT
    `version`,
    COUNT(*) AS `count`,
    AVG(`time_diff`) AS `avg_time_to_version`,
    MIN(`time_diff`) AS `min_time_to_version`,
    MAX(`time_diff`) AS `max_time_to_version`
FROM (
    SELECT
        `pv`.`package_id`,
        `pv`.`version`,
        `pv`.`released`,
        `sub`.`first_released`,
        TIMESTAMPDIFF(SECOND, `sub`.`first_released`, `pv`.`released`) AS `time_diff`
    FROM
        `package_versions` `pv`
        INNER JOIN
        (
            SELECT
                `package_id`,
                MIN(`released`) AS `first_released`
            FROM
                `package_versions`
            GROUP BY
                `package_id`
        ) `sub`
        ON `pv`.`package_id` = `sub`.`package_id`
) `xxx`
WHERE
    `version` REGEXP "^[0-9]+\\.[0-9]+\\.[0-9]+$" 
GROUP BY
    `version`;
