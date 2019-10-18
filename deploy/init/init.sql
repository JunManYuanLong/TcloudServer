SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
CREATE DATABASE demo;
use demo;
-- ----------------------------
-- Table structure for ability
-- ----------------------------
DROP TABLE IF EXISTS `ability`;
CREATE TABLE `ability` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `handler` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ability
-- ----------------------------
BEGIN;
INSERT INTO `ability` VALUES (1, NULL, '2019-08-21 14:00:08', '访问_资产', 'asset_view');
INSERT INTO `ability` VALUES (2, NULL, '2019-08-21 14:00:09', '编辑_资产', 'asset_modify');
INSERT INTO `ability` VALUES (3, NULL, '2019-08-21 14:00:11', '删除_资产', 'asset_delete');
INSERT INTO `ability` VALUES (4, NULL, '2019-08-21 14:00:12', '访问_项目', 'project_view');
INSERT INTO `ability` VALUES (5, NULL, '2019-08-21 14:00:13', '编辑_项目', 'project_modify');
INSERT INTO `ability` VALUES (6, NULL, '2019-08-21 14:00:15', '删除_项目', 'project_delete');
INSERT INTO `ability` VALUES (7, NULL, '2019-08-21 14:00:18', '访问_模块', 'module_view');
INSERT INTO `ability` VALUES (8, NULL, '2019-08-21 14:00:19', '编辑_模块', 'module_modify');
INSERT INTO `ability` VALUES (9, NULL, '2019-08-21 14:00:21', '删除_模块', 'module_delete');
INSERT INTO `ability` VALUES (10, NULL, '2019-08-21 14:00:23', '访问_版本', 'version_view');
INSERT INTO `ability` VALUES (11, NULL, '2019-08-21 14:00:25', '编辑_版本', 'version_modify');
INSERT INTO `ability` VALUES (12, NULL, '2019-08-21 14:00:26', '删除_版本', 'version_delete');
INSERT INTO `ability` VALUES (13, NULL, '2019-08-21 14:00:27', '访问_需求', 'requirement_view');
INSERT INTO `ability` VALUES (14, NULL, '2019-08-21 14:00:28', '编辑_需求', 'requirement_modify');
INSERT INTO `ability` VALUES (15, NULL, '2019-08-21 14:00:31', '删除_需求', 'requirement_delete');
INSERT INTO `ability` VALUES (16, NULL, '2019-08-21 14:00:32', '访问_用例', 'case_view');
INSERT INTO `ability` VALUES (17, NULL, '2019-08-21 14:00:35', '编辑_用例', 'case_modify');
INSERT INTO `ability` VALUES (18, NULL, '2019-08-21 14:00:37', '删除_用例', 'case_delete');
INSERT INTO `ability` VALUES (19, NULL, '2019-08-21 14:00:39', '访问_任务', 'task_view');
INSERT INTO `ability` VALUES (20, NULL, '2019-08-21 14:00:40', '编辑_任务', 'task_modify');
INSERT INTO `ability` VALUES (21, NULL, '2019-08-21 14:00:43', '删除_任务', 'task_delete');
INSERT INTO `ability` VALUES (22, NULL, '2019-08-21 14:00:44', '访问_缺陷', 'issue_view');
INSERT INTO `ability` VALUES (23, NULL, '2019-08-21 14:00:45', '编辑_缺陷', 'issue_modify');
INSERT INTO `ability` VALUES (24, NULL, '2019-08-21 14:00:49', '删除_缺陷', 'issue_delete');
INSERT INTO `ability` VALUES (25, NULL, '2019-08-21 14:00:50', '访问_流程', 'flow_view');
INSERT INTO `ability` VALUES (26, NULL, '2019-08-21 14:00:51', '编辑_流程', 'flow_modify');
INSERT INTO `ability` VALUES (27, NULL, '2019-08-21 14:00:53', '删除_流程', 'flow_delete');
INSERT INTO `ability` VALUES (28, NULL, '2019-08-21 14:00:54', '访问_配置', 'projectconfig_view');
INSERT INTO `ability` VALUES (29, NULL, '2019-08-21 14:00:56', '编辑_配置', 'projectconfig_modify');
INSERT INTO `ability` VALUES (30, NULL, '2019-08-21 14:00:58', '删除_配置', 'projectconfig_delete');
INSERT INTO `ability` VALUES (31, NULL, '2019-08-21 14:01:00', '执行_用例', 'case_excute');
INSERT INTO `ability` VALUES (32, NULL, '2019-09-24 16:27:56', '编辑_标签', 'tag_modify');
INSERT INTO `ability` VALUES (33, NULL, '2019-09-24 16:28:16', '删除_标签', 'tag_delete');
INSERT INTO `ability` VALUES (34, NULL, '2019-09-24 16:28:34', '访问_标签', 'tag_view');
COMMIT;


-- ----------------------------
-- Table structure for board_config
-- ----------------------------
DROP TABLE IF EXISTS `board_config`;
CREATE TABLE `board_config` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `issue` varchar(20) DEFAULT NULL,
  `requirement` varchar(20) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NULL DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `project_id` varchar(20) NOT NULL DEFAULT '',
  `hasconfig` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for case
-- ----------------------------
DROP TABLE IF EXISTS `case`;
CREATE TABLE `case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cnumber` varchar(100) DEFAULT NULL,
  `module_id` int(11) DEFAULT NULL,
  `ctype` varchar(10) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `title` varchar(300) DEFAULT NULL,
  `precondition` text,
  `step_result` text,
  `is_auto` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `requirement_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for ci_data
-- ----------------------------
DROP TABLE IF EXISTS `ci_data`;
CREATE TABLE `ci_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(200) DEFAULT NULL,
  `accuracy` varchar(10) DEFAULT NULL,
  `case_count` int(11) DEFAULT NULL,
  `nextBuildNumber` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ci_job
