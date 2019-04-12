CREATE TABLE `package_versions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `package_id` BIGINT NOT NULL,
    `version` VARCHAR(126) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
    `released` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`),
    UNIQUE KEY (`package_id`, `version`)
);
