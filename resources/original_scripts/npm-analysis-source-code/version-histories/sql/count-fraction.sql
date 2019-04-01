SELECT
    `rd`.`version`,
    `rd`.`released` AS `released`,
    UNIX_TIMESTAMP(`rd`.`released`) AS `ts`,
    `rd`.`resolvable_dependents` AS `resolvable`,
    `ad`.`resolved_dependents` AS `resolved`,
    `ad`.`resolved_dependents` / `rd`.`resolvable_dependents` AS `fraction`
FROM
    `resolvable_dependents` `rd`
        LEFT OUTER JOIN 
    `resolved_dependents` `ad`
        ON
    `rd`.`version` = `ad`.`version`
WHERE
    `rd`.`package_id` = `ad`.`package_id` AND
    `rd`.`version` = `ad`.`version`
ORDER BY
    `released`
;
