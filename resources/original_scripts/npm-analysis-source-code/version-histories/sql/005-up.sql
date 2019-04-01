CREATE TABLE `version_query_resolutions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `package_id` BIGINT NOT NULL,
    `version_query` VARCHAR(126) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
    `result_version` BIGINT NOT NULL,   
    `started` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ended` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`),
    FOREIGN KEY (`result_version`) REFERENCES `package_versions` (`id`)
);

CREATE INDEX `query_index` ON `version_query_resolutions` (`version_query`);

--- We need this one too!
CREATE INDEX `version_index` ON `package_versions` (`version`);
