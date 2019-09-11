/*
 Navicat Premium Data Transfer

 Source Server         : dev
 Source Server Type    : MySQL
 Source Server Version : 50616
 Source Host           : rm-2ze3hdq85qi33k641fo.mysql.rds.aliyuncs.com:3306
 Source Schema         : tcloud_2

 Target Server Type    : MySQL
 Target Server Version : 50616
 File Encoding         : 65001

 Date: 10/09/2019 20:31:50
*/

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of board_config
-- ----------------------------
BEGIN;
INSERT INTO `board_config` VALUES (1, '1,2,3,4,6,5', '0,1,2,4,5,6,3', '2019-09-03 12:49:31', '2019-09-03 20:49:31', NULL, '2', NULL);
INSERT INTO `board_config` VALUES (2, '1,2,3,4,6,5', '0,1,2,4,5,6,3', '2019-09-06 08:19:21', '2019-09-06 16:19:21', NULL, '3', NULL);
INSERT INTO `board_config` VALUES (3, '1,2,3,4,6,5', '0,1,2,4,5,6,3', '2019-09-10 08:29:44', '2019-09-10 16:29:43', NULL, '4', NULL);
COMMIT;

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
-- Records of case
-- ----------------------------
BEGIN;
INSERT INTO `case` VALUES (1, '2019-09-03 12:50:01', '2019-09-03 20:50:00', 'TC1', 1, '1', NULL, '测试用例', NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 0, 1152, 1, NULL);
INSERT INTO `case` VALUES (2, '2019-09-04 06:56:37', '2019-09-04 14:56:36', 'TC2', 1, '1', NULL, '测试用例2', '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 0, 1152, 0, NULL);
INSERT INTO `case` VALUES (3, '2019-09-04 06:56:49', '2019-09-04 14:56:48', 'TC3', 1, '1', NULL, '测试用例3', '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 0, 1152, 1, NULL);
INSERT INTO `case` VALUES (4, '2019-09-04 06:56:58', '2019-09-04 14:56:57', 'TC4', 1, '1', NULL, '测试用例4', '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 0, 1152, 2, NULL);
INSERT INTO `case` VALUES (5, '2019-09-06 07:48:26', '2019-09-06 15:48:26', 'TC5', 7, '1', NULL, '新建一条流程', '当前在测试环境，用例管理模块', '{\"step_result\":[{\"step\":\"点击新建按钮\",\"expect\":\"弹出新建流程的弹窗页面\"},{\"step\":\"一次输入必填项，点击保存按钮\",\"expect\":\"流程新建成功，跳转到该流程的详情页面\"}]}', 1, 0, 1152, 1, NULL);
INSERT INTO `case` VALUES (6, '2019-09-06 07:52:20', '2019-09-06 15:52:20', 'TC6', 7, '1', NULL, '删除一条流程', NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击确定\",\"expect\":\"删除成功\"}]}', 1, 0, 1152, 2, NULL);
INSERT INTO `case` VALUES (7, '2019-09-06 07:53:13', '2019-09-06 15:53:12', 'TC7', 7, '1', NULL, '取消删除流程', NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击取消按钮\",\"expect\":\"删除确认框收起，没有执行删除操作\"}]}', 1, 0, 1152, 1, NULL);
INSERT INTO `case` VALUES (8, '2019-09-06 08:01:26', '2019-09-06 16:01:25', 'TC8', 4, '1', NULL, 'issue字段检查', NULL, '{\"step_result\":[{\"step\":\"检查issue列表的字段\",\"expect\":\"字段包含：ID、标题、创建人、处理人、状态、优先级、级别、issue分数、创建时间、更新时间。。。\"}]}', 1, 0, 1152, 2, NULL);
INSERT INTO `case` VALUES (9, '2019-09-10 09:03:24', '2019-09-10 17:03:24', 'TC9', 15, '1,3', NULL, '1', NULL, '{\"step_result\":[{\"step\":\"2\",\"expect\":\"3\"},{\"step\":\"4\",\"expect\":\"5\"}]}', 1, 0, 1152, 1, NULL);
COMMIT;

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
INSERT INTO `config` VALUES (1, '2019-01-23 14:19:56', '2019-08-08 11:09:01', 'issue', 1, '{\"operation_dict\":{\"requirement_id\":\"需求\",\"attach\":\"附件\",\"chance\":\"BUG出现机率\",\"comment\":\"备注\",\"description\":\"描述\",\"handle_status\":\"处理状态\",\"handler_name\":\"处理人\",\"issue_type\":\"BUG类型\",\"level\":\"BUG级别\",\"module_name\":\"模块\",\"priority\":\"优先级\",\"status\":\"状态\",\"title\":\"标题\",\"system\":\"所属系统\",\"detection_chance\":\"用户识别度\"},\"chance\":{\"0\":\"必现\",\"1\":\"大概率\",\"2\":\"小概率\",\"3\":\"极小概率\",\"\":\"\"},\"issue_type\":{\"0\":\"功能问题\",\"1\":\"界面优化\",\"2\":\"设计缺陷\",\"3\":\"安全相关\",\"4\":\"性能问题\",\"5\":\"开发修改引入\",\"6\":\"其他\",\"\":\"\"},\"level\":{\"0\":\"阻塞\",\"1\":\"严重\",\"2\":\"重要\",\"3\":\"次要\",\"4\":\"微小\",\"\":\"\"},\"priority\":{\"0\":\"紧急\",\"1\":\"高\",\"2\":\"中\",\"3\":\"低\",\"\":\"\"},\"handle_status\":{\"1\":\"待办\",\"2\":\"处理中\",\"3\":\"测试中\",\"4\":\"已关闭\",\"5\":\"已拒绝\",\"6\":\"延时处理\",\"\":\"\"},\"system\":{\"1\":\"ANDROID\",\"2\":\"IOS\",\"3\":\"后端\",\"4\":\"H5\",\"5\":\"小程序\",\"6\":\"WEB端\",\"7\":\"其他\",\"\":\"\"},\"detection_chance\":{\"0\":\"明显的\",\"1\":\"高概率\",\"2\":\"中概率\",\"3\":\"小概率\"}}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (2, '2019-01-23 14:19:56', '2019-01-23 14:19:58', 'board', 1, '{\"create\":{\"task\":[0,1,2],\"task_case\":[],\"issue\":[1,2,3,4,5,6]},\"unfinish\":{\"task\":[0],\"task_case\":[0],\"issue\":[1,2,3,5,6]},\"finish\":{\"task\":[2],\"task_case\":[2,3,4],\"issue\":[4]}}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (3, '2019-01-23 14:19:56', '2019-06-24 19:10:34', 'requirement', 1, '{\"operation_dict\":{\"attach\":\"附件\",\"comment\":\"备注\",\"description\":\"描述\",\"board_status\":\"处理状态\",\"handler_name\":\"处理人\",\"requirement_type\":\"类型\",\"priority\":\"优先级\",\"status\":\"状态\",\"title\":\"标题\",\"review_status\":\"评审状态\",\"worth\":\"需求价值\",\"worth_sure\":\"需求价值确认\",\"jira_id\":\"jira号\",\"report_time\":\"需获取置信结果天数\",\"report_expect\":\"高价值预期结果\",\"report_real\":\"高价值实际结果\"},\"requirement_type\":{\"0\":\"功能需求\",\"1\":\"优化需求\",\"2\":\"自动化需求\",\"3\":\"性能需求\",\"4\":\"兼容性需求\",\"5\":\"报表需求\",\"6\":\"临时需求\",\"7\":\"紧急需求\",\"8\":\"新功能需求\",\"9\":\"其他\",\"\":\"\"},\"priority\":{\"0\":\"紧急\",\"1\":\"高\",\"2\":\"中\",\"3\":\"低\",\"\":\"\"},\"board_status\":{\"0\":\"规划中\",\"1\":\"实现中\",\"2\":\"测试中\",\"3\":\"已拒绝\",\"4\":\"待验收\",\"5\":\"待发布\",\"6\":\"完成\",\"\":\"\"},\"review_status\":{\"1\":\"未评审\",\"2\":\"评审成功\",\"3\":\"评审失败\",\"\":\"\"},\"worth_sure\":{\"1\":\"超出预期\",\"2\":\"符合预期\",\"3\":\"低于预期\",\"\":\"\"},\"worth\":{\"1\":\"高价值\",\"2\":\"非高价值\",\"\":\"\"}}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (4, '2019-01-23 14:19:56', '2019-03-15 11:02:20', 'issue', 2, '{\"test\":[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[1,2],[3,2],[3,4],[4,2],[5,2],[5,4],[6,2],[6,4]],\"dev\":[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[1,2],[2,3],[2,5],[2,6]],\"admin\":[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[1,2],[2,3],[2,5],[2,6],[3,2],[3,4],[4,2],[5,2],[5,4],[6,2],[6,4]]}', 'issue的状态记录', NULL);
INSERT INTO `config` VALUES (5, '2019-01-23 14:19:56', '2019-09-02 10:36:55', 'access_token', 1, '{\"access_token\": \"\"}', NULL, 0);
INSERT INTO `config` VALUES (6, '2019-04-03 10:41:22', '2019-06-14 13:57:29', 'stf', 1, '{\"URL\":\"\",\"headers\":{\"Authorization\": \"\"}}', NULL, NULL);
INSERT INTO `config` VALUES (7, '2019-04-12 13:47:51', '2019-04-12 13:52:29', 'corp_secret', 1, '', NULL, NULL);
INSERT INTO `config` VALUES (8, '2019-04-28 16:27:46', '2019-04-29 16:31:36', 'stf', 2, '{\"URL\":\"\"}', NULL, NULL);
INSERT INTO `config` VALUES (9, '2019-05-05 15:53:04', '2019-06-24 12:39:36', 'stf', 3, '{\"URL\":\"\",\"headers\":{\"Authorization\": \"\"}}', NULL, NULL);
INSERT INTO `config` VALUES (10, NULL, '2019-06-20 14:14:25', 'tcloud', 1, '', NULL, NULL);
INSERT INTO `config` VALUES (15, NULL, '2019-06-20 14:14:17', 'tcloud', 2, '', NULL, NULL);
INSERT INTO `config` VALUES (16, '2019-05-24 17:54:08', '2019-07-26 16:35:33', 'jenkins', 1, '{\"4\":[{\"id\":0,\"name\":\"萌推回归测试\",\"job\":\"mengtui_regression_test\"},{\"id\":1,\"name\":\"萌推回归测试\",\"job\":\"mengtui_regression_test\"},{\"id\":2,\"name\":\"萌推单个接口\",\"job\":\"mengtui_singel_api_dev\"}],\"1\":[{\"id\":1,\"name\":\"萌推回归测试\",\"job\":\"mengtui_regression_test\"}]}', NULL, NULL);
INSERT INTO `config` VALUES (17, '2019-05-24 20:10:50', '2019-07-22 10:43:34', 'jenkins', 2, '{\"url\":\"\",\"user_id\":\"\",\"api_token\":\"\"}', 'jenkins 账号信息', NULL);
INSERT INTO `config` VALUES (18, '2019-06-14 11:19:56', '2019-06-13 18:59:35', 'asset', 1, '{\"operation_dict\":{\"name\":\"名称\",\"asset_id\":\"资产编号\",\"status\":\"状态\",\"borrow_id\":\"持有者\"},\"status\":{\"0\":\"不可用\",\"1\":\"可用\"}}', '资产的转移记录', NULL);
INSERT INTO `config` VALUES (19, '2019-06-14 14:19:56', '2019-06-14 14:08:15', 'credit', 1, '{\"operation_dict\":{\"score\": \"信用积分\"},\"status\":{\"0\":\"不可用\",\"1\":\"可用\"}}', '信用积分记录', NULL);
INSERT INTO `config` VALUES (20, '2019-06-17 19:43:09', '2019-07-02 14:27:40', 'deploy', 1, '{\"operation_dict\":[{\"4\":\"4\"},{\"1\":\"4\"}]}', NULL, NULL);
INSERT INTO `config` VALUES (22, '2019-06-21 15:49:01', '2019-07-02 22:40:30', 'track', 1, '{\"operation_dict\":[{\"1\":\"3\"},{\"2\":\"42\"},{\"3\":\"41\"},{\"4\":\"43\"},{\"63\":\"45\"}]}', '埋点项目配置', NULL);
INSERT INTO `config` VALUES (23, '2019-06-21 16:05:34', '2019-07-02 22:40:09', 'track', 2, '{\"URL\":\"\"}', '埋点项目url', NULL);
INSERT INTO `config` VALUES (24, '2019-06-26 23:08:57', '2019-07-02 22:40:19', 'track', 3, '{\"URL\":\"\"}', '埋点项目websocket', NULL);
INSERT INTO `config` VALUES (25, '2019-07-01 16:11:16', '2019-07-02 21:41:32', 'deploy', 2, '{\"URL\":\"\"}', '部署url', NULL);
INSERT INTO `config` VALUES (26, '2019-07-01 16:12:13', '2019-07-02 14:27:30', 'deploy', 3, '{\"api\":\"AwA8qLLB\"}', '部署token', NULL);
INSERT INTO `config` VALUES (27, '2019-07-22 10:44:01', '2019-07-22 19:12:27', 'jenkins', 3, '{\"job\":[\"mengtui_activity_api\",\"mengtui_regression_test\",\"mengtui_scene_api\",\"shihuimiao_activity_api\",\"shihuimiao_scene_api\"]}', 'jenkins更新的job', NULL);
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of feedback
-- ----------------------------
BEGIN;
INSERT INTO `feedback` VALUES (1, '2019-09-06 07:37:31', '2019-09-06 15:37:30', '10000000000', 1152, 0, '平台不错', 1);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of flow_info
-- ----------------------------
BEGIN;
INSERT INTO `flow_info` VALUES (1, '2019-09-06 08:02:52', '2019-09-06 16:09:08', '搜索优化上线提测', 1, '3', 2, '3,4,5,6,8,9,11,13,14,16', NULL, NULL, '2019-09-06 08:09:08', 2, NULL, 1152, '[1152, 1155]', '[1154]', '[1154]', '[1155]', '{\"process\": 100, \"current_step\": \"16\", \"current_step_name\": \"\\u5b8c\\u6210\", \"steps\": [{\"id\": 3, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u81ea\\u6d4b\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:03:28\"}, {\"id\": 4, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u6d4b\\u8bd5\\u73af\\u5883\\u6d4b\\u8bd5\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:03:38\"}, {\"id\": 5, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>PM\\u9a8c\\u6536\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:03:46\"}, {\"id\": 6, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>[\\u4f9d\\u8d56kafka]\\uff1a</p><p>[PR]:</p><p>[\\u6570\\u636e\\u5e93\\u53d8\\u52a8]\\uff1a</p><p>[\\u4f9d\\u8d56ab\\u5b9e\\u9a8c]:</p><p>[\\u4f9d\\u8d56\\u914d\\u7f6e]:</p><p>[\\u670d\\u52a1\\u7aef\\u4e0a\\u7ebf\\u987a\\u5e8f]</p><p>[OMS/MMS]</p><p>[\\u9700\\u6c42JIRA]</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:08:20\"}, {\"id\": 8, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u9884\\u53d1\\u5e03\\u73af\\u5883\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:08:31\"}, {\"id\": 9, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>PM\\u9884\\u53d1\\u5e03\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:08:39\"}, {\"id\": 11, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>ok</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:08:43\"}, {\"id\": 13, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>QA\\u7ebf\\u4e0a\\u73af\\u5883\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:08:58\"}, {\"id\": 14, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>PM\\u7ebf\\u4e0a\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:09:04\"}, {\"id\": 16, \"name\": \"\\u641c\\u7d22\\u4f18\\u5316\\u4e0a\\u7ebf\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>ok</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:09:08\"}], \"step_tab\": [{\"step_tab_id\": \"1\", \"step_tab_name\": \"\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u6d4b\\u8bd5,\\u5f00\\u53d1\"}]}', 2, NULL, '[{\"id\":3,\"title\":\"搜索页面优化\",\"jira_id\":\"\"}]', '[1]', '暂无');
INSERT INTO `flow_info` VALUES (2, '2019-09-06 08:05:08', '2019-09-06 16:25:28', 'issue增加一个字段提测', 1, '6', 1, '3,4,5,8,9,10,13,14,15,16', NULL, NULL, NULL, 2, NULL, 1152, '[1155]', '[1154]', '[1154]', '[1155, 1152]', '{\"process\": 80, \"current_step\": \"15\", \"current_step_name\": \"\\u5168\\u91cf\\u53d1\\u5305\", \"steps\": [{\"id\": 3, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u81ea\\u6d4b\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:05:42\"}, {\"id\": 4, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"2\", \"comment\": \"<p>\\u5192\\u70df\\u4e0d\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:05:48\"}, {\"id\": 3, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u81ea\\u6d4b\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:24:11\"}, {\"id\": 4, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u6d4b\\u8bd5\\u73af\\u5883\\u6d4b\\u8bd5\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:24:21\"}, {\"id\": 5, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>PM\\u9a8c\\u6536\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:24:28\"}, {\"id\": 8, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>QA\\u9884\\u53d1\\u5e03\\u9a8c\\u6536\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:24:41\"}, {\"id\": 9, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>PM\\u9884\\u53d1\\u5e03\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:24:54\"}, {\"id\": 10, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u7070\\u5ea6\\u53d1\\u5305OK</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:25:07\"}, {\"id\": 13, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>QA\\u7ebf\\u4e0a\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:25:19\"}, {\"id\": 14, \"name\": \"issue\\u589e\\u52a0\\u4e00\\u4e2a\\u5b57\\u6bb5\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>PM\\u7ebf\\u4e0a\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:25:28\"}], \"step_tab\": [{\"step_tab_id\": \"1\", \"step_tab_name\": \"\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u5f00\\u53d1\"}, {\"step_tab_id\": \"2\", \"step_tab_name\": \"\\u4e0d\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u6d41\\u7a0b\\u7b2c\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u5f00\\u53d1\"}, {\"step_tab_id\": \"3\", \"step_tab_name\": \"\\u8df3\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u5f00\\u53d1\"}]}', 0, NULL, '[{\"id\":6,\"title\":\"issue增加一个字段\",\"jira_id\":\"\"}]', '[1]', '数据库依赖');
INSERT INTO `flow_info` VALUES (3, '2019-09-06 08:06:35', '2019-09-06 16:23:53', '分页优化提测', 1, '5', 5, '2,4,7,11,12,16', NULL, NULL, NULL, 2, NULL, 1152, '[1155]', '[1154]', '[1154]', '[1152]', '{\"process\": 50, \"current_step\": \"11\", \"current_step_name\": \"\\u6b63\\u5f0f\\u4e0a\\u7ebf\", \"steps\": [{\"id\": 2, \"name\": \"\\u5206\\u9875\\u4f18\\u5316\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u81ea\\u6d4b\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:23:36\"}, {\"id\": 4, \"name\": \"\\u5206\\u9875\\u4f18\\u5316\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u6d4b\\u8bd5\\u73af\\u5883\\u6d4b\\u8bd5\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:23:44\"}, {\"id\": 7, \"name\": \"\\u5206\\u9875\\u4f18\\u5316\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u9884\\u53d1\\u5e03\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:23:53\"}], \"step_tab\": [{\"step_tab_id\": \"6\", \"step_tab_name\": \"\\u5907\\u6ce8\", \"step_tab_result\": \"\\u4f1a\\u505c\\u7559\\u5728\\u5f53\\u524d\\u6b65\\u9aa4\", \"step_tab_user\": \"admin,\\u5f00\\u53d1\"}, {\"step_tab_id\": \"1\", \"step_tab_name\": \"\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u5f00\\u53d1\"}, {\"step_tab_id\": \"2\", \"step_tab_name\": \"\\u4e0d\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u6d41\\u7a0b\\u7b2c\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u5f00\\u53d1\"}, {\"step_tab_id\": \"3\", \"step_tab_name\": \"\\u8df3\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin\"}]}', 0, 1, '[{\"id\":5,\"title\":\"分页优化\",\"jira_id\":\"\"}]', '[1]', '');
INSERT INTO `flow_info` VALUES (4, '2019-09-06 08:07:27', '2019-09-06 16:23:27', '增加taskcase导出功能', 1, '4', 1, '3,4,5,8,9,10,13,14,15,16', NULL, NULL, NULL, 2, NULL, 1152, '[1155]', '[1154]', '[1154]', '[1152]', '{\"process\": 20, \"current_step\": \"5\", \"current_step_name\": \"PM\\u9a8c\\u6536\", \"steps\": [{\"id\": 3, \"name\": \"\\u589e\\u52a0taskcase\\u5bfc\\u51fa\\u529f\\u80fd\", \"result\": \"1\", \"comment\": \"<p>\\u81ea\\u6d4b\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:23:19\"}, {\"id\": 4, \"name\": \"\\u589e\\u52a0taskcase\\u5bfc\\u51fa\\u529f\\u80fd\", \"result\": \"1\", \"comment\": \"<p>\\u6d4b\\u8bd5\\u73af\\u5883\\u9a8c\\u8bc1\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:23:27\"}], \"step_tab\": [{\"step_tab_id\": \"1\", \"step_tab_name\": \"\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u6d4b\\u8bd5\"}, {\"step_tab_id\": \"2\", \"step_tab_name\": \"\\u4e0d\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u6d41\\u7a0b\\u7b2c\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u6d4b\\u8bd5\"}, {\"step_tab_id\": \"3\", \"step_tab_name\": \"\\u8df3\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin\"}]}', 0, NULL, '[{\"id\":4,\"title\":\"增加taskcase导出功能\",\"jira_id\":\"\"}]', '[2, 4]', '上线依赖1\n上线依赖2\n上线依赖3\n');
INSERT INTO `flow_info` VALUES (5, '2019-09-06 08:22:59', '2019-09-06 16:23:08', '缺陷支持修改版本提测', 1, '2', 1, '3,4,5,8,9,10,13,14,15,16', NULL, NULL, NULL, 2, NULL, 1152, '[1155]', '[1154]', '[1154]', '[1152]', '{\"process\": 10, \"current_step\": \"4\", \"current_step_name\": \"\\u529f\\u80fd\\u6d4b\\u8bd5\", \"steps\": [{\"id\": 3, \"name\": \"\\u7f3a\\u9677\\u652f\\u6301\\u4fee\\u6539\\u7248\\u672c\\u63d0\\u6d4b\", \"result\": \"1\", \"comment\": \"<p>\\u81ea\\u6d4b\\u901a\\u8fc7</p>\", \"user_id\": 1152, \"user_name\": \"admin\", \"creation_time\": \"2019-09-06 08:23:08\"}], \"step_tab\": [{\"step_tab_id\": \"5\", \"step_tab_name\": \"\\u81ea\\u52a8\\u5316\\u6d4b\\u8bd5\", \"step_tab_result\": \"\\u4f1a\\u505c\\u7559\\u5728\\u5f53\\u524d\\u6b65\\u9aa4\", \"step_tab_user\": \"admin,\\u6d4b\\u8bd5\"}, {\"step_tab_id\": \"1\", \"step_tab_name\": \"\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u4e0b\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u6d4b\\u8bd5\"}, {\"step_tab_id\": \"2\", \"step_tab_name\": \"\\u4e0d\\u901a\\u8fc7\", \"step_tab_result\": \"\\u4f1a\\u8df3\\u8f6c\\u5230\\u6d41\\u7a0b\\u7b2c\\u4e00\\u6b65\", \"step_tab_user\": \"admin,\\u6d4b\\u8bd5\"}]}', 0, 1, '[{\"id\":2,\"title\":\"云测平台3.0版本需求\",\"jira_id\":\"\"}]', '[1]', '');
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of flow_record
-- ----------------------------
BEGIN;
INSERT INTO `flow_record` VALUES (1, '2019-09-06 08:03:29', '2019-09-06 16:03:28', 1, NULL, 1152, 3, 4, '1', '搜索优化上线提测', 2, NULL, 1, '<p>自测通过</p>');
INSERT INTO `flow_record` VALUES (2, '2019-09-06 08:03:38', '2019-09-06 16:03:38', 1, NULL, 1152, 4, 5, '1', '搜索优化上线提测', 2, NULL, 1, '<p>测试环境测试通过</p>');
INSERT INTO `flow_record` VALUES (3, '2019-09-06 08:03:46', '2019-09-06 16:03:46', 1, NULL, 1152, 5, 6, '1', '搜索优化上线提测', 2, NULL, 1, '<p>PM验收通过</p>');
INSERT INTO `flow_record` VALUES (4, '2019-09-06 08:05:42', '2019-09-06 16:05:42', 2, NULL, 1152, 3, 4, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>自测通过</p>');
INSERT INTO `flow_record` VALUES (5, '2019-09-06 08:05:49', '2019-09-06 16:05:48', 2, NULL, 1152, 4, 3, '2', 'issue增加一个字段提测', 2, NULL, 1, '<p>冒烟不通过</p>');
INSERT INTO `flow_record` VALUES (6, '2019-09-06 08:08:21', '2019-09-06 16:08:20', 1, NULL, 1152, 6, 8, '1', '搜索优化上线提测', 2, NULL, 1, '<p>[依赖kafka]：</p><p>[PR]:</p><p>[数据库变动]：</p><p>[依赖ab实验]:</p><p>[依赖配置]:</p><p>[服务端上线顺序]</p><p>[OMS/MMS]</p><p>[需求JIRA]</p>');
INSERT INTO `flow_record` VALUES (7, '2019-09-06 08:08:31', '2019-09-06 16:08:31', 1, NULL, 1152, 8, 9, '1', '搜索优化上线提测', 2, NULL, 1, '<p>预发布环境验证通过</p>');
INSERT INTO `flow_record` VALUES (8, '2019-09-06 08:08:39', '2019-09-06 16:08:39', 1, NULL, 1152, 9, 11, '1', '搜索优化上线提测', 2, NULL, 1, '<p>PM预发布验证通过</p>');
INSERT INTO `flow_record` VALUES (9, '2019-09-06 08:08:43', '2019-09-06 16:08:43', 1, NULL, 1152, 11, 13, '1', '搜索优化上线提测', 2, NULL, 1, '<p>ok</p>');
INSERT INTO `flow_record` VALUES (10, '2019-09-06 08:08:58', '2019-09-06 16:08:58', 1, NULL, 1152, 13, 14, '1', '搜索优化上线提测', 2, NULL, 1, '<p>QA线上环境验证通过</p>');
INSERT INTO `flow_record` VALUES (11, '2019-09-06 08:09:05', '2019-09-06 16:09:04', 1, NULL, 1152, 14, 16, '1', '搜索优化上线提测', 2, NULL, 1, '<p>PM线上验证通过</p>');
INSERT INTO `flow_record` VALUES (12, '2019-09-06 08:09:08', '2019-09-06 16:09:08', 1, NULL, 1152, 16, 16, '1', '搜索优化上线提测', 2, NULL, 1, '<p>ok</p>');
INSERT INTO `flow_record` VALUES (13, '2019-09-06 08:23:09', '2019-09-06 16:23:08', 5, NULL, 1152, 3, 4, '1', '缺陷支持修改版本提测', 2, NULL, 1, '<p>自测通过</p>');
INSERT INTO `flow_record` VALUES (14, '2019-09-06 08:23:19', '2019-09-06 16:23:19', 4, NULL, 1152, 3, 4, '1', '增加taskcase导出功能', 2, NULL, 1, '<p>自测通过</p>');
INSERT INTO `flow_record` VALUES (15, '2019-09-06 08:23:27', '2019-09-06 16:23:27', 4, NULL, 1152, 4, 5, '1', '增加taskcase导出功能', 2, NULL, 1, '<p>测试环境验证通过</p>');
INSERT INTO `flow_record` VALUES (16, '2019-09-06 08:23:37', '2019-09-06 16:23:36', 3, NULL, 1152, 2, 4, '1', '分页优化提测', 2, NULL, 1, '<p>自测通过</p>');
INSERT INTO `flow_record` VALUES (17, '2019-09-06 08:23:45', '2019-09-06 16:23:44', 3, NULL, 1152, 4, 7, '1', '分页优化提测', 2, NULL, 1, '<p>测试环境测试通过</p>');
INSERT INTO `flow_record` VALUES (18, '2019-09-06 08:23:53', '2019-09-06 16:23:53', 3, NULL, 1152, 7, 11, '1', '分页优化提测', 2, NULL, 1, '<p>预发布验证通过</p>');
INSERT INTO `flow_record` VALUES (19, '2019-09-06 08:24:11', '2019-09-06 16:24:11', 2, NULL, 1152, 3, 4, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>自测通过</p>');
INSERT INTO `flow_record` VALUES (20, '2019-09-06 08:24:21', '2019-09-06 16:24:21', 2, NULL, 1152, 4, 5, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>测试环境测试通过</p>');
INSERT INTO `flow_record` VALUES (21, '2019-09-06 08:24:29', '2019-09-06 16:24:28', 2, NULL, 1152, 5, 8, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>PM验收通过</p>');
INSERT INTO `flow_record` VALUES (22, '2019-09-06 08:24:42', '2019-09-06 16:24:41', 2, NULL, 1152, 8, 9, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>QA预发布验收通过</p>');
INSERT INTO `flow_record` VALUES (23, '2019-09-06 08:24:55', '2019-09-06 16:24:54', 2, NULL, 1152, 9, 10, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>PM预发布验证通过</p>');
INSERT INTO `flow_record` VALUES (24, '2019-09-06 08:25:08', '2019-09-06 16:25:07', 2, NULL, 1152, 10, 13, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>灰度发包OK</p>');
INSERT INTO `flow_record` VALUES (25, '2019-09-06 08:25:20', '2019-09-06 16:25:19', 2, NULL, 1152, 13, 14, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>QA线上验证通过</p>');
INSERT INTO `flow_record` VALUES (26, '2019-09-06 08:25:28', '2019-09-06 16:25:28', 2, NULL, 1152, 14, 15, '1', 'issue增加一个字段提测', 2, NULL, 1, '<p>PM线上验证通过</p>');
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of flow_source
-- ----------------------------
BEGIN;
INSERT INTO `flow_source` VALUES (1, '2019-09-05 02:33:35', '2019-09-10 16:39:20', 2, 1152, '[]', 1, NULL);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interface_api_msg
-- ----------------------------
BEGIN;
INSERT INTO `interface_api_msg` VALUES (1, '2019-09-06 08:35:42', '2019-09-06 16:42:14', 1, '百度', NULL, 'data', '0', NULL, NULL, 'GET', '[{\"key\":null,\"param_type\":\"string\",\"remark\":null,\"value\":null}]', '', '[{\"key\":\"prod\",\"value\":\"pc_his\"},{\"key\":\"from\",\"value\":\"pc_web\"},{\"key\":\"json\",\"value\":\"1\"},{\"key\":\"sid\",\"value\":\"1463_21086_29073_29523_29518_29721_29568_29220_29460_22158\"},{\"key\":\"hisdata\",\"value\":\"%5B%7B%22time%22%3A1567222515%2C%22kw%22%3A%22%E5%AE%89%E5%BE%BD%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8%E7%BD%91%E4%B8%8A%E8%90%A5%E4%B8%9A%E5%8E%85%22%7D%2C%7B%22time%22%3A1567396095%2C%22kw%22%3A%22%E9%A5%BF%E4%BA%86%E4%B9%88%E7%BA%A2%E5%8C%85%E5%85%91%E6%8D%A2%E7%A0%81%22%7D%2C%7B%22time%22%3A1567410346%2C%22kw%22%3A%22%E4%B8%AD%E5%9B%BD%E7%9F%B3%E6%B2%B9%E5%92%8C%E4%B8%AD%E5%9B%BD%E7%9F%B3%E5%8C%96%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB%22%7D%2C%7B%22time%22%3A1567410358%2C%22kw%22%3A%22%E4%B8%AD%E5%9B%BD%E7%9F%B3%E6%B2%B9%E5%92%8C%E4%B8%AD%E5%9B%BD%E7%9F%B3%E5%8C%96%E5%93%AA%E4%B8%AA%E6%B2%B9%E5%A5%BD%22%7D%2C%7B%22time%22%3A1567426398%2C%22kw%22%3A%22%E5%A6%82%E4%BD%95%E9%80%9A%E8%BF%87%E7%94%B5%E8%84%91%E6%9F%A5%E7%9C%8B%E6%89%8B%E6%9C%BAapp%E5%86%85%E5%AD%97%E4%BD%93%E5%A4%A7%E5%B0%8F%22%7D%2C%7B%22time%22%3A1567476192%2C%22kw%22%3A%22%E5%91%A8%E7%90%A6%22%7D%2C%7B%22time%22%3A1567503035%2C%22kw%22%3A%22%E5%B0%8F%E7%B1%B3max4%22%7D%2C%7B%22time%22%3A1567517532%2C%22kw%22%3A%22jenkins%E8%AE%BE%E7%BD%AE%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1%22%2C%22fq%22%3A2%7D%2C%7B%22time%22%3A1567657102%2C%22kw%22%3A%22%E7%89%A9%E8%81%94%E7%BD%91%E6%98%AF%E4%BB%80%E4%B9%88%22%7D%2C%7B%22time%22%3A1567670897%2C%22kw%22%3A%22airtest%20ide%E4%B8%BA%E4%BB%80%E4%B9%88%E6%AF%94adb%20airtest%E6%85%A2%22%7D%5D\"},{\"key\":\"req\",\"value\":\"2\"},{\"key\":\"csor\",\"value\":\"0\"},{\"key\":\"cb\",\"value\":\"jQuery110206396234958706419_1567758662752\"},{\"key\":\"_\",\"value\":\"1567758662753\"},{\"key\":null,\"value\":null}]', '/sugrec', '[{\"key\":null,\"remark\":null,\"value\":null}]', '[{\"key\":null,\"value\":null}]', '[{\"key\":null,\"value\":null}]', 1, 1, 0);
INSERT INTO `interface_api_msg` VALUES (2, '2019-09-06 08:39:54', '2019-09-10 19:19:08', 2, '百度一下', NULL, 'data', '0', NULL, NULL, 'GET', '[{\"key\":null,\"param_type\":\"string\",\"remark\":null,\"value\":null}]', '', '[{\"key\":\"ie\",\"value\":\"utf-8\"},{\"key\":\"csq\",\"value\":\"1\"},{\"key\":\"pstg\",\"value\":\"20\"},{\"key\":\"mod\",\"value\":\"2\"},{\"key\":\"isbd\",\"value\":\"1\"},{\"key\":\"cqid\",\"value\":\"f00b9f0b0000d646\"},{\"key\":\"istc\",\"value\":\"769\"},{\"key\":\"ver\",\"value\":\"QtdvTgpZOrXaje7b6aDYyu9W1bV9WSGUDoG\"},{\"key\":\"chk\",\"value\":\"5d721a70\"},{\"key\":\"isid\",\"value\":\"DFA262942D061518\"},{\"key\":\"ie\",\"value\":\"utf-8\"},{\"key\":\"f\",\"value\":\"8\"},{\"key\":\"rsv_bp\",\"value\":\"1\"},{\"key\":\"rsv_idx\",\"value\":\"1\"},{\"key\":\"tn\",\"value\":\"baidu\"},{\"key\":\"wd\",\"value\":\"11\"},{\"key\":\"rsv_pq\",\"value\":\"905b042e000228aa\"},{\"key\":\"rsv_t\",\"value\":\"5e541XNlvvE%2FkL3KCcr30HbBLcp7tfrEPdWwwpuMe%2FqCtz7oBMUW4nVX5wo\"},{\"key\":\"rqlang\",\"value\":\"cn\"},{\"key\":\"rsv_enter\",\"value\":\"0\"},{\"key\":\"rsv_dl\",\"value\":\"tb\"},{\"key\":\"rsv_sug3\",\"value\":\"3\"},{\"key\":\"rsv_sug1\",\"value\":\"3\"},{\"key\":\"rsv_sug7\",\"value\":\"101\"},{\"key\":\"prefixsug\",\"value\":\"11\"},{\"key\":\"rsp\",\"value\":\"0\"},{\"key\":\"inputT\",\"value\":\"4603\"},{\"key\":\"rsv_sug4\",\"value\":\"7457\"},{\"key\":\"f4s\",\"value\":\"1\"},{\"key\":\"_ck\",\"value\":\"952.1.82.32.24.693.35\"},{\"key\":\"rsv_isid\",\"value\":\"1463_21086_29073_29523_29518_29721_29568_29220_29460_22158\"},{\"key\":\"isnop\",\"value\":\"1\"},{\"key\":\"rsv_stat\",\"value\":\"-2\"},{\"key\":\"rsv_bp\",\"value\":\"1\"},{\"key\":null,\"value\":null}]', '/s', '[{\"key\":null,\"remark\":null,\"value\":null}]', '[{\"key\":null,\"value\":null}]', '[{\"key\":null,\"value\":null}]', 1, 1, 0);
INSERT INTO `interface_api_msg` VALUES (3, '2019-09-10 11:18:20', '2019-09-10 19:18:20', 3, 'baidu', NULL, 'data', '0', NULL, NULL, 'GET', '[{\"key\":null,\"value\":null,\"param_type\":\"string\",\"remark\":null}]', '', '[{\"key\":\"\",\"value\":\"\"}]', 'baidu.com', '[{\"key\":null,\"value\":null,\"remark\":null}]', '[{\"key\":null,\"value\":null}]', '[{\"key\":null,\"value\":null}]', 1, 1, 0);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interface_case
-- ----------------------------
BEGIN;
INSERT INTO `interface_case` VALUES (1, '2019-09-06 08:40:57', '2019-09-06 16:42:05', 1, '百度', '', '[]', '[{\"key\":\"\",\"remark\":\"\",\"value\":\"\"}]', 1, 1, 1, 0);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interface_case_data
-- ----------------------------
BEGIN;
INSERT INTO `interface_case_data` VALUES (1, '2019-09-06 08:40:57', '2019-09-06 16:40:56', 0, 'true', '百度', NULL, NULL, 1, '[{\"key\": \"prod\", \"value\": \"pc_his\"}, {\"key\": \"from\", \"value\": \"pc_web\"}, {\"key\": \"json\", \"value\": \"1\"}, {\"key\": \"sid\", \"value\": \"1463_21086_29073_29523_29518_29721_29568_29220_29460_22158\"}, {\"key\": \"hisdata\", \"value\": \"%5B%7B%22time%22%3A1567222515%2C%22kw%22%3A%22%E5%AE%89%E5%BE%BD%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8%E7%BD%91%E4%B8%8A%E8%90%A5%E4%B8%9A%E5%8E%85%22%7D%2C%7B%22time%22%3A1567396095%2C%22kw%22%3A%22%E9%A5%BF%E4%BA%86%E4%B9%88%E7%BA%A2%E5%8C%85%E5%85%91%E6%8D%A2%E7%A0%81%22%7D%2C%7B%22time%22%3A1567410346%2C%22kw%22%3A%22%E4%B8%AD%E5%9B%BD%E7%9F%B3%E6%B2%B9%E5%92%8C%E4%B8%AD%E5%9B%BD%E7%9F%B3%E5%8C%96%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB%22%7D%2C%7B%22time%22%3A1567410358%2C%22kw%22%3A%22%E4%B8%AD%E5%9B%BD%E7%9F%B3%E6%B2%B9%E5%92%8C%E4%B8%AD%E5%9B%BD%E7%9F%B3%E5%8C%96%E5%93%AA%E4%B8%AA%E6%B2%B9%E5%A5%BD%22%7D%2C%7B%22time%22%3A1567426398%2C%22kw%22%3A%22%E5%A6%82%E4%BD%95%E9%80%9A%E8%BF%87%E7%94%B5%E8%84%91%E6%9F%A5%E7%9C%8B%E6%89%8B%E6%9C%BAapp%E5%86%85%E5%AD%97%E4%BD%93%E5%A4%A7%E5%B0%8F%22%7D%2C%7B%22time%22%3A1567476192%2C%22kw%22%3A%22%E5%91%A8%E7%90%A6%22%7D%2C%7B%22time%22%3A1567503035%2C%22kw%22%3A%22%E5%B0%8F%E7%B1%B3max4%22%7D%2C%7B%22time%22%3A1567517532%2C%22kw%22%3A%22jenkins%E8%AE%BE%E7%BD%AE%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1%22%2C%22fq%22%3A2%7D%2C%7B%22time%22%3A1567657102%2C%22kw%22%3A%22%E7%89%A9%E8%81%94%E7%BD%91%E6%98%AF%E4%BB%80%E4%B9%88%22%7D%2C%7B%22time%22%3A1567670897%2C%22kw%22%3A%22airtest%20ide%E4%B8%BA%E4%BB%80%E4%B9%88%E6%AF%94adb%20airtest%E6%85%A2%22%7D%5D\"}, {\"key\": \"req\", \"value\": \"2\"}, {\"key\": \"csor\", \"value\": \"0\"}, {\"key\": \"cb\", \"value\": \"jQuery110206396234958706419_1567758662752\"}, {\"key\": \"_\", \"value\": \"1567758662753\"}, {\"key\": null, \"value\": null}]', '[true, true]', '[true, true]', '', '[true, true]', '[{\"key\": null, \"remark\": null, \"value\": null}]', '[true, true]', '[{\"key\": null, \"value\": null}]', '[true, true]', 1, 1, 0);
INSERT INTO `interface_case_data` VALUES (2, '2019-09-06 08:40:57', '2019-09-06 16:40:56', 1, 'true', '百度一下', NULL, NULL, 1, '[{\"key\": \"ie\", \"value\": \"utf-8\"}, {\"key\": \"csq\", \"value\": \"1\"}, {\"key\": \"pstg\", \"value\": \"20\"}, {\"key\": \"mod\", \"value\": \"2\"}, {\"key\": \"isbd\", \"value\": \"1\"}, {\"key\": \"cqid\", \"value\": \"f00b9f0b0000d646\"}, {\"key\": \"istc\", \"value\": \"769\"}, {\"key\": \"ver\", \"value\": \"QtdvTgpZOrXaje7b6aDYyu9W1bV9WSGUDoG\"}, {\"key\": \"chk\", \"value\": \"5d721a70\"}, {\"key\": \"isid\", \"value\": \"DFA262942D061518\"}, {\"key\": \"ie\", \"value\": \"utf-8\"}, {\"key\": \"f\", \"value\": \"8\"}, {\"key\": \"rsv_bp\", \"value\": \"1\"}, {\"key\": \"rsv_idx\", \"value\": \"1\"}, {\"key\": \"tn\", \"value\": \"baidu\"}, {\"key\": \"wd\", \"value\": \"11\"}, {\"key\": \"rsv_pq\", \"value\": \"905b042e000228aa\"}, {\"key\": \"rsv_t\", \"value\": \"5e541XNlvvE%2FkL3KCcr30HbBLcp7tfrEPdWwwpuMe%2FqCtz7oBMUW4nVX5wo\"}, {\"key\": \"rqlang\", \"value\": \"cn\"}, {\"key\": \"rsv_enter\", \"value\": \"0\"}, {\"key\": \"rsv_dl\", \"value\": \"tb\"}, {\"key\": \"rsv_sug3\", \"value\": \"3\"}, {\"key\": \"rsv_sug1\", \"value\": \"3\"}, {\"key\": \"rsv_sug7\", \"value\": \"101\"}, {\"key\": \"prefixsug\", \"value\": \"11\"}, {\"key\": \"rsp\", \"value\": \"0\"}, {\"key\": \"inputT\", \"value\": \"4603\"}, {\"key\": \"rsv_sug4\", \"value\": \"7457\"}, {\"key\": \"f4s\", \"value\": \"1\"}, {\"key\": \"_ck\", \"value\": \"952.1.82.32.24.693.35\"}, {\"key\": \"rsv_isid\", \"value\": \"1463_21086_29073_29523_29518_29721_29568_29220_29460_22158\"}, {\"key\": \"isnop\", \"value\": \"1\"}, {\"key\": \"rsv_stat\", \"value\": \"-2\"}, {\"key\": \"rsv_bp\", \"value\": \"1\"}, {\"key\": null, \"value\": null}]', '[true, true]', '[true, true]', '', '[true, true]', '[{\"key\": null, \"remark\": null, \"value\": null}]', '[true, true]', '[{\"key\": null, \"value\": null}]', '[true, true]', 1, 2, 0);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interface_case_set
-- ----------------------------
BEGIN;
INSERT INTO `interface_case_set` VALUES (1, '2019-09-06 08:40:27', '2019-09-06 16:40:26', 1, '百度', 1, 0);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interface_module
-- ----------------------------
BEGIN;
INSERT INTO `interface_module` VALUES (1, '2019-09-06 08:34:06', '2019-09-06 16:34:05', 1, '百度', 1, 1, 0);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of interface_project
-- ----------------------------
BEGIN;
INSERT INTO `interface_project` VALUES (1, '2019-09-06 08:32:51', '2019-09-06 16:32:51', 'baidu', '', 0, 1, NULL, '[\"https://www.baidu.com\"]', '[]', '[]', '[]', 'first', NULL, '[]', '[]', 2, 1152);
INSERT INTO `interface_project` VALUES (2, '2019-09-10 08:50:21', '2019-09-10 16:50:21', 'test01', '', 0, 1, NULL, '[]', '[]', '[]', '[]', 'first', NULL, '[]', '[]', 2, 1155);
COMMIT;

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
  PRIMARY KEY (`id`) USING BTREE,
  KEY `creator` (`creator`) USING BTREE,
  KEY `modifier` (`modifier`) USING BTREE,
  KEY `handler` (`handler`) USING BTREE,
  CONSTRAINT `issue_ibfk_1` FOREIGN KEY (`creator`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_ibfk_2` FOREIGN KEY (`modifier`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_ibfk_3` FOREIGN KEY (`handler`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of issue
-- ----------------------------
BEGIN;
INSERT INTO `issue` VALUES (1, '2019-09-04 06:59:30', '2019-09-04 14:59:38', 'T1', 2, NULL, 1, NULL, 1152, 1152, NULL, NULL, 0, 0, 0, NULL, '缺陷测试', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 25, 1, NULL);
INSERT INTO `issue` VALUES (2, '2019-09-06 07:39:14', '2019-09-06 15:44:25', 'T2', 2, 1, 2, 1, 1152, 1152, 1152, 0, 0, 2, 1, NULL, '【功能点】 主要问题描述，如果是偶现请备注', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, 1, 15, 2, NULL);
INSERT INTO `issue` VALUES (3, '2019-09-06 08:10:20', '2019-09-10 17:27:41', 'T3', 2, 6, 2, 4, 1152, 1152, 1155, 0, 0, 1, 1, NULL, 'issue列表页分页功能错误', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 1:17:21', NULL, NULL, 20, 5, NULL);
INSERT INTO `issue` VALUES (4, '2019-09-06 08:11:14', '2019-09-10 19:49:16', 'T4', 2, 6, 2, 3, 1152, NULL, 1155, 0, 0, 2, 2, NULL, 'taskcase无法导出excel', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 1, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 3:38:02', NULL, NULL, 15, 4, NULL);
INSERT INTO `issue` VALUES (5, '2019-09-06 08:11:59', '2019-09-10 19:49:13', 'T5', 2, 6, 2, 4, 1152, NULL, 1155, 1, 0, 3, 2, NULL, '搜索界面显示优化建议', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 4, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '0:00:07', '4 days, 3:37:07', NULL, 10, 3, NULL);
INSERT INTO `issue` VALUES (6, '2019-09-06 08:14:42', '2019-09-10 18:28:02', 'T6', 2, 6, 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue` VALUES (7, '2019-09-06 08:18:36', '2019-09-10 19:49:18', 'T7', 2, 6, 2, 7, 1152, 1152, 1155, 0, 0, 2, 2, NULL, '按照标题搜索，不要区分大小写', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 1, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 3:30:42', NULL, NULL, 15, NULL, NULL);
COMMIT;

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
  PRIMARY KEY (`id`) USING BTREE,
  KEY `creator` (`creator`) USING BTREE,
  KEY `modifier` (`modifier`) USING BTREE,
  KEY `handler` (`handler`) USING BTREE,
  CONSTRAINT `issue_record_ibfk_1` FOREIGN KEY (`creator`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_record_ibfk_2` FOREIGN KEY (`modifier`) REFERENCES `user` (`id`),
  CONSTRAINT `issue_record_ibfk_3` FOREIGN KEY (`handler`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of issue_record
-- ----------------------------
BEGIN;
INSERT INTO `issue_record` VALUES (1, '2019-09-04 06:59:30', '2019-09-04 14:59:29', 1, 'T1', 2, NULL, 1, NULL, 1152, NULL, NULL, NULL, 0, 0, 0, NULL, '缺陷测试', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 25, NULL, NULL);
INSERT INTO `issue_record` VALUES (2, '2019-09-04 06:59:39', '2019-09-04 14:59:38', 1, 'T1', 2, NULL, 1, NULL, 1152, 1152, NULL, NULL, 0, 0, 0, NULL, '缺陷测试', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 25, 1, NULL);
INSERT INTO `issue_record` VALUES (3, '2019-09-06 07:39:14', '2019-09-06 15:39:13', 2, 'T2', 2, '1', 2, 1, 1152, NULL, 1152, 0, 0, 2, 1, NULL, '标题： 【功能点】 主要问题描述，如果是偶现请备注', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, 1, 15, 1, NULL);
INSERT INTO `issue_record` VALUES (4, '2019-09-06 07:44:16', '2019-09-06 15:44:15', 2, 'T2', 2, '1', 2, 1, 1152, 1152, 1152, 0, 0, 2, 1, NULL, '标题： 【功能点】 主要问题描述，如果是偶现请备注', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, 1, 15, 2, NULL);
INSERT INTO `issue_record` VALUES (5, '2019-09-06 07:44:26', '2019-09-06 15:44:25', 2, 'T2', 2, '1', 2, 1, 1152, 1152, 1152, 0, 0, 2, 1, NULL, '【功能点】 主要问题描述，如果是偶现请备注', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, 1, 15, 2, NULL);
INSERT INTO `issue_record` VALUES (6, '2019-09-06 08:10:20', '2019-09-06 16:10:20', 3, 'T3', 2, '6', 2, 4, 1152, NULL, 1155, 0, 0, 1, 1, NULL, 'issue列表页分页功能错误', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 20, 5, NULL);
INSERT INTO `issue_record` VALUES (7, '2019-09-06 08:10:27', '2019-09-06 16:10:27', 3, 'T3', 2, '6', 2, 4, 1152, 1152, 1155, 0, 0, 1, 1, NULL, 'issue列表页分页功能错误', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 20, 5, NULL);
INSERT INTO `issue_record` VALUES (8, '2019-09-06 08:11:14', '2019-09-06 16:11:14', 4, 'T4', 2, '6', 2, 3, 1152, NULL, 1155, 0, 0, 2, 2, NULL, 'taskcase无法导出excel', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, 4, NULL);
INSERT INTO `issue_record` VALUES (9, '2019-09-06 08:11:59', '2019-09-06 16:11:59', 5, 'T5', 2, '6', 2, 4, 1152, NULL, 1155, 1, 0, 3, 2, NULL, '搜索界面显示优化建议', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 10, 3, NULL);
INSERT INTO `issue_record` VALUES (10, '2019-09-06 08:12:06', '2019-09-06 16:12:06', 5, 'T5', 2, '6', 2, 4, 1152, 1152, 1155, 1, 0, 3, 2, NULL, '搜索界面显示优化建议', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '0:00:07', NULL, NULL, 10, 3, NULL);
INSERT INTO `issue_record` VALUES (11, '2019-09-06 08:12:10', '2019-09-06 16:12:09', 4, 'T4', 2, '6', 2, 3, 1152, 1152, 1155, 0, 0, 2, 2, NULL, 'taskcase无法导出excel', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 4, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, 4, NULL);
INSERT INTO `issue_record` VALUES (12, '2019-09-06 08:14:42', '2019-09-06 16:14:42', 6, 'T6', 2, '6', 2, 4, 1152, NULL, 1155, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (13, '2019-09-06 08:14:54', '2019-09-06 16:14:54', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1155, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (14, '2019-09-06 08:18:36', '2019-09-06 16:18:36', 7, 'T7', 2, '6', 2, 7, 1152, NULL, 1155, 0, 0, 2, 2, NULL, '按照标题搜索，不要区分大小写', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 15, NULL, NULL);
INSERT INTO `issue_record` VALUES (15, '2019-09-06 08:18:43', '2019-09-06 16:18:43', 7, 'T7', 2, '6', 2, 7, 1152, 1152, 1155, 0, 0, 2, 2, NULL, '按照标题搜索，不要区分大小写', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, NULL, NULL);
INSERT INTO `issue_record` VALUES (16, '2019-09-10 08:13:33', '2019-09-10 16:13:32', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1155, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (17, '2019-09-10 08:13:37', '2019-09-10 16:13:37', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1155, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (18, '2019-09-10 08:31:47', '2019-09-10 16:31:46', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (19, '2019-09-10 08:33:15', '2019-09-10 16:33:15', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (20, '2019-09-10 08:33:49', '2019-09-10 16:33:48', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (21, '2019-09-10 08:36:49', '2019-09-10 16:36:48', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (22, '2019-09-10 08:36:49', '2019-09-10 16:36:49', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (23, '2019-09-10 08:37:23', '2019-09-10 16:37:23', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (24, '2019-09-10 08:37:26', '2019-09-10 16:37:25', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (25, '2019-09-10 09:22:32', '2019-09-10 17:22:31', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (26, '2019-09-10 09:22:34', '2019-09-10 17:22:34', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (27, '2019-09-10 09:27:42', '2019-09-10 17:27:41', 3, 'T3', 2, '6', 2, 4, 1152, 1152, 1155, 0, 0, 1, 1, NULL, 'issue列表页分页功能错误', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 1:17:21', NULL, NULL, 20, 5, NULL);
INSERT INTO `issue_record` VALUES (28, '2019-09-10 10:28:01', '2019-09-10 18:28:01', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (29, '2019-09-10 10:28:03', '2019-09-10 18:28:02', 6, 'T6', 2, '6', 2, 4, 1152, 1152, 1152, 0, 0, 2, 1, NULL, 'issue列表字段不符合设计要求', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', '点点点', NULL, NULL, NULL, 15, 6, NULL);
INSERT INTO `issue_record` VALUES (30, '2019-09-10 11:49:12', '2019-09-10 19:49:12', 7, 'T7', 2, '6', 2, 7, 1152, 1152, 1155, 0, 0, 2, 2, NULL, '按照标题搜索，不要区分大小写', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 0, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 3:30:36', NULL, NULL, 15, NULL, NULL);
INSERT INTO `issue_record` VALUES (31, '2019-09-10 11:49:14', '2019-09-10 19:49:13', 5, 'T5', 2, '6', 2, 4, 1152, 1152, 1155, 1, 0, 3, 2, NULL, '搜索界面显示优化建议', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 4, 0, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '0:00:07', '4 days, 3:37:07', NULL, 10, 3, NULL);
INSERT INTO `issue_record` VALUES (32, '2019-09-10 11:49:15', '2019-09-10 19:49:15', 4, 'T4', 2, '6', 2, 3, 1152, 1152, 1155, 0, 0, 2, 2, NULL, 'taskcase无法导出excel', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 1, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, NULL, NULL, NULL, 15, 4, NULL);
INSERT INTO `issue_record` VALUES (33, '2019-09-10 11:49:16', '2019-09-10 19:49:16', 4, 'T4', 2, '6', 2, 3, 1152, 1152, 1155, 0, 0, 2, 2, NULL, 'taskcase无法导出excel', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 1, 0, NULL, '<p>标题：&nbsp;【功能点】&nbsp;主要问题描述，如果是偶现请备注<br><br>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 3:38:02', NULL, NULL, 15, 4, NULL);
INSERT INTO `issue_record` VALUES (34, '2019-09-10 11:49:18', '2019-09-10 19:49:17', 7, 'T7', 2, '6', 2, 7, 1152, 1152, 1155, 0, 0, 2, 2, NULL, '按照标题搜索，不要区分大小写', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 2, 1, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 3:30:36', NULL, NULL, 15, NULL, NULL);
INSERT INTO `issue_record` VALUES (35, '2019-09-10 11:49:19', '2019-09-10 19:49:18', 7, 'T7', 2, '6', 2, 7, 1152, 1152, 1155, 0, 0, 2, 2, NULL, '按照标题搜索，不要区分大小写', '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 3, 1, 0, NULL, '<p>描述：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;环境：&nbsp;测试/线上<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;前提：&nbsp;前置条件<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发生步骤：&nbsp;&nbsp;详细描述发生的步骤，<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预期：&nbsp;预期表现形式<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实际结果：</p>', NULL, '4 days, 3:30:42', NULL, NULL, 15, NULL, NULL);
COMMIT;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of requirement
-- ----------------------------
BEGIN;
INSERT INTO `requirement` VALUES (1, '2019-09-04 06:59:08', '2019-09-04 14:59:07', '需求测试', 2, NULL, NULL, 1152, 1152, NULL, 1, 0, '<p>需求测试</p>', NULL, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement` VALUES (2, '2019-09-06 07:40:32', '2019-09-06 15:55:52', '云测平台3.0版本需求', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、UI页面优化</p><p>2、导出功能增加筛选的功能</p><p>3、bug fix</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 1, '180', NULL, '<p>高价值的预期值：次日留存达到XXX</p>', 2, NULL);
INSERT INTO `requirement` VALUES (3, '2019-09-06 07:55:06', '2019-09-06 15:56:01', '搜索页面优化', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、当前搜索页面会由于浏览器的缩放，导致搜索词和输入框有点挤，优化一下</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement` VALUES (4, '2019-09-06 07:58:05', '2019-09-06 16:12:20', '增加taskcase导出功能', 2, '2', 0, 1152, 1152, 1152, 4, 0, '<p>增加taskcase导出功能</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement` VALUES (5, '2019-09-06 07:58:40', '2019-09-06 16:04:14', '分页优化', 2, '2', 1, 1152, 1152, 1152, 2, 0, '<p>分页优化</p>', 2, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement` VALUES (6, '2019-09-06 07:59:37', '2019-09-10 18:04:28', 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 2, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement` VALUES (7, '2019-09-06 08:21:29', '2019-09-06 16:21:28', '缺陷支持修改版本', 2, '1', 1, 1152, 1152, 1155, 1, 0, '<p>需求的具体描述</p><p>需求的具体描述</p><p>需求的具体描述</p><p>需求的具体描述</p><p>需求的具体描述</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of requirement_bind_case
-- ----------------------------
BEGIN;
INSERT INTO `requirement_bind_case` VALUES (1, 6, 8, '2019-09-06 08:01:38', '2019-09-06 16:01:38', 0);
COMMIT;

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of requirement_record
-- ----------------------------
BEGIN;
INSERT INTO `requirement_record` VALUES (1, '2019-09-04 06:59:08', '2019-09-04 14:59:07', 1, '需求测试', 2, NULL, NULL, 1152, 1152, NULL, 1, 0, '<p>需求测试</p>', NULL, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (2, '2019-09-06 07:40:32', '2019-09-06 15:40:31', 2, '需求标题', 2, '2', 1, 1152, 1152, 1152, 0, 0, NULL, 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 1, NULL, '<p>高价值的预期值：次日留存达到XXX</p>', NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (3, '2019-09-06 07:41:02', '2019-09-06 15:41:02', 2, '需求标题', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、需求描述</p><p>2、需求详情</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 1, '180', '<p>高价值的预期值：次日留存达到XXX</p>', NULL, 2, NULL);
INSERT INTO `requirement_record` VALUES (4, '2019-09-06 07:41:41', '2019-09-06 15:41:40', 2, '云测平台3.0版本需求', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、需求描述</p><p>2、需求详情</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 1, '180', '<p>高价值的预期值：次日留存达到XXX</p>', NULL, 2, NULL);
INSERT INTO `requirement_record` VALUES (5, '2019-09-06 07:43:29', '2019-09-06 15:43:28', 2, '云测平台3.0版本需求', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、UI页面优化</p><p>2、导出功能增加筛选的功能</p><p>3、bug fix</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 1, '180', '<p>高价值的预期值：次日留存达到XXX</p>', NULL, 2, NULL);
INSERT INTO `requirement_record` VALUES (6, '2019-09-06 07:55:06', '2019-09-06 15:55:06', 3, '搜索页面优化', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、当前搜索页面会由于浏览器的缩放，导致搜索词和输入框有点挤，优化一下</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (7, '2019-09-06 07:55:52', '2019-09-06 15:55:52', 2, '云测平台3.0版本需求', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、UI页面优化</p><p>2、导出功能增加筛选的功能</p><p>3、bug fix</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 1, '180', '<p>高价值的预期值：次日留存达到XXX</p>', NULL, 2, NULL);
INSERT INTO `requirement_record` VALUES (8, '2019-09-06 07:56:01', '2019-09-06 15:56:01', 3, '搜索页面优化', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、当前搜索页面会由于浏览器的缩放，导致搜索词和输入框有点挤，优化一下</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (9, '2019-09-06 07:58:05', '2019-09-06 15:58:04', 4, '增加taskcase导出功能', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>增加taskcase导出功能</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (10, '2019-09-06 07:58:40', '2019-09-06 15:58:40', 5, '分页优化', 2, '2', 1, 1152, 1152, 1152, 2, 0, '<p>分页优化</p>', 2, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (11, '2019-09-06 07:59:37', '2019-09-06 15:59:37', 6, 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (12, '2019-09-06 08:01:38', '2019-09-06 16:01:38', 6, 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (13, '2019-09-06 08:04:14', '2019-09-06 16:04:14', 6, 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (14, '2019-09-06 08:04:14', '2019-09-06 16:04:14', 5, '分页优化', 2, '2', 1, 1152, 1152, 1152, 2, 0, '<p>分页优化</p>', 2, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (15, '2019-09-06 08:04:14', '2019-09-06 16:04:14', 4, '增加taskcase导出功能', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>增加taskcase导出功能</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (16, '2019-09-06 08:12:20', '2019-09-06 16:12:20', 4, '增加taskcase导出功能', 2, '2', 0, 1152, 1152, 1152, 4, 0, '<p>增加taskcase导出功能</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (17, '2019-09-06 08:21:29', '2019-09-06 16:21:28', 7, '缺陷支持修改版本', 2, '1', 1, 1152, 1152, 1155, 1, 0, '<p>需求的具体描述</p><p>需求的具体描述</p><p>需求的具体描述</p><p>需求的具体描述</p><p>需求的具体描述</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (18, '2019-09-10 10:04:25', '2019-09-10 18:04:24', 6, 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (19, '2019-09-10 10:04:27', '2019-09-10 18:04:27', 6, 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_record` VALUES (20, '2019-09-10 10:04:29', '2019-09-10 18:04:28', 6, 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 2, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 2, NULL, 2, NULL, NULL, NULL, NULL, NULL);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of requirement_review
-- ----------------------------
BEGIN;
INSERT INTO `requirement_review` VALUES (1, '2019-09-06 07:55:48', '2019-09-06 15:55:52', 1, 2, '云测平台3.0版本需求', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、UI页面优化</p><p>2、导出功能增加筛选的功能</p><p>3、bug fix</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 1, '180', NULL, '<p>高价值的预期值：次日留存达到XXX</p>', 2);
INSERT INTO `requirement_review` VALUES (2, '2019-09-06 07:55:58', '2019-09-06 15:56:01', 2, 3, '搜索页面优化', 2, '2', 1, 1152, 1152, 1152, 0, 0, '<p>1、当前搜索页面会由于浏览器的缩放，导致搜索词和输入框有点挤，优化一下</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_review` VALUES (3, '2019-09-06 08:04:10', '2019-09-06 16:04:14', 3, 4, '增加taskcase导出功能', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>增加taskcase导出功能</p>', 1, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_review` VALUES (4, '2019-09-06 08:04:10', '2019-09-06 16:04:14', 3, 5, '分页优化', 2, '2', 1, 1152, 1152, 1152, 2, 0, '<p>分页优化</p>', 2, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL);
INSERT INTO `requirement_review` VALUES (5, '2019-09-06 08:04:10', '2019-09-06 16:04:14', 3, 6, 'issue增加一个字段', 2, '2', 0, 1152, 1152, 1152, 1, 0, '<p>issue增加一个字段</p>', 0, '{\"images\":[],\"files\":[],\"videos\":[]}', NULL, 1, 0, 1, NULL, 2, NULL, NULL, NULL, NULL);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of review
-- ----------------------------
BEGIN;
INSERT INTO `review` VALUES (1, '2019-09-06 07:55:48', '2019-09-06 15:55:52', NULL, '2', 2, 1152, 1152, 'admin', 0, NULL, '', 1, 2, 2);
INSERT INTO `review` VALUES (2, '2019-09-06 07:55:58', '2019-09-06 15:56:01', NULL, '3', 2, 1152, 1152, 'admin', 0, NULL, '', 1, 2, 2);
INSERT INTO `review` VALUES (3, '2019-09-06 08:04:10', '2019-09-06 16:04:14', NULL, '4,5,6', 2, 1152, 1152, 'admin', 0, NULL, '', 1, 2, 2);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=3316 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role_bind_ability
-- ----------------------------
BEGIN;
INSERT INTO `role_bind_ability` VALUES (280, '2019-08-21 19:28:24', '2019-08-21 19:28:24', 38, 8);
INSERT INTO `role_bind_ability` VALUES (281, '2019-08-21 19:28:24', '2019-08-21 19:28:24', 38, 7);
INSERT INTO `role_bind_ability` VALUES (2838, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 3);
INSERT INTO `role_bind_ability` VALUES (2839, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 2);
INSERT INTO `role_bind_ability` VALUES (2840, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 1);
INSERT INTO `role_bind_ability` VALUES (2841, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 4);
INSERT INTO `role_bind_ability` VALUES (2842, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 5);
INSERT INTO `role_bind_ability` VALUES (2843, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 6);
INSERT INTO `role_bind_ability` VALUES (2844, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 7);
INSERT INTO `role_bind_ability` VALUES (2845, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 8);
INSERT INTO `role_bind_ability` VALUES (2846, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 9);
INSERT INTO `role_bind_ability` VALUES (2847, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 10);
INSERT INTO `role_bind_ability` VALUES (2848, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 11);
INSERT INTO `role_bind_ability` VALUES (2849, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 12);
INSERT INTO `role_bind_ability` VALUES (2850, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 13);
INSERT INTO `role_bind_ability` VALUES (2851, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 14);
INSERT INTO `role_bind_ability` VALUES (2852, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 15);
INSERT INTO `role_bind_ability` VALUES (2853, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 16);
INSERT INTO `role_bind_ability` VALUES (2854, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 31);
INSERT INTO `role_bind_ability` VALUES (2855, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 17);
INSERT INTO `role_bind_ability` VALUES (2856, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 18);
INSERT INTO `role_bind_ability` VALUES (2857, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 19);
INSERT INTO `role_bind_ability` VALUES (2858, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 21);
INSERT INTO `role_bind_ability` VALUES (2859, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 20);
INSERT INTO `role_bind_ability` VALUES (2860, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 22);
INSERT INTO `role_bind_ability` VALUES (2861, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 23);
INSERT INTO `role_bind_ability` VALUES (2862, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 24);
INSERT INTO `role_bind_ability` VALUES (2863, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 27);
INSERT INTO `role_bind_ability` VALUES (2864, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 25);
INSERT INTO `role_bind_ability` VALUES (2865, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 26);
INSERT INTO `role_bind_ability` VALUES (2866, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 28);
INSERT INTO `role_bind_ability` VALUES (2867, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 29);
INSERT INTO `role_bind_ability` VALUES (2868, '2019-08-22 18:41:56', '2019-08-22 18:41:55', 6, 30);
INSERT INTO `role_bind_ability` VALUES (3072, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 1);
INSERT INTO `role_bind_ability` VALUES (3073, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 5);
INSERT INTO `role_bind_ability` VALUES (3074, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 6);
INSERT INTO `role_bind_ability` VALUES (3075, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 4);
INSERT INTO `role_bind_ability` VALUES (3076, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 7);
INSERT INTO `role_bind_ability` VALUES (3077, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 10);
INSERT INTO `role_bind_ability` VALUES (3078, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 13);
INSERT INTO `role_bind_ability` VALUES (3079, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 17);
INSERT INTO `role_bind_ability` VALUES (3080, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 18);
INSERT INTO `role_bind_ability` VALUES (3081, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 16);
INSERT INTO `role_bind_ability` VALUES (3082, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 19);
INSERT INTO `role_bind_ability` VALUES (3083, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 22);
INSERT INTO `role_bind_ability` VALUES (3084, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 25);
INSERT INTO `role_bind_ability` VALUES (3085, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 26);
INSERT INTO `role_bind_ability` VALUES (3086, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 28);
INSERT INTO `role_bind_ability` VALUES (3087, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 29);
INSERT INTO `role_bind_ability` VALUES (3088, '2019-08-22 19:27:13', '2019-08-22 19:27:12', 5, 30);
INSERT INTO `role_bind_ability` VALUES (3089, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 1);
INSERT INTO `role_bind_ability` VALUES (3090, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 4);
INSERT INTO `role_bind_ability` VALUES (3091, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 7);
INSERT INTO `role_bind_ability` VALUES (3092, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 10);
INSERT INTO `role_bind_ability` VALUES (3093, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 13);
INSERT INTO `role_bind_ability` VALUES (3094, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 16);
INSERT INTO `role_bind_ability` VALUES (3095, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 19);
INSERT INTO `role_bind_ability` VALUES (3096, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 22);
INSERT INTO `role_bind_ability` VALUES (3097, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 25);
INSERT INTO `role_bind_ability` VALUES (3098, '2019-08-22 20:08:13', '2019-08-22 20:08:12', 4, 28);
INSERT INTO `role_bind_ability` VALUES (3268, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 1);
INSERT INTO `role_bind_ability` VALUES (3269, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 2);
INSERT INTO `role_bind_ability` VALUES (3270, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 3);
INSERT INTO `role_bind_ability` VALUES (3271, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 4);
INSERT INTO `role_bind_ability` VALUES (3272, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 5);
INSERT INTO `role_bind_ability` VALUES (3273, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 6);
INSERT INTO `role_bind_ability` VALUES (3274, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 7);
INSERT INTO `role_bind_ability` VALUES (3275, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 8);
INSERT INTO `role_bind_ability` VALUES (3276, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 9);
INSERT INTO `role_bind_ability` VALUES (3277, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 10);
INSERT INTO `role_bind_ability` VALUES (3278, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 11);
INSERT INTO `role_bind_ability` VALUES (3279, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 12);
INSERT INTO `role_bind_ability` VALUES (3280, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 13);
INSERT INTO `role_bind_ability` VALUES (3281, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 14);
INSERT INTO `role_bind_ability` VALUES (3282, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 15);
INSERT INTO `role_bind_ability` VALUES (3283, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 16);
INSERT INTO `role_bind_ability` VALUES (3284, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 31);
INSERT INTO `role_bind_ability` VALUES (3285, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 17);
INSERT INTO `role_bind_ability` VALUES (3286, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 18);
INSERT INTO `role_bind_ability` VALUES (3287, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 19);
INSERT INTO `role_bind_ability` VALUES (3288, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 20);
INSERT INTO `role_bind_ability` VALUES (3289, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 21);
INSERT INTO `role_bind_ability` VALUES (3290, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 22);
INSERT INTO `role_bind_ability` VALUES (3291, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 23);
INSERT INTO `role_bind_ability` VALUES (3292, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 24);
INSERT INTO `role_bind_ability` VALUES (3293, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 26);
INSERT INTO `role_bind_ability` VALUES (3294, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 25);
INSERT INTO `role_bind_ability` VALUES (3295, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 27);
INSERT INTO `role_bind_ability` VALUES (3296, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 28);
INSERT INTO `role_bind_ability` VALUES (3297, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 29);
INSERT INTO `role_bind_ability` VALUES (3298, '2019-08-29 19:51:08', '2019-08-29 19:51:08', 3, 30);
INSERT INTO `role_bind_ability` VALUES (3299, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 1);
INSERT INTO `role_bind_ability` VALUES (3300, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 8);
INSERT INTO `role_bind_ability` VALUES (3301, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 7);
INSERT INTO `role_bind_ability` VALUES (3302, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 10);
INSERT INTO `role_bind_ability` VALUES (3303, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 11);
INSERT INTO `role_bind_ability` VALUES (3304, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 13);
INSERT INTO `role_bind_ability` VALUES (3305, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 16);
INSERT INTO `role_bind_ability` VALUES (3306, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 31);
INSERT INTO `role_bind_ability` VALUES (3307, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 17);
INSERT INTO `role_bind_ability` VALUES (3308, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 20);
INSERT INTO `role_bind_ability` VALUES (3309, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 19);
INSERT INTO `role_bind_ability` VALUES (3310, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 23);
INSERT INTO `role_bind_ability` VALUES (3311, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 22);
INSERT INTO `role_bind_ability` VALUES (3312, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 25);
INSERT INTO `role_bind_ability` VALUES (3313, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 26);
INSERT INTO `role_bind_ability` VALUES (3314, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 28);
INSERT INTO `role_bind_ability` VALUES (3315, '2019-09-03 12:48:51', '2019-09-03 20:48:51', 2, 29);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of task
-- ----------------------------
BEGIN;
INSERT INTO `task` VALUES (1, '2019-09-04 06:57:22', '2019-09-04 14:57:21', '测试任务', '', NULL, '自动化测试', '功能测试', 0, 1152, 1152, 2, '2019-09-04 00:00:00', '2019-09-05 00:00:00', 2, 1, NULL, '[4, 3, 2, 1]', NULL, '', NULL);
INSERT INTO `task` VALUES (2, '2019-09-04 12:34:04', '2019-09-04 20:34:03', '任务一', '1、\n2、', NULL, '人工测试', '功能测试', 0, 1152, 1154, 2, '2019-09-04 00:00:00', '2019-09-06 00:00:00', 2, 2, NULL, '[4, 3, 2, 1]', NULL, '', NULL);
INSERT INTO `task` VALUES (3, '2019-09-04 12:34:31', '2019-09-10 16:37:25', '任务二', '1、\n2、', '', '人工测试', '兼容性测试', 0, 1152, 1154, 2, '2019-09-04 00:00:00', '2019-09-06 00:00:00', 2, 2, NULL, '[4, 3, 2, 1]', '{\"image\":\"\",\"files\":[]}', '', NULL);
INSERT INTO `task` VALUES (4, '2019-09-06 08:13:28', '2019-09-10 17:57:31', '流程管理模块执行用例', '流程管理模块执行用例', '', '人工测试', '功能测试', 0, 1152, 1154, 1, '2019-09-05 00:00:00', '2019-09-06 00:00:00', 2, 2, NULL, '[7, 6, 5]', '{\"image\":\"\",\"files\":[]}', '', NULL);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of task_case
-- ----------------------------
BEGIN;
INSERT INTO `task_case` VALUES (1, '2019-09-04 06:57:22', '2019-09-04 14:58:10', 1, NULL, NULL, 1152, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 4, NULL, 1, 2);
INSERT INTO `task_case` VALUES (2, '2019-09-04 06:57:22', '2019-09-04 14:58:09', 1, NULL, NULL, 1152, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 3, NULL, 1, 2);
INSERT INTO `task_case` VALUES (3, '2019-09-04 06:57:22', '2019-09-04 14:58:08', 1, NULL, NULL, 1152, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 3, NULL, 1, 2);
INSERT INTO `task_case` VALUES (4, '2019-09-04 06:57:22', '2019-09-04 14:58:07', 1, NULL, NULL, 1152, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 3, NULL, 1, 2);
INSERT INTO `task_case` VALUES (5, '2019-09-04 12:34:04', '2019-09-04 20:34:03', 2, NULL, NULL, NULL, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case` VALUES (6, '2019-09-04 12:34:04', '2019-09-04 20:34:03', 2, NULL, NULL, NULL, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case` VALUES (7, '2019-09-04 12:34:04', '2019-09-04 20:34:04', 2, NULL, NULL, NULL, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case` VALUES (8, '2019-09-04 12:34:04', '2019-09-04 20:34:04', 2, NULL, NULL, NULL, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case` VALUES (9, '2019-09-04 12:34:31', '2019-09-04 20:38:02', 3, NULL, NULL, NULL, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 4, NULL, 2, 2);
INSERT INTO `task_case` VALUES (10, '2019-09-04 12:34:31', '2019-09-04 20:38:01', 3, NULL, NULL, NULL, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case` VALUES (11, '2019-09-04 12:34:31', '2019-09-04 20:38:00', 3, NULL, NULL, NULL, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case` VALUES (12, '2019-09-04 12:34:31', '2019-09-04 20:37:59', 3, NULL, NULL, NULL, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case` VALUES (13, '2019-09-06 08:13:28', '2019-09-06 16:13:39', 4, NULL, NULL, NULL, 1, NULL, '取消删除流程', 'TC7', 7, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击取消按钮\",\"expect\":\"删除确认框收起，没有执行删除操作\"}]}', 1, 4, NULL, 2, 2);
INSERT INTO `task_case` VALUES (14, '2019-09-06 08:13:28', '2019-09-06 16:13:35', 4, NULL, NULL, NULL, 2, NULL, '删除一条流程', 'TC6', 7, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击确定\",\"expect\":\"删除成功\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case` VALUES (15, '2019-09-06 08:13:28', '2019-09-06 16:13:34', 4, NULL, NULL, NULL, 1, NULL, '新建一条流程', 'TC5', 7, NULL, '1', NULL, '当前在测试环境，用例管理模块', '{\"step_result\":[{\"step\":\"点击新建按钮\",\"expect\":\"弹出新建流程的弹窗页面\"},{\"step\":\"一次输入必填项，点击保存按钮\",\"expect\":\"流程新建成功，跳转到该流程的详情页面\"}]}', 1, 3, NULL, 2, 2);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of task_case_record
-- ----------------------------
BEGIN;
INSERT INTO `task_case_record` VALUES (1, '2019-09-04 06:57:22', '2019-09-04 14:57:21', 1, 1, NULL, NULL, NULL, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 0, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (2, '2019-09-04 06:57:22', '2019-09-04 14:57:21', 2, 1, NULL, NULL, NULL, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 0, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (3, '2019-09-04 06:57:22', '2019-09-04 14:57:21', 3, 1, NULL, NULL, NULL, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 0, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (4, '2019-09-04 06:57:22', '2019-09-04 14:57:21', 4, 1, NULL, NULL, NULL, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 0, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (5, '2019-09-04 06:58:07', '2019-09-04 14:58:07', 4, 1, NULL, NULL, NULL, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 3, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (6, '2019-09-04 06:58:08', '2019-09-04 14:58:08', 3, 1, NULL, NULL, NULL, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 3, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (7, '2019-09-04 06:58:10', '2019-09-04 14:58:09', 2, 1, NULL, NULL, NULL, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 3, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (8, '2019-09-04 06:58:11', '2019-09-04 14:58:10', 1, 1, NULL, NULL, NULL, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 4, NULL, 1, 2);
INSERT INTO `task_case_record` VALUES (9, '2019-09-04 12:34:04', '2019-09-04 20:34:03', 5, 2, NULL, NULL, NULL, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (10, '2019-09-04 12:34:04', '2019-09-04 20:34:03', 6, 2, NULL, NULL, NULL, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (11, '2019-09-04 12:34:04', '2019-09-04 20:34:04', 7, 2, NULL, NULL, NULL, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (12, '2019-09-04 12:34:04', '2019-09-04 20:34:04', 8, 2, NULL, NULL, NULL, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (13, '2019-09-04 12:34:31', '2019-09-04 20:34:31', 9, 3, NULL, NULL, NULL, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (14, '2019-09-04 12:34:31', '2019-09-04 20:34:31', 10, 3, NULL, NULL, NULL, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (15, '2019-09-04 12:34:31', '2019-09-04 20:34:31', 11, 3, NULL, NULL, NULL, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (16, '2019-09-04 12:34:31', '2019-09-04 20:34:31', 12, 3, NULL, NULL, NULL, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (17, '2019-09-04 12:37:59', '2019-09-04 20:37:59', 12, 3, NULL, NULL, NULL, 1, NULL, '测试用例', 'TC1', 1, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"11\",\"expect\":\"22\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (18, '2019-09-04 12:38:01', '2019-09-04 20:38:00', 11, 3, NULL, NULL, NULL, 0, NULL, '测试用例2', 'TC2', 1, NULL, '1', NULL, '2', '{\"step_result\":[{\"step\":\"2\",\"expect\":\"2\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (19, '2019-09-04 12:38:02', '2019-09-04 20:38:01', 10, 3, NULL, NULL, NULL, 1, NULL, '测试用例3', 'TC3', 1, NULL, '1', NULL, '3', '{\"step_result\":[{\"step\":\"3\",\"expect\":\"3\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (20, '2019-09-04 12:38:03', '2019-09-04 20:38:02', 9, 3, NULL, NULL, NULL, 2, NULL, '测试用例4', 'TC4', 1, NULL, '1', NULL, '4', '{\"step_result\":[{\"step\":\"4\",\"expect\":\"4\"}]}', 1, 4, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (21, '2019-09-06 08:13:28', '2019-09-06 16:13:27', 13, 4, NULL, NULL, NULL, 1, NULL, '取消删除流程', 'TC7', 7, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击取消按钮\",\"expect\":\"删除确认框收起，没有执行删除操作\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (22, '2019-09-06 08:13:28', '2019-09-06 16:13:27', 14, 4, NULL, NULL, NULL, 2, NULL, '删除一条流程', 'TC6', 7, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击确定\",\"expect\":\"删除成功\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (23, '2019-09-06 08:13:28', '2019-09-06 16:13:27', 15, 4, NULL, NULL, NULL, 1, NULL, '新建一条流程', 'TC5', 7, NULL, '1', NULL, '当前在测试环境，用例管理模块', '{\"step_result\":[{\"step\":\"点击新建按钮\",\"expect\":\"弹出新建流程的弹窗页面\"},{\"step\":\"一次输入必填项，点击保存按钮\",\"expect\":\"流程新建成功，跳转到该流程的详情页面\"}]}', 1, 0, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (24, '2019-09-06 08:13:35', '2019-09-06 16:13:34', 15, 4, NULL, NULL, NULL, 1, NULL, '新建一条流程', 'TC5', 7, NULL, '1', NULL, '当前在测试环境，用例管理模块', '{\"step_result\":[{\"step\":\"点击新建按钮\",\"expect\":\"弹出新建流程的弹窗页面\"},{\"step\":\"一次输入必填项，点击保存按钮\",\"expect\":\"流程新建成功，跳转到该流程的详情页面\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (25, '2019-09-06 08:13:36', '2019-09-06 16:13:35', 14, 4, NULL, NULL, NULL, 2, NULL, '删除一条流程', 'TC6', 7, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击确定\",\"expect\":\"删除成功\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (26, '2019-09-06 08:13:37', '2019-09-06 16:13:36', 13, 4, NULL, NULL, NULL, 1, NULL, '取消删除流程', 'TC7', 7, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击取消按钮\",\"expect\":\"删除确认框收起，没有执行删除操作\"}]}', 1, 3, NULL, 2, 2);
INSERT INTO `task_case_record` VALUES (27, '2019-09-06 08:13:39', '2019-09-06 16:13:39', 13, 4, NULL, NULL, NULL, 1, NULL, '取消删除流程', 'TC7', 7, NULL, '1', NULL, NULL, '{\"step_result\":[{\"step\":\"点击流程列表后面的删除按钮\",\"expect\":\"弹出删除确认框\"},{\"step\":\"点击取消按钮\",\"expect\":\"删除确认框收起，没有执行删除操作\"}]}', 1, 4, NULL, 2, 2);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=182 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of track_user
-- ----------------------------
BEGIN;
INSERT INTO `track_user` VALUES (1, '2019-09-03 03:01:47', '2019-09-03 03:01:46', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (2, '2019-09-03 03:18:03', '2019-09-03 03:18:02', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (3, '2019-09-03 03:39:12', '2019-09-03 03:39:12', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (4, '2019-09-03 03:42:20', '2019-09-03 03:42:19', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (5, '2019-09-03 03:53:41', '2019-09-03 03:53:40', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (6, '2019-09-03 03:55:45', '2019-09-03 03:55:44', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (7, '2019-09-03 05:57:40', '2019-09-03 05:57:39', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (8, '2019-09-03 06:00:27', '2019-09-03 06:00:26', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (9, '2019-09-03 06:00:44', '2019-09-03 06:00:44', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (10, '2019-09-03 06:07:10', '2019-09-03 06:07:10', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (11, '2019-09-03 06:11:30', '2019-09-03 06:11:30', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (12, '2019-09-03 06:31:37', '2019-09-03 06:31:37', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (13, '2019-09-03 06:31:42', '2019-09-03 06:31:42', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (14, '2019-09-03 06:31:43', '2019-09-03 06:31:43', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (15, '2019-09-03 06:31:44', '2019-09-03 06:31:44', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (16, '2019-09-03 06:31:45', '2019-09-03 06:31:45', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (17, '2019-09-03 06:33:11', '2019-09-03 06:33:11', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (18, '2019-09-03 06:33:13', '2019-09-03 06:33:12', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (19, '2019-09-03 06:33:14', '2019-09-03 06:33:13', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (20, '2019-09-03 06:33:15', '2019-09-03 06:33:14', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (21, '2019-09-03 06:33:16', '2019-09-03 06:33:15', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (22, '2019-09-03 06:33:17', '2019-09-03 06:33:16', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (23, '2019-09-03 06:33:18', '2019-09-03 06:33:17', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (24, '2019-09-03 06:33:18', '2019-09-03 06:33:18', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (25, '2019-09-03 07:35:58', '2019-09-03 07:35:57', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (26, '2019-09-03 07:36:47', '2019-09-03 07:36:47', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (27, '2019-09-03 08:00:10', '2019-09-03 08:00:09', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (28, '2019-09-03 08:05:51', '2019-09-03 08:05:51', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (29, '2019-09-03 08:25:57', '2019-09-03 08:25:56', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (30, '2019-09-03 08:44:14', '2019-09-03 08:44:13', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (31, '2019-09-03 09:01:39', '2019-09-03 09:01:38', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (32, '2019-09-03 09:06:01', '2019-09-03 09:06:00', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (33, '2019-09-03 09:10:06', '2019-09-03 09:10:06', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (34, '2019-09-03 09:23:16', '2019-09-03 09:23:15', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (35, '2019-09-03 09:24:19', '2019-09-03 09:24:18', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (36, '2019-09-03 09:24:55', '2019-09-03 09:24:54', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (37, '2019-09-03 09:42:46', '2019-09-03 09:42:46', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (38, '2019-09-03 09:46:19', '2019-09-03 09:46:18', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (39, '2019-09-03 09:51:47', '2019-09-03 09:51:46', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (40, '2019-09-03 09:54:05', '2019-09-03 09:54:04', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (41, '2019-09-03 09:54:41', '2019-09-03 09:54:40', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (42, '2019-09-03 09:54:51', '2019-09-03 09:54:51', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (43, '2019-09-03 09:57:59', '2019-09-03 09:57:59', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (44, '2019-09-03 10:00:25', '2019-09-03 10:00:25', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (45, '2019-09-03 10:02:04', '2019-09-03 10:02:03', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (46, '2019-09-03 10:02:32', '2019-09-03 10:02:31', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (47, '2019-09-03 10:02:54', '2019-09-03 10:02:54', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (48, '2019-09-03 10:04:45', '2019-09-03 10:04:44', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (49, '2019-09-03 11:06:08', '2019-09-03 11:06:08', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (50, '2019-09-03 11:06:19', '2019-09-03 11:06:19', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (51, '2019-09-03 11:13:07', '2019-09-03 11:13:07', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (52, '2019-09-03 11:14:13', '2019-09-03 11:14:12', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (53, '2019-09-03 11:19:38', '2019-09-03 11:19:38', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (54, '2019-09-03 11:20:34', '2019-09-03 11:20:33', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (55, '2019-09-03 11:26:50', '2019-09-03 11:26:50', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (56, '2019-09-03 11:31:58', '2019-09-03 11:31:57', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (57, '2019-09-03 11:33:37', '2019-09-03 11:33:36', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (58, '2019-09-03 11:36:19', '2019-09-03 11:36:19', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (59, '2019-09-03 11:36:48', '2019-09-03 11:36:48', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (60, '2019-09-03 11:44:45', '2019-09-03 11:44:45', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (61, '2019-09-03 11:45:18', '2019-09-03 11:45:17', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (62, '2019-09-03 11:46:10', '2019-09-03 11:46:09', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (63, '2019-09-03 11:46:12', '2019-09-03 11:46:12', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (64, '2019-09-03 11:46:25', '2019-09-03 11:46:25', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (65, '2019-09-03 11:47:33', '2019-09-03 11:47:32', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (66, '2019-09-03 11:47:40', '2019-09-03 11:47:39', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (67, '2019-09-03 11:50:14', '2019-09-03 11:50:14', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (68, '2019-09-03 11:52:46', '2019-09-03 11:52:46', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (69, '2019-09-03 11:52:48', '2019-09-03 11:52:47', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (70, '2019-09-03 11:52:51', '2019-09-03 11:52:51', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (71, '2019-09-03 11:54:16', '2019-09-03 11:54:15', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (72, '2019-09-03 11:55:21', '2019-09-03 11:55:20', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (73, '2019-09-03 12:06:38', '2019-09-03 12:06:37', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (74, '2019-09-03 12:16:28', '2019-09-03 12:16:28', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (75, '2019-09-03 12:19:14', '2019-09-03 12:19:14', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (76, '2019-09-03 12:20:05', '2019-09-03 12:20:05', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (77, '2019-09-03 12:23:02', '2019-09-03 12:23:01', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (78, '2019-09-03 12:25:39', '2019-09-03 12:25:39', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (79, '2019-09-03 12:30:25', '2019-09-03 12:30:24', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (80, '2019-09-03 12:33:33', '2019-09-03 12:33:32', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (81, '2019-09-03 12:33:33', '2019-09-03 12:33:33', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (82, '2019-09-03 12:35:02', '2019-09-03 12:35:02', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (83, '2019-09-03 12:35:31', '2019-09-03 12:35:31', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (84, '2019-09-03 12:48:14', '2019-09-03 20:48:13', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (85, '2019-09-03 12:51:26', '2019-09-03 20:51:26', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (86, '2019-09-03 12:56:13', '2019-09-03 20:56:13', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (87, '2019-09-04 02:37:34', '2019-09-04 10:37:33', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (88, '2019-09-04 02:42:37', '2019-09-04 10:42:37', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (89, '2019-09-04 02:55:46', '2019-09-04 10:55:46', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (90, '2019-09-04 03:10:24', '2019-09-04 11:10:24', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (91, '2019-09-04 03:11:04', '2019-09-04 11:11:04', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (92, '2019-09-04 03:23:58', '2019-09-04 11:23:57', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (93, '2019-09-04 03:29:33', '2019-09-04 11:29:33', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (94, '2019-09-04 03:45:44', '2019-09-04 11:45:43', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (95, '2019-09-04 06:54:21', '2019-09-04 14:54:20', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (96, '2019-09-04 12:19:57', '2019-09-04 20:19:57', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (97, '2019-09-05 02:32:26', '2019-09-05 10:32:26', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (98, '2019-09-06 02:20:37', '2019-09-06 10:20:37', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (99, '2019-09-06 07:21:16', '2019-09-06 15:21:15', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (100, '2019-09-06 08:29:14', '2019-09-06 16:29:13', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (101, '2019-09-06 10:29:21', '2019-09-06 18:29:21', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (102, '2019-09-06 10:29:55', '2019-09-06 18:29:54', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (103, '2019-09-06 10:30:34', '2019-09-06 18:30:33', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (104, '2019-09-09 08:03:49', '2019-09-09 16:03:49', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (105, '2019-09-10 03:32:20', '2019-09-10 11:32:20', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (106, '2019-09-10 04:00:29', '2019-09-10 12:00:28', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (107, '2019-09-10 06:44:06', '2019-09-10 14:44:06', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (108, '2019-09-10 07:23:41', '2019-09-10 15:23:41', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (109, '2019-09-10 07:34:17', '2019-09-10 15:34:16', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (110, '2019-09-10 07:37:25', '2019-09-10 15:37:25', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (111, '2019-09-10 07:47:22', '2019-09-10 15:47:21', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (112, '2019-09-10 08:13:03', '2019-09-10 16:13:02', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (113, '2019-09-10 08:26:22', '2019-09-10 16:26:21', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (114, '2019-09-10 08:27:28', '2019-09-10 16:27:27', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (115, '2019-09-10 08:28:27', '2019-09-10 16:28:27', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (116, '2019-09-10 08:34:49', '2019-09-10 16:34:49', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (117, '2019-09-10 08:35:02', '2019-09-10 16:35:02', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (118, '2019-09-10 08:35:36', '2019-09-10 16:35:36', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (119, '2019-09-10 08:36:26', '2019-09-10 16:36:25', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (120, '2019-09-10 08:39:21', '2019-09-10 16:39:20', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (121, '2019-09-10 08:39:46', '2019-09-10 16:39:45', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (122, '2019-09-10 08:46:55', '2019-09-10 16:46:55', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (123, '2019-09-10 08:48:36', '2019-09-10 16:48:35', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (124, '2019-09-10 08:49:37', '2019-09-10 16:49:37', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (125, '2019-09-10 08:56:28', '2019-09-10 16:56:27', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (126, '2019-09-10 09:00:11', '2019-09-10 17:00:11', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (127, '2019-09-10 09:08:23', '2019-09-10 17:08:23', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (128, '2019-09-10 09:11:21', '2019-09-10 17:11:21', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (129, '2019-09-10 09:20:34', '2019-09-10 17:20:33', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (130, '2019-09-10 09:23:37', '2019-09-10 17:23:37', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (131, '2019-09-10 09:25:26', '2019-09-10 17:25:26', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (132, '2019-09-10 09:26:51', '2019-09-10 17:26:50', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (133, '2019-09-10 09:27:23', '2019-09-10 17:27:23', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (134, '2019-09-10 09:31:51', '2019-09-10 17:31:50', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (135, '2019-09-10 09:42:08', '2019-09-10 17:42:08', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (136, '2019-09-10 09:47:31', '2019-09-10 17:47:30', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (137, '2019-09-10 09:51:21', '2019-09-10 17:51:21', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (138, '2019-09-10 09:55:01', '2019-09-10 17:55:00', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (139, '2019-09-10 09:56:41', '2019-09-10 17:56:41', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (140, '2019-09-10 09:57:36', '2019-09-10 17:57:35', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (141, '2019-09-10 10:00:44', '2019-09-10 18:00:44', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (142, '2019-09-10 10:01:23', '2019-09-10 18:01:22', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (143, '2019-09-10 10:02:24', '2019-09-10 18:02:23', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (144, '2019-09-10 10:02:28', '2019-09-10 18:02:27', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (145, '2019-09-10 10:02:42', '2019-09-10 18:02:42', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (146, '2019-09-10 10:03:00', '2019-09-10 18:03:00', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (147, '2019-09-10 10:05:54', '2019-09-10 18:05:53', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (148, '2019-09-10 10:06:22', '2019-09-10 18:06:22', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (149, '2019-09-10 10:06:47', '2019-09-10 18:06:47', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (150, '2019-09-10 10:07:08', '2019-09-10 18:07:07', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (151, '2019-09-10 10:09:37', '2019-09-10 18:09:37', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (152, '2019-09-10 10:10:22', '2019-09-10 18:10:21', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (153, '2019-09-10 10:16:52', '2019-09-10 18:16:52', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (154, '2019-09-10 10:17:21', '2019-09-10 18:17:20', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (155, '2019-09-10 10:25:11', '2019-09-10 18:25:11', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (156, '2019-09-10 10:25:32', '2019-09-10 18:25:32', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (157, '2019-09-10 10:27:50', '2019-09-10 18:27:49', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (158, '2019-09-10 10:28:46', '2019-09-10 18:28:46', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (159, '2019-09-10 10:33:11', '2019-09-10 18:33:10', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (160, '2019-09-10 10:34:44', '2019-09-10 18:34:43', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (161, '2019-09-10 10:45:39', '2019-09-10 18:45:38', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (162, '2019-09-10 10:57:12', '2019-09-10 18:57:12', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (163, '2019-09-10 11:03:01', '2019-09-10 19:03:01', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (164, '2019-09-10 11:05:30', '2019-09-10 19:05:29', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (165, '2019-09-10 11:11:12', '2019-09-10 19:11:12', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (166, '2019-09-10 11:14:30', '2019-09-10 19:14:29', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (167, '2019-09-10 11:17:03', '2019-09-10 19:17:02', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (168, '2019-09-10 11:21:10', '2019-09-10 19:21:09', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (169, '2019-09-10 11:21:33', '2019-09-10 19:21:33', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (170, '2019-09-10 11:30:26', '2019-09-10 19:30:25', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (171, '2019-09-10 11:32:04', '2019-09-10 19:32:04', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (172, '2019-09-10 11:35:00', '2019-09-10 19:34:59', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (173, '2019-09-10 11:35:19', '2019-09-10 19:35:18', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (174, '2019-09-10 11:43:45', '2019-09-10 19:43:45', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (175, '2019-09-10 11:44:43', '2019-09-10 19:44:43', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (176, '2019-09-10 11:45:24', '2019-09-10 19:45:24', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (177, '2019-09-10 11:47:21', '2019-09-10 19:47:21', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (178, '2019-09-10 11:47:52', '2019-09-10 19:47:51', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (179, '2019-09-10 12:14:15', '2019-09-10 20:14:15', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (180, '2019-09-10 12:22:51', '2019-09-10 20:22:50', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
INSERT INTO `track_user` VALUES (181, '2019-09-10 12:29:58', '2019-09-10 20:29:57', 'admin', NULL, 0, NULL, NULL, 1, '', 'admin', 1152, NULL, NULL, NULL);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=1156 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (1152, NULL, '2019-09-02 03:39:01', 'admin', 'admin', NULL, '7133befcaa96ce75df05038e4c8bf0d9', 0, NULL, NULL, 1, NULL, NULL);
INSERT INTO `user` VALUES (1153, '2019-09-03 12:49:12', '2019-09-03 21:00:29', 'zy1', '张宇', NULL, '7133befcaa96ce75df05038e4c8bf0d9', 0, 'zy1@ass.com', '', 1, NULL, NULL);
INSERT INTO `user` VALUES (1154, '2019-09-03 12:59:22', '2019-09-03 20:59:21', 'test', '测试', NULL, '7133befcaa96ce75df05038e4c8bf0d9', 0, 'test@test.com', '', 1, NULL, NULL);
INSERT INTO `user` VALUES (1155, '2019-09-03 12:59:56', '2019-09-03 20:59:55', 'dev', '开发', NULL, '7133befcaa96ce75df05038e4c8bf0d9', 0, 'dev@tcloud.com', '', 1, NULL, NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_bind_project
-- ----------------------------
BEGIN;
INSERT INTO `user_bind_project` VALUES (1, '2019-09-03 12:49:24', '2019-09-03 20:49:23', 1153, 2);
INSERT INTO `user_bind_project` VALUES (2, '2019-09-03 13:00:10', '2019-09-03 21:00:10', 1154, 2);
INSERT INTO `user_bind_project` VALUES (3, '2019-09-03 13:00:10', '2019-09-03 21:00:10', 1155, 2);
INSERT INTO `user_bind_project` VALUES (4, '2019-09-03 13:00:10', '2019-09-03 21:00:10', 1152, 2);
COMMIT;

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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_bind_role
-- ----------------------------
BEGIN;
INSERT INTO `user_bind_role` VALUES (1, NULL, '2019-09-03 12:28:31', 1152, 1, 0);
INSERT INTO `user_bind_role` VALUES (2, '2019-09-03 12:49:28', '2019-09-03 20:49:27', 1153, 3, 2);
INSERT INTO `user_bind_role` VALUES (4, '2019-09-03 13:00:49', '2019-09-03 21:00:48', 1152, 3, 2);
INSERT INTO `user_bind_role` VALUES (5, '2019-09-03 13:00:49', '2019-09-03 21:00:48', 1152, 1, 2);
INSERT INTO `user_bind_role` VALUES (6, '2019-09-03 13:00:53', '2019-09-03 21:00:53', 1155, 2, 2);
INSERT INTO `user_bind_role` VALUES (7, '2019-09-03 13:00:57', '2019-09-03 21:00:56', 1154, 3, 2);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of version
-- ----------------------------
BEGIN;
INSERT INTO `version` VALUES (1, '2019-09-03 12:50:21', '2019-09-03 20:50:20', '1.0.0', 2, '2019-09-03 00:00:00', '2019-10-16 00:00:00', NULL, 1152, 0, 0, '1.0.0', NULL, 1);
INSERT INTO `version` VALUES (2, '2019-09-04 12:33:11', '2019-09-10 17:30:31', '1.0.1', 2, '2019-09-04 00:00:00', '2019-09-06 00:00:00', '2019-09-10 09:30:31', 1152, 1, 0, '1.0.1版本', NULL, 1);
COMMIT;

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