-- ----------------------------
DROP TABLE IF EXISTS `ci_job`;
CREATE TABLE `ci_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `number` int(11) DEFAULT NULL,
  `url` varchar(300) DEFAULT NULL,
  `ci_id` int(11) DEFAULT NULL,
  `start_name` varchar(300) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `report` varchar(300) DEFAULT NULL,
  `run_date` timestamp NULL DEFAULT NULL,
  `run_time` varchar(300) DEFAULT NULL,
  `job_count` int(11) DEFAULT NULL,
  `job_accuracy` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for company
-- ----------------------------
DROP TABLE IF EXISTS `company`;
CREATE TABLE `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `corporation` varchar(100) DEFAULT NULL,
  `tax` varchar(30) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `module` varchar(100) DEFAULT NULL,
  `module_type` int(11) DEFAULT NULL,
  `content` text,
  `description` text,
  `projectid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of config
-- ----------------------------
BEGIN;
INSERT INTO `config` VALUES (1, '2019-01-23 14:19:56', '2019-09-06 12:57:16', 'issue', 1, '{\"operation_dict\":{\"requirement_id\":\"需求\",\"attach\":\"附件\",\"chance\":\"BUG出现机率\",\"comment\":\"备注\",\"description\":\"描述\",\"handle_status\":\"处理状态\",\"handler_name\":\"处理人\",\"issue_type\":\"BUG类型\",\"level\":\"BUG级别\",\"module_name\":\"模块\",\"priority\":\"优先级\",\"status\":\"状态\",\"title\":\"标题\",\"system\":\"所属系统\",\"detection_chance\":\"用户识别度\"},\"chance\":{\"0\":\"必现\",\"1\":\"大概率\",\"2\":\"小概率\",\"3\":\"极小概率\",\"\":\"\"},\"issue_type\":{\"0\":\"功能问题\",\"1\":\"界面优化\",\"2\":\"设计缺陷\",\"3\":\"安全相关\",\"4\":\"性能问题\",\"5\":\"开发修改引入\",\"6\":\"其他\",\"\":\"\"},\"level\":{\"0\":\"阻塞\",\"1\":\"严重\",\"2\":\"重要\",\"3\":\"次要\",\"4\":\"微小\",\"\":\"\"},\"priority\":{\"0\":\"紧急\",\"1\":\"高\",\"2\":\"中\",\"3\":\"低\",\"\":\"\"},\"handle_status\":{\"1\":\"待办\",\"2\":\"处理中\",\"3\":\"测试中\",\"4\":\"已关闭\",\"5\":\"已拒绝\",\"6\":\"延时处理\",\"\":\"\"},\"system\":{\"1\":\"ANDROID\",\"2\":\"IOS\",\"3\":\"后端\",\"4\":\"H5\",\"5\":\"小程序\",\"6\":\"WEB端\",\"7\":\"其他\",\"\":\"\"},\"detection_chance\":{\"0\":\"明显的\",\"1\":\"高概率\",\"2\":\"中概率\",\"3\":\"小概率\",\"\":\"\"}}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (2, '2019-01-23 14:19:56', '2019-01-23 14:19:58', 'board', 1, '{\"create\":{\"task\":[0,1,2],\"task_case\":[],\"issue\":[1,2,3,4,5,6]},\"unfinish\":{\"task\":[0],\"task_case\":[0],\"issue\":[1,2,3,5,6]},\"finish\":{\"task\":[2],\"task_case\":[2,3,4],\"issue\":[4]}}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (3, '2019-01-23 14:19:56', '2019-06-24 19:10:34', 'requirement', 1, '{\"operation_dict\":{\"attach\":\"附件\",\"comment\":\"备注\",\"description\":\"描述\",\"board_status\":\"处理状态\",\"handler_name\":\"处理人\",\"requirement_type\":\"类型\",\"priority\":\"优先级\",\"status\":\"状态\",\"title\":\"标题\",\"review_status\":\"评审状态\",\"worth\":\"需求价值\",\"worth_sure\":\"需求价值确认\",\"jira_id\":\"jira号\",\"report_time\":\"需获取置信结果天数\",\"report_expect\":\"高价值预期结果\",\"report_real\":\"高价值实际结果\"},\"requirement_type\":{\"0\":\"功能需求\",\"1\":\"优化需求\",\"2\":\"自动化需求\",\"3\":\"性能需求\",\"4\":\"兼容性需求\",\"5\":\"报表需求\",\"6\":\"临时需求\",\"7\":\"紧急需求\",\"8\":\"新功能需求\",\"9\":\"其他\",\"\":\"\"},\"priority\":{\"0\":\"紧急\",\"1\":\"高\",\"2\":\"中\",\"3\":\"低\",\"\":\"\"},\"board_status\":{\"0\":\"规划中\",\"1\":\"实现中\",\"2\":\"测试中\",\"3\":\"已拒绝\",\"4\":\"待验收\",\"5\":\"待发布\",\"6\":\"完成\",\"\":\"\"},\"review_status\":{\"1\":\"未评审\",\"2\":\"评审成功\",\"3\":\"评审失败\",\"\":\"\"},\"worth_sure\":{\"1\":\"超出预期\",\"2\":\"符合预期\",\"3\":\"低于预期\",\"\":\"\"},\"worth\":{\"1\":\"高价值\",\"2\":\"非高价值\",\"\":\"\"}}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (4, '2019-01-23 14:19:56', '2019-09-25 16:52:47', 'issue', 2, '{\"test\":[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[1,2],[3,2],[3,4],[3,6],[4,2],[5,2],[5,4],[6,2],[6,4]],\"dev\":[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[1,2],[2,3],[2,5],[2,6]],\"admin\":[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[1,2],[2,3],[2,5],[2,6],[3,2],[3,4],[4,2],[5,2],[5,4],[6,2],[6,4]]}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (5, '2019-01-23 14:19:56', '2019-09-27 15:45:36', 'access_token', 1, '{\"access_token\": \"youraccesstoken\"}', NULL, 0);
INSERT INTO `config` VALUES (6, '2019-04-03 10:41:22', '2019-06-14 13:57:29', 'stf', 1, '{\"URL\":\"http://yourstfurl\",\"headers\":{\"Authorization\": \"yourtoken\"}}', NULL, NULL);
INSERT INTO `config` VALUES (7, '2019-04-12 13:47:51', '2019-04-12 13:52:29', 'corp_secret', 1, 'yourcorpsecret', NULL, NULL);
INSERT INTO `config` VALUES (8, '2019-04-28 16:27:46', '2019-09-27 11:21:47', 'stf', 2, '{\"URL\":\"http://yourstfurl\", \"stfurl\":\"http://yourstfurl\"}', NULL, NULL);
INSERT INTO `config` VALUES (9, '2019-05-05 15:53:04', '2019-06-24 12:39:36', 'stf', 3, '{\"URL\":\"http://yourstfurl\",\"headers\":{\"Authorization\": \"yourtoken\"}}', NULL, NULL);
INSERT INTO `config` VALUES (10, NULL, '2019-06-20 14:14:25', 'tcloud', 1, 'http://tcloud-demo.innotechx.com/#', NULL, NULL);
INSERT INTO `config` VALUES (15, NULL, '2019-06-20 14:14:17', 'tcloud', 2, 'http://tcloud-demo.innotechx.com/#', NULL, NULL);
INSERT INTO `config` VALUES (16, '2019-05-24 17:54:08', '2019-07-26 16:35:33', 'jenkins', 1, '{\"4\":[{\"id\":0,\"name\":\"回归测试\",\"job\":\"regression_test\"},{\"id\":1,\"name\":\"回归测试\",\"job\":\"regression_test\"},{\"id\":2,\"name\":\"单个接口\",\"job\":\"singel_api_dev\"}],\"1\":[{\"id\":1,\"name\":\"回归测试\",\"job\":\"regression_test\"}]}', NULL, NULL);
INSERT INTO `config` VALUES (17, '2019-05-24 20:10:50', '2019-07-22 10:43:34', 'jenkins', 2, '{\"url\":\"http://ci.xx.com\",\"user_id\":\"aaa\",\"api_token\":\"yourtoken\"}', 'jenkins 账号信息', NULL);
INSERT INTO `config` VALUES (18, '2019-06-14 11:19:56', '2019-06-13 18:59:35', 'asset', 1, '{\"operation_dict\":{\"name\":\"名称\",\"asset_id\":\"资产编号\",\"status\":\"状态\",\"borrow_id\":\"持有者\"},\"status\":{\"0\":\"不可用\",\"1\":\"可用\"}}', '资产的转移记录', NULL);
INSERT INTO `config` VALUES (19, '2019-06-14 14:19:56', '2019-06-14 14:08:15', 'credit', 1, '{\"operation_dict\":{\"score\": \"信用积分\"},\"status\":{\"0\":\"不可用\",\"1\":\"可用\"}}', '信用积分记录', NULL);
INSERT INTO `config` VALUES (20, '2019-06-17 19:43:09', '2019-07-02 14:27:40', 'deploy', 1, '{\"operation_dict\":[{\"4\":\"4\"},{\"1\":\"4\"}]}', NULL, NULL);
INSERT INTO `config` VALUES (22, '2019-06-21 15:49:01', '2019-07-02 22:40:30', 'track', 1, '{\"operation_dict\":[{\"1\":\"3\"},{\"2\":\"42\"},{\"3\":\"41\"},{\"4\":\"43\"},{\"63\":\"45\"}]}', '埋点项目配置', NULL);
INSERT INTO `config` VALUES (23, '2019-06-21 16:05:34', '2019-07-02 22:40:09', 'track', 2, '{\"URL\":\"http://yourtrackurl\"}', '埋点项目url', NULL);
INSERT INTO `config` VALUES (24, '2019-06-26 23:08:57', '2019-07-02 22:40:19', 'track', 3, '{\"URL\":\"ws://yourtrackurl\"}', '埋点项目websocket', NULL);
INSERT INTO `config` VALUES (25, '2019-07-01 16:11:16', '2019-07-02 21:41:32', 'deploy', 2, '{\"URL\":\"http://yourdeployurl\"}', '部署url', NULL);
INSERT INTO `config` VALUES (26, '2019-07-01 16:12:13', '2019-07-02 14:27:30', 'deploy', 3, '{\"api\":\"yourapi\"}', '部署token', NULL);
INSERT INTO `config` VALUES (27, '2019-07-22 10:44:01', '2019-07-22 19:12:27', 'jenkins', 3, '{\"job\":[\"activity_api\",\"regression_test\",\"scene_api\",\"activity_api\",\"scene_api\"]}', 'jenkins更新的job', NULL);
INSERT INTO `config` VALUES (28, '2019-07-29 16:30:15', '2019-08-13 10:41:26', 'flow_config', NULL, '{\"type\":{\"1\":\"版本需求\",\"2\":\"搜索推荐\",\"3\":\"问题修复\",\"4\":\"临时需求\",\"5\":\"优化\",\"6\":\"紧急需求\"},\"platform\":{\"1\":\"后端\",\"2\":\"PHP\",\"3\":\"APP\",\"4\":\"H5\",\"5\":\"微信商城\",\"6\":\"小程序\"},\"permission_check\":true}', '默认的流程配置', 0);
INSERT INTO `config` VALUES (29, '2019-08-19 16:55:16', '2019-08-30 14:43:55', 'flow_config', NULL, '{\"type\": {\"1\": \"\\u7248\\u672c\\u9700\\u6c42\", \"2\": \"\\u641c\\u7d22\\u63a8\\u8350\", \"3\": \"\\u95ee\\u9898\\u4fee\\u590d\", \"4\": \"\\u4e34\\u65f6\\u9700\\u6c42\", \"5\": \"\\u4f18\\u5316\", \"6\": \"\\u7d27\\u6025\\u9700\\u6c42\"}, \"platform\": {\"1\": \"\\u540e\\u7aef\", \"2\": \"PHP\", \"3\": \"APP\", \"4\": \"H5\", \"5\": \"\\u5fae\\u4fe1\\u5546\\u57ce\", \"6\": \"\\u5c0f\\u7a0b\\u5e8f\"}, \"permission_check\": true}', '默认的流程配置', 4);
INSERT INTO `config` VALUES (30, '2019-09-04 07:00:30', '2019-09-04 15:00:30', 'flow_config', NULL, '{\"type\": {\"1\": \"\\u7248\\u672c\\u9700\\u6c42\", \"2\": \"\\u641c\\u7d22\\u63a8\\u8350\", \"3\": \"\\u95ee\\u9898\\u4fee\\u590d\", \"4\": \"\\u4e34\\u65f6\\u9700\\u6c42\", \"5\": \"\\u4f18\\u5316\", \"6\": \"\\u7d27\\u6025\\u9700\\u6c42\"}, \"platform\": {\"1\": \"\\u540e\\u7aef\", \"2\": \"PHP\", \"3\": \"APP\", \"4\": \"H5\", \"5\": \"\\u5fae\\u4fe1\\u5546\\u57ce\", \"6\": \"\\u5c0f\\u7a0b\\u5e8f\"}, \"permission_check\": false}', '默认的流程配置', 2);
COMMIT;

-- ----------------------------
-- Table structure for content
-- ----------------------------
DROP TABLE IF EXISTS `content`;
CREATE TABLE `content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `send_id` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `group` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for credit
-- ----------------------------
DROP TABLE IF EXISTS `credit`;
CREATE TABLE `credit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for credit_record
-- ----------------------------
DROP TABLE IF EXISTS `credit_record`;
CREATE TABLE `credit_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `score_operation` int(11) DEFAULT NULL,
  `reason` varchar(1000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for data_show_fields
-- ----------------------------
DROP TABLE IF EXISTS `data_show_fields`;
CREATE TABLE `data_show_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_type` int(11) DEFAULT NULL,
  `data_value` varchar(255) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for data_show_first_page_first_word_correct_rate
-- ----------------------------
DROP TABLE IF EXISTS `data_show_first_page_first_word_correct_rate`;
CREATE TABLE `data_show_first_page_first_word_correct_rate` (
  `data_source` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_model` varchar(255) DEFAULT NULL,
  `apk_version` varchar(255) DEFAULT NULL,
  `kernel_version` varchar(255) DEFAULT NULL,
  `system_version` varchar(255) DEFAULT NULL,
  `thesaurus_version` varchar(255) DEFAULT NULL,
  `corpus_version` varchar(255) DEFAULT NULL,
  `key_9_and_26` varchar(255) DEFAULT NULL,
  `first_word_correct_rate` varchar(255) DEFAULT NULL,
  `first_page_correct_rate` varchar(255) DEFAULT NULL,
  `creator` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  `show_in_chart` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for data_show_response_kernel_record
-- ----------------------------
DROP TABLE IF EXISTS `data_show_response_kernel_record`;
CREATE TABLE `data_show_response_kernel_record` (
  `data_source` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_model` varchar(255) DEFAULT NULL,
  `apk_version` varchar(255) DEFAULT NULL,
  `kernel_version` varchar(255) DEFAULT NULL,
  `system_version` varchar(255) DEFAULT NULL,
  `thesaurus_version` varchar(255) DEFAULT NULL,
  `corpus_version` varchar(255) DEFAULT NULL,
  `key_9_and_26` varchar(255) DEFAULT NULL,
  `average` varchar(255) DEFAULT NULL,
  `line_90_percent` varchar(255) DEFAULT NULL,
  `line_95_percent` varchar(255) DEFAULT NULL,
  `creator` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  `status` int(255) DEFAULT '0',
  `show_in_chart` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for data_show_response_log
-- ----------------------------
DROP TABLE IF EXISTS `data_show_response_log`;
CREATE TABLE `data_show_response_log` (
  `data_source` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_model` varchar(255) DEFAULT NULL,
  `apk_version` varchar(255) DEFAULT NULL,
  `kernel_version` varchar(255) DEFAULT NULL,
  `system_version` varchar(255) DEFAULT NULL,
  `thesaurus_version` varchar(255) DEFAULT NULL,
  `corpus_version` varchar(255) DEFAULT NULL,
  `key_9_kernel_click_time_average` varchar(255) DEFAULT NULL,
  `key_26_kernel_click_time_average` varchar(255) DEFAULT NULL,
  `key_9_kernel_response_time` varchar(255) DEFAULT NULL,
  `key_26_kernel_response_time` varchar(255) DEFAULT NULL,
  `cpu_average` varchar(255) DEFAULT NULL,
  `ram_average` varchar(255) DEFAULT NULL,
  `battery_use` varchar(255) DEFAULT NULL,
  `creator` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  `status` int(255) DEFAULT '0',
  `show_in_chart` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for deploy
-- ----------------------------
DROP TABLE IF EXISTS `deploy`;
CREATE TABLE `deploy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_id` int(11) DEFAULT NULL,
  `server_list` varchar(500) DEFAULT NULL,
  `node_list` varchar(500) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `branch` varchar(500) DEFAULT NULL,
  `flow_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for deploy_log
-- ----------------------------
DROP TABLE IF EXISTS `deploy_log`;
CREATE TABLE `deploy_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_id` int(11) DEFAULT NULL,
  `comment` text,
  `flow_id` int(11) DEFAULT NULL,
  `result` varchar(500) DEFAULT NULL,
  `name` varchar(500) DEFAULT NULL,
  `use_id` int(11) DEFAULT NULL,
  `deploy_id` int(11) DEFAULT NULL,
  `user_name` varchar(500) DEFAULT NULL,
  `result_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `log_type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for deploy_record
-- ----------------------------
DROP TABLE IF EXISTS `deploy_record`;
CREATE TABLE `deploy_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_id` int(11) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `node_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `version` varchar(100) DEFAULT NULL,
  `branch` varchar(100) DEFAULT NULL,
  `result` int(11) DEFAULT NULL,
  `deploy_id` int(11) DEFAULT NULL,
  `flow_id` int(11) DEFAULT NULL,
  `server_name` varchar(500) DEFAULT NULL,
  `node_name` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for displayer
-- ----------------------------
DROP TABLE IF EXISTS `displayer`;
CREATE TABLE `displayer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `asset_id` varchar(100) DEFAULT NULL,
  `vendor` varchar(100) DEFAULT NULL,
  `resolution` varchar(100) DEFAULT NULL,
  `buy_date` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for feature
-- ----------------------------
DROP TABLE IF EXISTS `feature`;
CREATE TABLE `feature` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `module_id` int(11) NOT NULL,
  `description` text,
  `weight` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for feedback
-- ----------------------------
DROP TABLE IF EXISTS `feedback`;
CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `contact` varchar(200) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `comment` text,
  `weight` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for flow_assemble
-- ----------------------------
DROP TABLE IF EXISTS `flow_assemble`;
CREATE TABLE `flow_assemble` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `flow_base_list` varchar(300) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `flow_asstype` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `comment` text,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of flow_assemble
-- ----------------------------
BEGIN;
INSERT INTO `flow_assemble` VALUES (1, '2019-05-14 14:46:11', '2019-05-22 17:45:17', '客户端', '3,4,5,8,9,10,13,14,15,16', 0, 1, 1, NULL, 1);
INSERT INTO `flow_assemble` VALUES (2, '2019-05-14 14:46:11', '2019-05-22 17:45:19', 'H5&服务端', '3,4,5,6,8,9,11,13,14,16', 0, 1, 1, NULL, NULL);
INSERT INTO `flow_assemble` VALUES (3, '2019-05-14 14:46:11', '2019-05-22 17:45:21', 'SkipTest', '2,6,7,11,12,16', 0, 1, 1, NULL, NULL);
INSERT INTO `flow_assemble` VALUES (4, '2019-05-14 14:46:11', '2019-05-22 17:45:22', 'HotFix', '2,7,11,12,16', 0, 1, 1, NULL, NULL);
INSERT INTO `flow_assemble` VALUES (5, '2019-07-10 17:38:54', '2019-07-11 19:06:41', 'HotFix（需QA验证）', '2,4,7,11,12,16', 0, 1, 1, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for flow_base
-- ----------------------------
DROP TABLE IF EXISTS `flow_base`;
CREATE TABLE `flow_base` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `step` varchar(300) DEFAULT NULL,
  `comment` text,
  `notice_type` int(11) DEFAULT NULL,
  `is_send` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of flow_base
-- ----------------------------
BEGIN;
INSERT INTO `flow_base` VALUES (1, '2019-05-14 14:43:49', '2019-06-06 14:57:55', '分支开发', '[{\"2\":\"不通过\"},{\"1\":\"通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_dev\",\"user_test\",\"user_prod\",\"user_owner\"],\"2\":[\"user_dev\",\"user_test\",\"user_prod\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 0);
INSERT INTO `flow_base` VALUES (2, '2019-05-14 14:43:49', '2019-06-06 14:57:55', '开发自测', '[{\"6\":\"备注\"},{\"1\":\"通过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"6\":[\"user_dev\",\"user_owner\"]}', 1, 0);
INSERT INTO `flow_base` VALUES (3, '2019-05-14 14:43:49', '2019-06-06 14:57:55', '提测', '[{\"6\":\"备注\"},{\"4\":\"部署\"},{\"1\":\"通过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"4\":[\"user_dev\",\"user_owner\"],\"6\":[\"user_dev\",\"user_owner\"]}', 1, 0);
INSERT INTO `flow_base` VALUES (4, '2019-05-14 14:43:49', '2019-06-06 14:58:51', '功能测试', '[{\"5\":\"自动化测试\"},{\"1\":\"通过\"},{\"2\":\"不通过\"}]', '{\"1\":[\"user_test\",\"user_owner\"],\"2\":[\"user_test\",\"user_owner\"],\"5\":[\"user_test\",\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (5, '2019-05-14 14:43:49', '2019-06-06 16:28:48', 'PM验收', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_prod\",\"user_owner\"],\"2\":[\"user_prod\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (6, '2019-05-14 14:43:49', '2019-06-06 16:33:37', '预发布上线', '[{\"6\":\"备注\"},{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"2\":[\"user_dev\",\"user_owner\"],\"3\":[\"user_owner\"],\"6\":[\"user_dev\",\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (7, '2019-05-14 14:43:49', '2019-06-06 14:59:07', '预发布验证', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"2\":[\"user_dev\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (8, '2019-05-14 14:43:49', '2019-06-06 14:59:09', 'QA预发布验证', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_test\",\"user_owner\"],\"2\":[\"user_test\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (9, '2019-05-14 14:43:49', '2019-06-06 14:59:17', 'PM预发布验证', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_prod\",\"user_owner\"],\"2\":[\"user_prod\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (10, '2019-05-14 14:43:49', '2019-06-06 14:57:55', '灰度发包', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"2\":[\"user_dev\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 0);
INSERT INTO `flow_base` VALUES (11, '2019-05-14 14:43:49', '2019-06-06 16:33:42', '正式上线', '[{\"6\":\"备注\"},{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"2\":[\"user_dev\",\"user_owner\"],\"3\":[\"user_owner\"],\"6\":[\"user_dev\",\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (12, '2019-05-14 14:43:49', '2019-06-06 14:59:23', '线上验证', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"2\":[\"user_dev\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (13, '2019-05-14 14:43:49', '2019-06-06 14:59:21', 'QA线上验证', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_test\",\"user_owner\"],\"2\":[\"user_test\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (14, '2019-05-14 14:43:49', '2019-06-06 14:59:20', 'PM线上验证', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_prod\",\"user_owner\"],\"2\":[\"user_prod\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 1);
INSERT INTO `flow_base` VALUES (15, '2019-05-14 14:43:49', '2019-06-06 14:57:55', '全量发包', '[{\"1\":\"通过\"},{\"2\":\"不通过\"},{\"3\":\"跳过\"}]', '{\"1\":[\"user_dev\",\"user_owner\"],\"2\":[\"user_dev\",\"user_owner\"],\"3\":[\"user_owner\"]}', 1, 0);
INSERT INTO `flow_base` VALUES (16, '2019-05-15 16:45:10', '2019-06-06 14:57:55', '完成', '[{\"1\":\"通过\"}]', '{\"1\":[\"user_dev\",\"user_test\",\"user_prod\",\"user_owner\"]}', 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for flow_info
-- ----------------------------
DROP TABLE IF EXISTS `flow_info`;
CREATE TABLE `flow_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `flow_type` int(11) DEFAULT NULL,
  `requirement_list` varchar(300) DEFAULT NULL,
  `flow_assemble_id` int(11) DEFAULT NULL,
  `flow_base_list` varchar(300) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `start_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `version_id` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `user_dev` varchar(300) DEFAULT NULL,
  `user_prod` varchar(300) DEFAULT NULL,
  `user_test` varchar(300) DEFAULT NULL,
  `user_owner` varchar(300) DEFAULT NULL,
  `action` text,
  `status` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `comment` text,
  `platform` varchar(300) DEFAULT NULL,
  `dependence` text,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for flow_record
-- ----------------------------
DROP TABLE IF EXISTS `flow_record`;
CREATE TABLE `flow_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `flow_info_id` int(11) DEFAULT NULL,
  `flow_type` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `step_id` int(11) DEFAULT NULL,
  `next_step_id` int(11) DEFAULT NULL,
  `result` varchar(300) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `version_id` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for flow_source
-- ----------------------------
DROP TABLE IF EXISTS `flow_source`;
CREATE TABLE `flow_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_id` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `user_ids` varchar(300) DEFAULT NULL,
  `source_type` int(11) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for guest
-- ----------------------------
DROP TABLE IF EXISTS `guest`;
CREATE TABLE `guest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(30) DEFAULT NULL,
  `platform` varchar(30) DEFAULT NULL,
  `browser` varchar(30) DEFAULT NULL,
  `version` varchar(30) DEFAULT NULL,
  `string` text,
  `count` int(11) DEFAULT '1',
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for interface_api_msg
-- ----------------------------
DROP TABLE IF EXISTS `interface_api_msg`;
CREATE TABLE `interface_api_msg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `num` int(11) DEFAULT NULL COMMENT '接口序号',
  `name` varchar(128) DEFAULT NULL COMMENT '接口名称',
  `desc` varchar(256) DEFAULT NULL COMMENT '接口描述',
  `variable_type` varchar(32) DEFAULT NULL COMMENT '参数类型选择',
  `status_url` varchar(32) DEFAULT NULL COMMENT '基础url,序号对应项目的环境',
  `up_func` varchar(128) DEFAULT NULL COMMENT '接口执行前的函数',
  `down_func` varchar(128) DEFAULT NULL COMMENT '接口执行后的函数',
  `method` varchar(32) DEFAULT NULL COMMENT '请求方式',
  `variable` text COMMENT 'form-data形式的参数',
  `json_variable` text COMMENT 'json形式的参数',
  `param` text COMMENT 'url上面所带的参数',
  `url` varchar(256) DEFAULT NULL COMMENT '接口地址',
  `extract` varchar(2048) DEFAULT NULL COMMENT '提取信息',
  `validate` varchar(2048) DEFAULT NULL COMMENT '断言信息',
  `header` varchar(2048) DEFAULT NULL COMMENT '头部信息',
  `module_id` int(11) DEFAULT NULL COMMENT '所属的接口模块id',
  `project_id` int(11) DEFAULT NULL COMMENT '所属的项目id',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for interface_case
-- ----------------------------
DROP TABLE IF EXISTS `interface_case`;
CREATE TABLE `interface_case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `num` int(11) DEFAULT NULL COMMENT '用例序号',
  `name` varchar(128) DEFAULT NULL COMMENT '用例名称',
  `desc` varchar(256) DEFAULT NULL COMMENT '用例描述',
  `func_address` varchar(256) DEFAULT NULL COMMENT '用例需要引用的函数',
  `variable` text COMMENT '用例公共参数',
  `times` int(11) DEFAULT NULL COMMENT '执行次数',
  `project_id` int(11) DEFAULT NULL COMMENT '所属的项目id',
  `case_set_id` int(11) DEFAULT NULL COMMENT '所属的用例集id',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for interface_case_data
-- ----------------------------
DROP TABLE IF EXISTS `interface_case_data`;
CREATE TABLE `interface_case_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `num` int(11) DEFAULT NULL COMMENT '步骤序号，执行顺序按序号来',
  `status` varchar(16) DEFAULT NULL COMMENT '状态，true表示执行，false表示不执行',
  `name` varchar(128) DEFAULT NULL COMMENT '步骤名称',
  `up_func` varchar(256) DEFAULT NULL COMMENT '步骤执行前的函数',
  `down_func` varchar(256) DEFAULT NULL COMMENT '步骤执行后的函数',
  `time` int(11) DEFAULT NULL COMMENT '执行次数',
  `param` text,
  `status_param` varchar(64) DEFAULT NULL,
  `variable` text,
  `json_variable` text,
  `status_variables` varchar(64) DEFAULT NULL,
  `extract` varchar(2048) DEFAULT NULL,
  `status_extract` varchar(64) DEFAULT NULL,
  `validate` varchar(2048) DEFAULT NULL,
  `status_validate` varchar(64) DEFAULT NULL,
  `case_id` int(11) DEFAULT NULL,
  `api_msg_id` int(11) DEFAULT NULL,
  `execute_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for interface_case_set
-- ----------------------------
DROP TABLE IF EXISTS `interface_case_set`;
CREATE TABLE `interface_case_set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `num` int(11) DEFAULT NULL COMMENT '用例集合序号',
  `name` varchar(256) DEFAULT NULL COMMENT '用例集名称',
  `project_id` int(11) DEFAULT NULL COMMENT '所属的项目id',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for interface_config
-- ----------------------------
DROP TABLE IF EXISTS `interface_config`;
CREATE TABLE `interface_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `num` int(11) DEFAULT NULL COMMENT '配置序号',
  `name` varchar(128) DEFAULT NULL COMMENT '配置名称',
  `variables` varchar(21000) DEFAULT NULL COMMENT '配置参数',
  `func_address` varchar(128) DEFAULT NULL COMMENT '配置函数',
  `project_id` int(11) DEFAULT NULL COMMENT '所属的项目id',
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for interface_module
-- ----------------------------
DROP TABLE IF EXISTS `interface_module`;
CREATE TABLE `interface_module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_id` int(11) NOT NULL,
  `name` varchar(64) DEFAULT NULL COMMENT '接口模块',
  `num` int(11) DEFAULT NULL COMMENT '模块序号',
  `weight` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for interface_project
-- ----------------------------
DROP TABLE IF EXISTS `interface_project`;
CREATE TABLE `interface_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `ext` text,
  `host` varchar(1024) DEFAULT NULL COMMENT '测试环境',
  `host_two` varchar(1024) DEFAULT NULL COMMENT '开发环境',
  `host_three` varchar(1024) DEFAULT NULL COMMENT '线上环境',
  `host_four` varchar(1024) DEFAULT NULL COMMENT '备用环境',
  `environment_choice` varchar(16) DEFAULT NULL COMMENT '环境选择，first为测试，以此类推',
  `principal` varchar(512) DEFAULT NULL,
  `variables` varchar(2048) DEFAULT NULL COMMENT '项目的公共变量',
  `headers` varchar(1024) DEFAULT NULL COMMENT '项目的公共头部信息',
  `all_project_id` int(11) DEFAULT NULL COMMENT '项目的总id',
  `user_id` int(11) DEFAULT NULL COMMENT '所属的用户id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for interface_report
-- ----------------------------
DROP TABLE IF EXISTS `interface_report`;
CREATE TABLE `interface_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `case_names` varchar(128) DEFAULT NULL COMMENT '用例的名称集合',
  `read_status` varchar(16) DEFAULT NULL COMMENT '阅读状态',
  `project_id` varchar(16) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for interface_task
-- ----------------------------
DROP TABLE IF EXISTS `interface_task`;
CREATE TABLE `interface_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `num` int(11) DEFAULT NULL COMMENT '任务序号',
  `task_name` varchar(64) DEFAULT NULL COMMENT '任务名称',
  `task_config_time` varchar(256) DEFAULT NULL COMMENT 'cron表达式',
  `set_id` varchar(2048) DEFAULT NULL,
  `case_id` varchar(2048) DEFAULT NULL,
  `task_type` varchar(16) DEFAULT NULL,
  `task_to_email_address` varchar(256) DEFAULT NULL COMMENT '收件人邮箱',
  `task_send_email_address` varchar(256) DEFAULT NULL COMMENT '发件人邮箱',
  `email_password` varchar(256) DEFAULT NULL COMMENT '发件人邮箱密码',
  `status` varchar(16) DEFAULT NULL COMMENT '任务的运行状态，默认是创建',
  `project_id` varchar(16) DEFAULT NULL,
  `delete_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for issue
-- ----------------------------
DROP TABLE IF EXISTS `issue`;
CREATE TABLE `issue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `issue_number` varchar(100) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `system` int(11) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `module_id` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `handler` int(11) DEFAULT NULL,
  `issue_type` int(11) DEFAULT NULL,
  `chance` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `stage` int(11) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `attach` text,
  `relate_case` int(11) DEFAULT NULL,
  `handle_status` int(11) DEFAULT NULL,
  `reopen` int(11) DEFAULT '0',
  `status` int(11) DEFAULT NULL,
  `weight` varchar(100) DEFAULT NULL,
  `description` text,
  `comment` varchar(255) DEFAULT NULL,
  `repair_time` varchar(100) DEFAULT NULL,
  `test_time` varchar(100) DEFAULT NULL,
  `detection_chance` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `requirement_id` int(11) DEFAULT NULL,
  `case_covered` int(11) DEFAULT NULL,
  `tag` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `creator` (`creator`),
  KEY `modifier` (`modifier`),
  KEY `handler` (`handler`),
  CONSTRAINT `issue_ibfk_1` FOREIGN KEY (`creator`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_ibfk_2` FOREIGN KEY (`modifier`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_ibfk_3` FOREIGN KEY (`handler`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for issue_record
-- ----------------------------
DROP TABLE IF EXISTS `issue_record`;
CREATE TABLE `issue_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `iss_id` int(11) DEFAULT NULL,
  `issue_number` varchar(100) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `system` varchar(100) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `module_id` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `handler` int(11) DEFAULT NULL,
  `issue_type` int(11) DEFAULT NULL,
  `chance` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `stage` int(11) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `attach` text,
  `relate_case` int(11) DEFAULT NULL,
  `handle_status` int(11) DEFAULT NULL,
  `reopen` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `weight` varchar(100) DEFAULT NULL,
  `description` text,
  `comment` varchar(255) DEFAULT NULL,
  `repair_time` varchar(100) DEFAULT NULL,
  `test_time` varchar(100) DEFAULT NULL,
  `detection_chance` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `requirement_id` int(11) DEFAULT NULL,
  `case_covered` int(11) DEFAULT NULL,
  `tag` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `creator` (`creator`),
  KEY `modifier` (`modifier`),
  KEY `handler` (`handler`),
  CONSTRAINT `issue_record_ibfk_1` FOREIGN KEY (`creator`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_record_ibfk_2` FOREIGN KEY (`modifier`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_record_ibfk_3` FOREIGN KEY (`handler`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for jira
-- ----------------------------
DROP TABLE IF EXISTS `jira`;
CREATE TABLE `jira` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) DEFAULT '0',
  `params` varchar(1000) DEFAULT NULL,
  `result` varchar(100) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NULL DEFAULT NULL,
  `key_type` int(11) DEFAULT NULL,
  `key_Id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for jobs_record
-- ----------------------------
DROP TABLE IF EXISTS `jobs_record`;
CREATE TABLE `jobs_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `job_id` varchar(100) DEFAULT NULL,
  `result` varchar(1000) DEFAULT NULL,
  `log` text,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_id` int(11) DEFAULT NULL,
  `content_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for module
-- ----------------------------
DROP TABLE IF EXISTS `module`;
CREATE TABLE `module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `project_id` int(11) NOT NULL,
  `description` text,
  `weight` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `parent_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of module
-- ----------------------------
BEGIN;
INSERT INTO `module` VALUES (1, '2019-09-03 12:49:47', '2019-09-06 15:45:11', 'Dashboard', 2, '', 1, 0, NULL, NULL);
INSERT INTO `module` VALUES (2, '2019-09-06 07:45:17', '2019-09-06 15:45:17', '看板', 2, '', 1, 0, NULL, NULL);
INSERT INTO `module` VALUES (3, '2019-09-06 07:45:25', '2019-09-06 15:45:24', '迭代管理', 2, '', 1, 0, NULL, NULL);
INSERT INTO `module` VALUES (4, '2019-09-06 07:45:34', '2019-09-06 15:45:33', '缺陷管理', 2, '', 1, 0, NULL, NULL);
INSERT INTO `module` VALUES (5, '2019-09-06 07:45:39', '2019-09-06 15:45:39', '用例管理', 2, '', 1, 0, NULL, NULL);
INSERT INTO `module` VALUES (6, '2019-09-06 07:45:45', '2019-09-06 15:45:45', '需求管理', 2, '', 1, 0, NULL, NULL);
INSERT INTO `module` VALUES (7, '2019-09-06 07:45:52', '2019-09-06 15:45:51', '流程管理', 2, '', 1, 0, NULL, NULL);
INSERT INTO `module` VALUES (8, '2019-09-06 08:15:37', '2019-09-06 16:15:36', '流程列表', 2, '', 1, 0, 7, NULL);
INSERT INTO `module` VALUES (9, '2019-09-06 08:15:43', '2019-09-06 16:15:42', '发起流程', 2, '', 1, 0, 7, NULL);
INSERT INTO `module` VALUES (10, '2019-09-06 08:15:51', '2019-09-06 16:15:50', '流程统计', 2, '', 1, 0, 7, NULL);
INSERT INTO `module` VALUES (11, '2019-09-06 08:16:03', '2019-09-06 16:16:03', '需求评审', 2, '', 1, 0, 6, NULL);
INSERT INTO `module` VALUES (12, '2019-09-06 08:16:17', '2019-09-06 16:16:16', '任务', 2, '', 1, 0, 3, NULL);
INSERT INTO `module` VALUES (13, '2019-09-06 08:16:23', '2019-09-06 16:16:23', '缺陷', 2, '', 1, 0, 3, NULL);
INSERT INTO `module` VALUES (14, '2019-09-06 08:16:29', '2019-09-06 16:16:28', '需求', 2, '', 1, 0, 3, NULL);
INSERT INTO `module` VALUES (15, '2019-09-10 09:02:21', '2019-09-10 17:02:20', '1', 3, '1', 1, 0, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for monkey
-- ----------------------------
DROP TABLE IF EXISTS `monkey`;
CREATE TABLE `monkey` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `app_name` varchar(100) DEFAULT NULL,
  `package_name` varchar(100) DEFAULT NULL,
  `app_version` varchar(100) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  `download_app_status` int(11) DEFAULT NULL,
  `begin_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `jenkins_url` varchar(100) DEFAULT NULL,
  `report_url` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `mobile_ids` varchar(100) DEFAULT NULL,
  `parameters` varchar(1000) DEFAULT NULL,
  `process` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `run_time` int(11) DEFAULT NULL,
  `actual_run_time` int(11) DEFAULT NULL,
  `app_install_required` int(11) DEFAULT NULL,
  `system_device` int(11) DEFAULT NULL,
  `login_required` int(11) DEFAULT NULL,
  `login_username` varchar(100) DEFAULT NULL,
  `login_password` varchar(100) DEFAULT NULL,
  `cancel_status` int(11) DEFAULT NULL,
  `test_type` int(11) DEFAULT '1',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for monkey_device_status
-- ----------------------------
DROP TABLE IF EXISTS `monkey_device_status`;
CREATE TABLE `monkey_device_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monkey_id` int(11) DEFAULT NULL,
  `mobile_id` int(11) DEFAULT NULL,
  `mobile_serial` varchar(100) DEFAULT NULL,
  `mobile_model` varchar(100) DEFAULT NULL,
  `mobile_version` varchar(100) DEFAULT NULL,
  `process` int(11) DEFAULT NULL,
  `activity_count` int(11) DEFAULT NULL,
  `activity_tested_count` int(11) DEFAULT NULL,
  `activity_all` varchar(10000) DEFAULT NULL,
  `activity_tested` varchar(10000) DEFAULT NULL,
  `anr_count` int(11) DEFAULT NULL,
  `crash_count` int(11) DEFAULT NULL,
  `crash_rate` int(11) DEFAULT NULL,
  `exception_count` int(11) DEFAULT NULL,
  `exception_run_time` int(11) DEFAULT NULL,
  `device_connect_status` int(11) DEFAULT NULL,
  `screen_lock_status` int(11) DEFAULT NULL,
  `setup_install_app_status` int(11) DEFAULT NULL,
  `start_app_status` int(11) DEFAULT NULL,
  `setup_uninstall_app_status` int(11) DEFAULT NULL,
  `login_app_status` int(11) DEFAULT NULL,
  `running_status` int(11) DEFAULT NULL,
  `teardown_uninstall_app_status` int(11) DEFAULT NULL,
  `current_stage` int(11) DEFAULT NULL,
  `begin_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `run_time` int(11) DEFAULT NULL,
  `running_error_reason` varchar(1000) DEFAULT NULL,
  `mobile_resolution` varchar(100) DEFAULT NULL,
  `cancel_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for monkey_device_using
-- ----------------------------
DROP TABLE IF EXISTS `monkey_device_using`;
CREATE TABLE `monkey_device_using` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `using` int(11) DEFAULT NULL,
  `serial` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for monkey_error_log
-- ----------------------------
DROP TABLE IF EXISTS `monkey_error_log`;
CREATE TABLE `monkey_error_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monkey_id` int(11) DEFAULT NULL,
  `task_id` int(11) DEFAULT NULL,
  `error_type` varchar(100) DEFAULT NULL,
  `error_message` text,
  `error_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for monkey_package
-- ----------------------------
DROP TABLE IF EXISTS `monkey_package`;
CREATE TABLE `monkey_package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) DEFAULT NULL,
  `package_name` varchar(100) DEFAULT NULL,
  `oss_url` varchar(200) DEFAULT NULL,
  `picture` text,
  `version` varchar(200) DEFAULT NULL,
  `default_activity` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `size` varchar(200) DEFAULT NULL,
  `test_type` int(11) DEFAULT '1',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for monkey_report
-- ----------------------------
DROP TABLE IF EXISTS `monkey_report`;
CREATE TABLE `monkey_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `monkey_id` int(11) DEFAULT NULL,
  `task_id` int(11) DEFAULT NULL,
  `report_type` int(11) DEFAULT NULL,
  `report_url` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pad
-- ----------------------------
DROP TABLE IF EXISTS `pad`;
CREATE TABLE `pad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `asset_id` varchar(100) DEFAULT NULL,
  `vendor` varchar(100) DEFAULT NULL,
  `device_number` varchar(1000) DEFAULT NULL,
  `os` varchar(100) DEFAULT NULL,
  `cpu` varchar(100) DEFAULT NULL,
  `core` varchar(100) DEFAULT NULL,
  `ram` varchar(100) DEFAULT NULL,
  `rom` varchar(100) DEFAULT NULL,
  `resolution` varchar(100) DEFAULT NULL,
  `buy_date` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pc
-- ----------------------------
DROP TABLE IF EXISTS `pc`;
CREATE TABLE `pc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `asset_id` varchar(100) DEFAULT NULL,
  `vendor` varchar(100) DEFAULT NULL,
  `os` varchar(100) DEFAULT NULL,
  `cpu` varchar(100) DEFAULT NULL,
  `core` int(11) DEFAULT NULL,
  `memory` int(11) DEFAULT NULL,
  `disk_size` int(11) DEFAULT NULL,
  `buy_date` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for performance_test
-- ----------------------------
DROP TABLE IF EXISTS `performance_test`;
CREATE TABLE `performance_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  `performance_id` int(11) DEFAULT NULL,
  `run_time` int(11) DEFAULT NULL,
  `cpu_average` float(255,0) DEFAULT NULL,
  `cpu_top` float(255,0) DEFAULT NULL,
  `rss_average` float(255,0) DEFAULT NULL,
  `rss_top` float(255,0) DEFAULT NULL,
  `heap_size_average` float(255,0) DEFAULT NULL,
  `heap_size_top` float(255,0) DEFAULT NULL,
  `heap_alloc_average` float(255,0) DEFAULT NULL,
  `heap_alloc_top` float(255,0) DEFAULT NULL,
  `run_type` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for performance_test_log
-- ----------------------------
DROP TABLE IF EXISTS `performance_test_log`;
CREATE TABLE `performance_test_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `performance_test_id` int(11) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  `cpu` float(255,0) DEFAULT NULL,
  `rss` float(255,0) DEFAULT NULL,
  `heap_size` float(255,0) DEFAULT NULL,
  `heap_alloc` float(255,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for phone
-- ----------------------------
DROP TABLE IF EXISTS `phone`;
CREATE TABLE `phone` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `asset_id` varchar(100) DEFAULT NULL,
  `vendor` varchar(100) DEFAULT NULL,
  `device_number` varchar(1000) DEFAULT NULL,
  `os` varchar(100) DEFAULT NULL,
  `cpu` varchar(100) DEFAULT NULL,
  `core` varchar(100) DEFAULT NULL,
  `ram` varchar(10) DEFAULT NULL,
  `rom` varchar(10) DEFAULT NULL,
  `resolution` varchar(100) DEFAULT NULL,
  `buy_date` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `borrow_id` int(11) DEFAULT NULL,
  `device_source` varchar(1000) DEFAULT NULL,
  `device_belong` varchar(1000) DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for phone_borrow
-- ----------------------------
DROP TABLE IF EXISTS `phone_borrow`;
CREATE TABLE `phone_borrow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `phone_id` int(11) DEFAULT NULL,
  `user_list` varchar(100) DEFAULT NULL,
  `confirm_userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for phone_record
-- ----------------------------
DROP TABLE IF EXISTS `phone_record`;
CREATE TABLE `phone_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `phone_id` int(11) DEFAULT NULL,
  `asset_id` varchar(100) DEFAULT NULL,
  `vendor` varchar(100) DEFAULT NULL,
  `device_number` varchar(1000) DEFAULT NULL,
  `os` varchar(100) DEFAULT NULL,
  `cpu` varchar(100) DEFAULT NULL,
  `core` varchar(100) DEFAULT NULL,
  `ram` varchar(10) DEFAULT NULL,
  `rom` varchar(10) DEFAULT NULL,
  `resolution` varchar(100) DEFAULT NULL,
  `buy_date` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `borrow_id` int(11) DEFAULT NULL,
  `device_source` varchar(1000) DEFAULT NULL,
  `device_belong` varchar(1000) DEFAULT NULL,
  `editor_id` int(11) DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `ext` text,
  `logo` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of project
-- ----------------------------
BEGIN;
INSERT INTO `project` VALUES (1, '2019-09-03 12:34:37', '2019-09-03 12:35:33', '云测平台', '云测平台', 1, 1, NULL, '');
INSERT INTO `project` VALUES (2, '2019-09-03 12:35:43', '2019-09-03 20:58:07', '云测平台', '', 0, 1, NULL, 'http://tcloud-static.ywopt.com/static/8757c32c-84cf-4e89-b03a-abf45461a8da.png');
INSERT INTO `project` VALUES (3, '2019-09-06 02:20:50', '2019-09-10 17:25:25', 'demo', 'demo', 1, 1, NULL, '');
INSERT INTO `project` VALUES (4, '2019-09-10 04:00:33', '2019-09-10 12:00:33', '1', '1', 0, 1, NULL, '');
INSERT INTO `project` VALUES (5, '2019-09-10 11:44:55', '2019-09-10 19:44:55', '123', '', 0, 1, NULL, '');
COMMIT;

-- ----------------------------
-- Table structure for project_bind_business
-- ----------------------------
DROP TABLE IF EXISTS `project_bind_business`;
CREATE TABLE `project_bind_business` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_id` int(11) DEFAULT NULL,
  `business_id` int(11) DEFAULT NULL,
  `ext` text,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for requirement
-- ----------------------------
DROP TABLE IF EXISTS `requirement`;
CREATE TABLE `requirement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(200) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `version` varchar(100) DEFAULT NULL,
  `requirement_type` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `handler` int(11) DEFAULT NULL,
  `board_status` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` text,
  `priority` int(11) DEFAULT NULL,
  `attach` text,
  `comment` varchar(300) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `parent_id` int(11) NOT NULL DEFAULT '0',
  `review_status` int(11) NOT NULL DEFAULT '1',
  `jira_id` varchar(300) DEFAULT NULL,
  `worth` int(11) DEFAULT NULL,
  `report_time` varchar(300) DEFAULT NULL,
  `report_real` text,
  `report_expect` text,
  `worth_sure` int(11) DEFAULT NULL,
  `expect_time` datetime DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for requirement_bind_case
-- ----------------------------
DROP TABLE IF EXISTS `requirement_bind_case`;
CREATE TABLE `requirement_bind_case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `requirement_id` int(11) DEFAULT NULL,
  `case_id` int(11) DEFAULT NULL,
  `creation_time` timestamp NULL DEFAULT NULL,
  `modified_time` timestamp NULL DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for requirement_record
-- ----------------------------
DROP TABLE IF EXISTS `requirement_record`;
CREATE TABLE `requirement_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `requirement_id` int(11) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `version` varchar(100) DEFAULT NULL,
  `requirement_type` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `handler` int(11) DEFAULT NULL,
  `board_status` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` text,
  `priority` int(11) DEFAULT NULL,
  `attach` text,
  `comment` varchar(300) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `parent_id` int(11) NOT NULL DEFAULT '0',
  `review_status` int(11) NOT NULL DEFAULT '1',
  `jira_id` varchar(300) DEFAULT NULL,
  `worth` int(11) DEFAULT NULL,
  `report_time` varchar(300) DEFAULT NULL,
  `report_expect` text,
  `report_real` text,
  `worth_sure` int(11) DEFAULT NULL,
  `expect_time` datetime DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for requirement_review
-- ----------------------------
DROP TABLE IF EXISTS `requirement_review`;
CREATE TABLE `requirement_review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `review_id` int(11) DEFAULT NULL,
  `requirement_id` int(11) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `version` varchar(100) DEFAULT NULL,
  `requirement_type` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `handler` int(11) DEFAULT NULL,
  `board_status` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` text,
  `priority` int(11) DEFAULT NULL,
  `attach` text,
  `comment` varchar(300) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `review_status` int(11) DEFAULT NULL,
  `jira_id` varchar(300) DEFAULT NULL,
  `worth` int(11) DEFAULT NULL,
  `report_time` varchar(300) DEFAULT NULL,
  `report_real` text,
  `report_expect` text,
  `worth_sure` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for review
-- ----------------------------
DROP TABLE IF EXISTS `review`;
CREATE TABLE `review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(200) DEFAULT NULL,
  `requirement_list` varchar(200) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `reviewer` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `attach` text,
  `comment` varchar(300) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `review_status` int(11) DEFAULT NULL,
  `version_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES (1, '2019-01-23 14:19:56', '2019-07-11 14:40:14', 'admin', 0, 1, '超级管理员');
INSERT INTO `role` VALUES (2, '2019-01-23 14:19:56', '2019-07-10 14:56:30', 'dev', 0, 1, '开发');
INSERT INTO `role` VALUES (3, '2019-01-23 14:19:56', '2019-07-10 14:56:33', 'test', 0, 1, '测试');
INSERT INTO `role` VALUES (4, '2019-01-23 14:19:56', '2019-07-10 14:56:36', 'opt', 0, 1, '运维');
INSERT INTO `role` VALUES (5, '2019-02-14 17:41:26', '2019-07-10 14:56:41', 'prod', 0, 1, '产品');
INSERT INTO `role` VALUES (6, '2019-02-15 11:46:59', '2019-07-10 14:56:47', 'owner', 0, 1, '项目管理员');
COMMIT;

-- ----------------------------
-- Table structure for role_bind_ability
-- ----------------------------
DROP TABLE IF EXISTS `role_bind_ability`;
CREATE TABLE `role_bind_ability` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `role_id` int(11) DEFAULT NULL,
  `ability_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for route_statistics
-- ----------------------------
DROP TABLE IF EXISTS `route_statistics`;
CREATE TABLE `route_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `route` varchar(100) DEFAULT NULL,
  `service` varchar(30) DEFAULT NULL,
  `count` int(11) DEFAULT '1',
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `method` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tag` varchar(300) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` text,
  `creator` varchar(300) DEFAULT NULL,
  `tag_type` int(11) DEFAULT NULL,
  `reference_nums` int(11) DEFAULT '0',
  `modifier` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `description` varchar(300) DEFAULT NULL,
  `testreport` text,
  `tmethod` varchar(50) DEFAULT NULL,
  `ttype` varchar(50) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `executor` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `start_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `ext` text,
  `case_list` text,
  `attach` text,
  `tag` varchar(300) DEFAULT NULL,
  `attachment` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for task_case
-- ----------------------------
DROP TABLE IF EXISTS `task_case`;
CREATE TABLE `task_case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `task_id` int(11) DEFAULT NULL,
  `executor` int(11) DEFAULT NULL,
  `exe_way` int(11) DEFAULT NULL,
  `handler` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `title` varchar(300) DEFAULT NULL,
  `cnumber` varchar(100) DEFAULT NULL,
  `module_id` int(11) DEFAULT NULL,
  `feature_id` int(11) DEFAULT NULL,
  `ctype` varchar(10) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `precondition` text,
  `step_result` text,
  `is_auto` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for task_case_record
-- ----------------------------
DROP TABLE IF EXISTS `task_case_record`;
CREATE TABLE `task_case_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `task_case_id` int(11) DEFAULT NULL,
  `task_id` int(11) DEFAULT NULL,
  `executor` int(11) DEFAULT NULL,
  `exe_way` int(11) DEFAULT NULL,
  `handler` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `modifier` int(11) DEFAULT NULL,
  `title` varchar(300) DEFAULT NULL,
  `cnumber` varchar(100) DEFAULT NULL,
  `module_id` int(11) DEFAULT NULL,
  `feature_id` int(11) DEFAULT NULL,
  `ctype` varchar(10) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `precondition` text,
  `step_result` text,
  `is_auto` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for task_tag
-- ----------------------------
DROP TABLE IF EXISTS `task_tag`;
CREATE TABLE `task_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tag` varchar(300) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` text,
  `creator` varchar(300) DEFAULT NULL,
  `tag_type` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tc_devices
-- ----------------------------
DROP TABLE IF EXISTS `tc_devices`;
CREATE TABLE `tc_devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `uuid` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `use_type` int(11) DEFAULT NULL,
  `using` int(11) DEFAULT NULL,
  `manufacturer` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `platform` varchar(100) DEFAULT NULL,
  `version` varchar(100) DEFAULT NULL,
  `serial` varchar(100) DEFAULT NULL,
  `resolution` varchar(100) DEFAULT NULL,
  `use_time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tc_devicesn_info
-- ----------------------------
DROP TABLE IF EXISTS `tc_devicesn_info`;
CREATE TABLE `tc_devicesn_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `serial` varchar(100) DEFAULT NULL,
  `times` int(11) DEFAULT NULL,
  `use_time` varchar(100) DEFAULT NULL,
  `pic` varchar(200) DEFAULT NULL,
  `comment` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for track_upload
-- ----------------------------
DROP TABLE IF EXISTS `track_upload`;
CREATE TABLE `track_upload` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `device_type` int(11) DEFAULT NULL,
  `device_typename` varchar(200) DEFAULT NULL,
  `device_number` varchar(500) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for track_user
-- ----------------------------
DROP TABLE IF EXISTS `track_user`;
CREATE TABLE `track_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `nickname` varchar(100) DEFAULT NULL,
  `wx_userid` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telephone` varchar(30) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `track_token` text,
  `name` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(200) DEFAULT NULL,
  `info` text,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(100) NOT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `wx_userid` varchar(200) DEFAULT NULL,
  `password` varchar(100) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telephone` varchar(30) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `ext` text,
  `picture` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (1, NULL, '2019-09-02 03:39:01', 'admin', 'admin', NULL, 'b8d65d4bd2d9416ec6300da8797e0284', 0, NULL, NULL, 1, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for user_bind_project
-- ----------------------------
DROP TABLE IF EXISTS `user_bind_project`;
CREATE TABLE `user_bind_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user_bind_role
-- ----------------------------
DROP TABLE IF EXISTS `user_bind_role`;
CREATE TABLE `user_bind_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_bind_role
-- ----------------------------
BEGIN;
INSERT INTO `user_bind_role` VALUES (1, NULL, '2019-09-03 12:28:31', 1, 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for version
-- ----------------------------
DROP TABLE IF EXISTS `version`;
CREATE TABLE `version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(200) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `start_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `publish_time` timestamp NULL DEFAULT NULL,
  `creator` int(11) DEFAULT NULL,
  `publish_status` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for virtual_asset
-- ----------------------------
DROP TABLE IF EXISTS `virtual_asset`;
CREATE TABLE `virtual_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_time` datetime DEFAULT NULL,
  `modified_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `asset_id` varchar(100) NOT NULL,
  `passwd` varchar(100) DEFAULT NULL,
  `administrator` varchar(100) DEFAULT NULL,
  `bind_tel` varchar(100) DEFAULT NULL,
  `idcard` varchar(100) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `asset_type` int(11) DEFAULT NULL,
  `operator` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
