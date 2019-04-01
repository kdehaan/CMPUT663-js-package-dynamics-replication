 SELECT
    -- *,
    `p`.`name`,
    `ped`.`version_query`,
    `ped`.`started` AS `query_started`,
    `ped`.`ended` AS `query_ended`,
    -- `vqr`.`started` AS `resolution_started`,
    -- `pv`.`version` AS `resolved_version`,
    COUNT(DISTINCT `pv`.`version`) AS `number_of_resolutions`
    
FROM
    `packages` AS `p`,
    `package_versions` AS `pv`,
    `project_explicit_dependencies` AS `ped`,
    `version_query_resolutions` AS `vqr`
WHERE
    -- `ped`.`project_id` = 6 AND -- just for test
    `p`.`id`=`pv`.`package_id`
    AND `ped`.`package_id` = `pv`.`package_id`
    AND `ped`.`version_query` = `vqr`.`version_query`
    AND `ped`.`started` <= `vqr`.`ended` AND `ped`.`ended` >= `vqr`.`started`
    AND `pv`.`id`=`vqr`.`result_version`
    AND `p`.`name` = "mkdirp"
GROUP BY `ped`.`id`;
