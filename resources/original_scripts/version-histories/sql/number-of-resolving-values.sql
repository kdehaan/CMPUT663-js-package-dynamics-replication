-- Counts, for each project dependency, how many versions it can resolve to.
-- Stores this in a table because it takes forever.
CREATE TABLE `version_resolution_counts`
SELECT
    `ped`.`id`,
    `ped`.`project_id`,
    `p`.`name` AS `package_name`,
    `ped`.`version_query` AS `version_query`,
    `ped`.`started` AS `started`,
    `ped`.`ended` AS `ended`,
    COUNT(DISTINCT `vqr`.`result_version`) AS `num_versions`
FROM
    `project_explicit_dependencies` AS `ped`,
    `packages` AS `p`,
    `package_versions` AS `pv`,
    `version_query_resolutions` AS `vqr`
WHERE
    -- `ped`.`project_id` = 6 AND -- just for test
    `ped`.`version_query` = `vqr`.`version_query`
    AND `ped`.`started` <= `vqr`.`ended` AND `ped`.`ended` >= `vqr`.`started`
    AND `pv`.`id`=`vqr`.`result_version`
    AND `ped`.`package_id` = `pv`.`package_id`
    AND `p`.`id`=`pv`.`package_id`
GROUP BY
    `ped`.`id`
;
