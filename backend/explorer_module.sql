CREATE TABLE `user_t` (
`id` int(11) NOT NULL auto_increment,
`user_name` varchar(255) NULL ,
`user_password` varchar(255) NULL,
`create_time` timestamp NULL ON UPDATE CURRENT_TIMESTAMP,
`update_time` timestamp NULL ON UPDATE CURRENT_TIMESTAMP,
`permission` varchar(255) NULL,
PRIMARY KEY (`id`) ,
UNIQUE INDEX `uniq_user_name` (`user_name` ASC)
);
CREATE TABLE `space_t` (
`id` int(11) NOT NULL auto_increment,
`file_name` varchar(255) NULL,
`update_time` timestamp NULL ON UPDATE CURRENT_TIMESTAMP,
`file_type` varchar(64) NULL,
`file_size` varchar(255) NULL,
`create_time` timestamp NULL ON UPDATE CURRENT_TIMESTAMP,
`author_name` varchar(32) NULL,
`desc_content` text NULL,
`user_id` int(11) NULL,
PRIMARY KEY (`id`) 
);

ALTER TABLE `space_t` ADD CONSTRAINT `foreign_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_t` (`id`) ON DELETE CASCADE;

