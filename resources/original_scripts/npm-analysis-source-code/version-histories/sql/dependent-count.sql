-- counts how many projects were dependent on (any version of) a package each
-- time a new version came out. Limited to "express" here because I'm tired of
-- hearing my disk spin.
CREATE TABLE `package_dependents_at_releases`
SELECT
    `p`.`id` AS `package_id`,
    -- `p`.`name` AS `package_name`,
    `pv`.`version` AS `version`,
    `pv`.`released` AS `released`,
    COUNT(*) AS `dependents`
    -- `vqr`.`version_query` AS `version_query`,
    -- `vqr`.`started` AS `resolution_started`,
    -- `vqr`.`ended` AS `resolution_ended`
    -- `ped`.`started` AS `query_started`,
    -- `ped`.`ended` AS `query_ended`
FROM
    `packages` `p`,
    `package_versions` `pv`,
    `project_explicit_dependencies` `ped`
    -- `version_query_resolutions` `vqr`
WHERE
    `p`.`name` = "express" AND --
    `p`.`id` = `pv`.`package_id` AND
    `pv`.`version` REGEXP "^[0-9]+\\.[0-9]+\\.[0-9]+$" AND
    -- `vqr`.`package_id` = `p`.`id` AND
    -- `vqr`.`result_version` = `pv`.`id` AND
    -- `pv`.`released` BETWEEN `vqr`.`started` AND `vqr`.`ended` AND
    `ped`.`package_id` = `p`.`id` AND
    -- `ped`.`version_query` = `vqr`.`version_query` AND
    `ped`.`ended` > `pv`.`released` AND `ped`.`started` < `pv`.`released` AND
    1 = 1
GROUP BY
   `pv`.`id`
ORDER BY
    `released`
;
