CREATE TABLE `project_explicit_dependencies` (
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `project_id` BIGINT NOT NULL,
    `package_id` BIGINT NOT NULL,
    `is_dev_dependency` BOOLEAN NOT NULL,
    `version_query` VARCHAR(126) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
    `started` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ended` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
    FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`)
);
