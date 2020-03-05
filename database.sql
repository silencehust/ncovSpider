CREATE DATABASE `2019ncov`;
CREATE TABLE `details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `update_time` datetime DEFAULT NULL COMMENT '数据最后更新时间',
  `province` varchar(50) DEFAULT NULL COMMENT '省',
  `city` varchar(50) DEFAULT NULL COMMENT '市',
  `confirm` int DEFAULT NULL COMMENT '累计确诊',
  `confirm_add` int DEFAULT NULL COMMENT '新增确诊',
  `heal` int DEFAULT NULL COMMENT '累计治愈',
  `dead` int DEFAULT NULL COMMENT '累计死亡',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `history` (
  `ds` datetime NOT NULL COMMENT '日期',
  `confirm` int DEFAULT NULL COMMENT '累计确诊',
  `confirm_add` int DEFAULT NULL COMMENT '当日新增确诊',
  `suspect` int DEFAULT NULL COMMENT '剩余疑似',
  `suspect_add` int DEFAULT NULL COMMENT '当日新增疑似',
  `heal` int DEFAULT NULL COMMENT '累计治愈',
  `heal_add` int DEFAULT NULL COMMENT '当日新增治愈',
  `dead` int DEFAULT NULL COMMENT '累计死亡',
  `dead_add` int DEFAULT NULL COMMENT '当日新增死亡',
  PRIMARY KEY (`ds`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `hotsearch` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dt` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `content` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;


