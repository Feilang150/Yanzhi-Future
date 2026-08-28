-- Yanzhi-Future 数据库初始化脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS yanzhi_future DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE yanzhi_future;

-- 用户表
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `openid` varchar(64) DEFAULT NULL COMMENT '微信openid',
  `nickname` varchar(50) DEFAULT NULL COMMENT '用户昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `gender` tinyint(1) DEFAULT '0' COMMENT '性别：0-未知，1-男，2-女',
  `age` int(3) DEFAULT NULL COMMENT '年龄',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `preferences` text COMMENT '用户偏好设置（JSON格式）',
  `status` tinyint(1) DEFAULT '0' COMMENT '账号状态：0-正常，1-禁用',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除标记：0-未删除，1-已删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_openid` (`openid`),
  KEY `idx_phone` (`phone`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 场景表
CREATE TABLE `scenario` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '场景ID',
  `name` varchar(100) NOT NULL COMMENT '场景名称',
  `description` varchar(500) DEFAULT NULL COMMENT '场景描述',
  `type` tinyint(1) DEFAULT '0' COMMENT '场景类型：0-预设，1-自定义',
  `icon` varchar(50) DEFAULT NULL COMMENT '场景图标',
  `difficulty` tinyint(1) DEFAULT '1' COMMENT '难度级别：1-简单，2-中等，3-困难',
  `duration` int(3) DEFAULT NULL COMMENT '预计时长（分钟）',
  `category` varchar(50) DEFAULT NULL COMMENT '分类标签',
  `keywords` text COMMENT '核心词汇（JSON数组）',
  `background` text COMMENT '背景描述',
  `creator_id` bigint(20) DEFAULT NULL COMMENT '创建者ID（自定义场景）',
  `usage_count` int(11) DEFAULT '0' COMMENT '使用次数',
  `rating` decimal(2,1) DEFAULT NULL COMMENT '评分（1-5星）',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除标记：0-未删除，1-已删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_type` (`type`),
  KEY `idx_creator` (`creator_id`),
  KEY `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='场景表';

-- 训练记录表
CREATE TABLE `training_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '训练ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `scenario_id` bigint(20) DEFAULT NULL COMMENT '场景ID',
  `status` tinyint(1) DEFAULT '0' COMMENT '训练状态：0-进行中，1-已完成，2-已中断',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `duration` int(11) DEFAULT NULL COMMENT '训练时长（秒）',
  `dialogue_count` int(11) DEFAULT '0' COMMENT '对话次数',
  `overall_score` decimal(5,2) DEFAULT NULL COMMENT '综合得分',
  `pronunciation_score` decimal(5,2) DEFAULT NULL COMMENT '发音得分',
  `grammar_score` decimal(5,2) DEFAULT NULL COMMENT '语法得分',
  `fluency_score` decimal(5,2) DEFAULT NULL COMMENT '流利度得分',
  `vocabulary_score` decimal(5,2) DEFAULT NULL COMMENT '词汇丰富度得分',
  `logic_score` decimal(5,2) DEFAULT NULL COMMENT '逻辑连贯性得分',
  `report_id` varchar(64) DEFAULT NULL COMMENT '训练报告（MongoDB文档ID）',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除标记：0-未删除，1-已删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_scenario_id` (`scenario_id`),
  KEY `idx_status` (`status`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='训练记录表';

-- 翻译记录表
CREATE TABLE `translation_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '翻译ID',
  `user_id` bigint(20) DEFAULT NULL COMMENT '用户ID',
  `source_language` varchar(10) DEFAULT NULL COMMENT '源语言',
  `target_language` varchar(10) DEFAULT NULL COMMENT '目标语言',
  `original_text` text COMMENT '原始文本',
  `translated_text` text COMMENT '翻译文本',
  `audio_url` varchar(255) DEFAULT NULL COMMENT '音频URL',
  `output_mode` varchar(20) DEFAULT 'subtitle' COMMENT '输出模式：subtitle-字幕，voice-语音，both-双模式',
  `duration` int(11) DEFAULT NULL COMMENT '翻译时长（毫秒）',
  `quality_score` decimal(5,2) DEFAULT NULL COMMENT '质量评分',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除标记：0-未删除，1-已删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_languages` (`source_language`, `target_language`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='翻译记录表';

-- 剧本表
CREATE TABLE `script` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '剧本ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `title` varchar(100) NOT NULL COMMENT '剧本标题',
  `author` varchar(50) DEFAULT NULL COMMENT '作者',
  `version` varchar(20) DEFAULT '1.0' COMMENT '版本号',
  `genre` varchar(50) DEFAULT NULL COMMENT '剧本类型',
  `synopsis` text COMMENT '剧本梗概',
  `content` longtext COMMENT '剧本内容（YAML格式）',
  `character_count` int(11) DEFAULT '0' COMMENT '人物数量',
  `scene_count` int(11) DEFAULT '0' COMMENT '场景数量',
  `word_count` int(11) DEFAULT '0' COMMENT '字数统计',
  `novel_text_id` varchar(64) DEFAULT NULL COMMENT '小说原文ID（MongoDB）',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除标记：0-未删除，1-已删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_genre` (`genre`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='剧本表';

-- 翻译纠错表
CREATE TABLE `translation_correction` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '纠错ID',
  `user_id` bigint(20) DEFAULT NULL COMMENT '用户ID',
  `translation_id` bigint(20) DEFAULT NULL COMMENT '翻译记录ID',
  `error_position` varchar(50) DEFAULT NULL COMMENT '错误位置',
  `error_content` text COMMENT '错误内容',
  `correct_content` text COMMENT '正确内容',
  `error_type` varchar(50) DEFAULT 'translation' COMMENT '错误类型',
  `status` tinyint(1) DEFAULT '0' COMMENT '处理状态：0-待处理，1-已处理',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除标记：0-未删除，1-已删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_translation_id` (`translation_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='翻译纠错表';

-- 插入初始数据
INSERT INTO `scenario` (`name`, `description`, `type`, `icon`, `difficulty`, `duration`, `category`, `keywords`, `background`) VALUES
('面试英语', '模拟真实的职场面试场景，提升求职竞争力', 0, '💼', 2, 15, '职场', '["interview", "resume", "experience", "skills"]', '你正在参加一家心仪公司的面试，HR正在询问你的工作经验和技能。'),
('餐厅点餐', '模拟餐厅点餐场景，练习日常英语对话', 0, '🍽️', 1, 10, '日常', '["order", "menu", "recommend", "delicious"]', '你在一家西餐厅，服务员来为你点餐。'),
('商务会议', '模拟商务会议场景，提升职场英语沟通能力', 0, '📊', 3, 20, '职场', '["meeting", "presentation", "project", "deadline"]', '你正在主持一个重要的项目会议，需要向团队汇报进展并讨论问题。'),
('机场问询', '模拟机场问询场景，练习旅行英语', 0, '✈️', 1, 10, '旅行', '["flight", "check-in", "boarding", "luggage"]', '你在机场，需要咨询航班信息和办理值机手续。'),
('酒店入住', '模拟酒店入住场景，练习住宿相关英语', 0, '🏨', 1, 10, '旅行', '["check-in", "room", "reservation", "key"]', '你到达预订的酒店，需要办理入住手续。');

-- 创建索引优化查询性能
CREATE INDEX idx_training_user_time ON training_record(user_id, create_time);
CREATE INDEX idx_translation_user_time ON translation_record(user_id, create_time);
CREATE INDEX idx_script_user_time ON script(user_id, create_time);