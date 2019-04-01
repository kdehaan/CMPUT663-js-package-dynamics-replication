-- Counts how many projects resolved to a specific version of a package when it
-- came out.
CREATE TABLE `resolved_dependents`
SELECT
    `p`.`id` AS `package_id`,
    -- `p`.`name` AS `package_name`,
    `pv`.`version` AS `version`,
    `pv`.`released` AS `released`,
    COUNT(*) AS `resolved_dependents`
    -- `ped`.`started` AS `query_started`,
    -- `ped`.`ended` AS `query_ended`,
    -- `vqr`.`version_query` AS `version_query`,
    -- `vqr`.`started` AS `resolution_started`,
    -- `vqr`.`ended` AS `resolution_ended`
FROM
    `packages` `p`,
    `package_versions` `pv`,
    `project_explicit_dependencies` `ped`,
    `version_query_resolutions` `vqr`
WHERE
    `p`.`name` = "express" AND --
    `p`.`id` = `pv`.`package_id` AND
    `pv`.`version` REGEXP "^[0-9]+\\.[0-9]+\\.[0-9]+$" AND
    `vqr`.`package_id` = `p`.`id` AND
    `vqr`.`result_version` = `pv`.`id` AND
    `pv`.`released` BETWEEN `vqr`.`started` AND `vqr`.`ended` AND
    `ped`.`package_id` = `p`.`id` AND
    `ped`.`version_query` = `vqr`.`version_query` AND
    `pv`.`released` BETWEEN `ped`.`started` AND `ped`.`ended` AND
    1 = 1
GROUP BY
    `pv`.`id`
ORDER BY
    `released`
;
