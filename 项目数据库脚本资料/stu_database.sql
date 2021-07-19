/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 8.0.20 : Database - sac_database
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`sac_database` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `sac_database`;

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group` */

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add act_to_stu',7,'add_act_to_stu'),
(26,'Can change act_to_stu',7,'change_act_to_stu'),
(27,'Can delete act_to_stu',7,'delete_act_to_stu'),
(28,'Can view act_to_stu',7,'view_act_to_stu'),
(29,'Can add activities',8,'add_activities'),
(30,'Can change activities',8,'change_activities'),
(31,'Can delete activities',8,'delete_activities'),
(32,'Can view activities',8,'view_activities'),
(33,'Can add activities_modified',9,'add_activities_modified'),
(34,'Can change activities_modified',9,'change_activities_modified'),
(35,'Can delete activities_modified',9,'delete_activities_modified'),
(36,'Can view activities_modified',9,'view_activities_modified'),
(37,'Can add bbs_comments',10,'add_bbs_comments'),
(38,'Can change bbs_comments',10,'change_bbs_comments'),
(39,'Can delete bbs_comments',10,'delete_bbs_comments'),
(40,'Can view bbs_comments',10,'view_bbs_comments'),
(41,'Can add managers',11,'add_managers'),
(42,'Can change managers',11,'change_managers'),
(43,'Can delete managers',11,'delete_managers'),
(44,'Can view managers',11,'view_managers'),
(45,'Can add notices',12,'add_notices'),
(46,'Can change notices',12,'change_notices'),
(47,'Can delete notices',12,'delete_notices'),
(48,'Can view notices',12,'view_notices'),
(49,'Can add org_direct messages',13,'add_org_directmessages'),
(50,'Can change org_direct messages',13,'change_org_directmessages'),
(51,'Can delete org_direct messages',13,'delete_org_directmessages'),
(52,'Can view org_direct messages',13,'view_org_directmessages'),
(53,'Can add organizers',14,'add_organizers'),
(54,'Can change organizers',14,'change_organizers'),
(55,'Can delete organizers',14,'delete_organizers'),
(56,'Can view organizers',14,'view_organizers'),
(57,'Can add organizers_modified',15,'add_organizers_modified'),
(58,'Can change organizers_modified',15,'change_organizers_modified'),
(59,'Can delete organizers_modified',15,'delete_organizers_modified'),
(60,'Can view organizers_modified',15,'view_organizers_modified'),
(61,'Can add stu_direct messages',16,'add_stu_directmessages'),
(62,'Can change stu_direct messages',16,'change_stu_directmessages'),
(63,'Can delete stu_direct messages',16,'delete_stu_directmessages'),
(64,'Can view stu_direct messages',16,'view_stu_directmessages'),
(65,'Can add stu_to_team',17,'add_stu_to_team'),
(66,'Can change stu_to_team',17,'change_stu_to_team'),
(67,'Can delete stu_to_team',17,'delete_stu_to_team'),
(68,'Can view stu_to_team',17,'view_stu_to_team'),
(69,'Can add students',18,'add_students'),
(70,'Can change students',18,'change_students'),
(71,'Can delete students',18,'delete_students'),
(72,'Can view students',18,'view_students'),
(73,'Can add teams',19,'add_teams'),
(74,'Can change teams',19,'change_teams'),
(75,'Can delete teams',19,'delete_teams'),
(76,'Can view teams',19,'view_teams');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user` */

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_admin_log` */

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values 
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(8,'sac_app','activities'),
(9,'sac_app','activities_modified'),
(7,'sac_app','act_to_stu'),
(10,'sac_app','bbs_comments'),
(11,'sac_app','managers'),
(12,'sac_app','notices'),
(14,'sac_app','organizers'),
(15,'sac_app','organizers_modified'),
(13,'sac_app','org_directmessages'),
(18,'sac_app','students'),
(16,'sac_app','stu_directmessages'),
(17,'sac_app','stu_to_team'),
(19,'sac_app','teams'),
(6,'sessions','session');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values 
(1,'contenttypes','0001_initial','2021-07-16 16:46:50.026570'),
(2,'auth','0001_initial','2021-07-16 16:46:50.259569'),
(3,'admin','0001_initial','2021-07-16 16:46:51.130568'),
(4,'admin','0002_logentry_remove_auto_add','2021-07-16 16:46:51.301569'),
(5,'admin','0003_logentry_add_action_flag_choices','2021-07-16 16:46:51.312608'),
(6,'contenttypes','0002_remove_content_type_name','2021-07-16 16:46:51.452569'),
(7,'auth','0002_alter_permission_name_max_length','2021-07-16 16:46:51.537572'),
(8,'auth','0003_alter_user_email_max_length','2021-07-16 16:46:51.641570'),
(9,'auth','0004_alter_user_username_opts','2021-07-16 16:46:51.659569'),
(10,'auth','0005_alter_user_last_login_null','2021-07-16 16:46:51.878568'),
(11,'auth','0006_require_contenttypes_0002','2021-07-16 16:46:51.887571'),
(12,'auth','0007_alter_validators_add_error_messages','2021-07-16 16:46:51.898575'),
(13,'auth','0008_alter_user_username_max_length','2021-07-16 16:46:51.986568'),
(14,'auth','0009_alter_user_last_name_max_length','2021-07-16 16:46:52.141569'),
(15,'auth','0010_alter_group_name_max_length','2021-07-16 16:46:52.225570'),
(16,'auth','0011_update_proxy_permissions','2021-07-16 16:46:52.236569'),
(17,'auth','0012_alter_user_first_name_max_length','2021-07-16 16:46:52.337569'),
(18,'sac_app','0001_initial','2021-07-16 16:46:53.412603'),
(19,'sac_app','0002_auto_20210716_2303','2021-07-16 16:46:56.570573'),
(20,'sac_app','0003_auto_20210717_0046','2021-07-16 16:46:59.764568'),
(21,'sessions','0001_initial','2021-07-16 16:46:59.804570');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values 
('337dd59a8lesl52zqwak51jsps20st5g','.eJyrVkrOSE3Ojk_OT0lVslLydnJxC1XSUSotTi2Kz0wBihgZGBiYwERKKgtAqvKL0hPzMqtSi5RqAYwJFI0:1m4Usv:otZxS3iygLZYCajHAkmK4WvAsKaDd3NCylahlWRpp-c','2021-07-30 20:56:37.350678'),
('gaall6kdf5n9eof7r9pk1av703xunzey','.eJxVjTEKQkEMRO-S2iKuyWa1E7Sy8QAB-bs_URCx-KQS7260sxmGxxvmBQ9blulqsAMNdt5kFpozt0gaZM00qpRJQ6r0n8PZS6_JEdca7jg0Wnf5d5gwt-Tiybk0WMG42bhfxnP-_h0P-_MJ3h-RniiE:1m4R6y:w0Us7PGdKhfbuT8bZxwaHoSTkCXmrKhgFk_mdwW0ypw','2021-07-30 16:54:52.319137');

/*Table structure for table `sac_app_act_to_stu` */

DROP TABLE IF EXISTS `sac_app_act_to_stu`;

CREATE TABLE `sac_app_act_to_stu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `act_id` int NOT NULL,
  `stu_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sac_app_act_to_stu_act_id_0b78d637_fk` (`act_id`),
  KEY `sac_app_act_to_stu_stu_id_40acbe92_fk` (`stu_id`),
  CONSTRAINT `sac_app_act_to_stu_act_id_0b78d637_fk` FOREIGN KEY (`act_id`) REFERENCES `sac_app_activities` (`id`),
  CONSTRAINT `sac_app_act_to_stu_stu_id_40acbe92_fk` FOREIGN KEY (`stu_id`) REFERENCES `sac_app_students` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_act_to_stu` */

insert  into `sac_app_act_to_stu`(`id`,`act_id`,`stu_id`) values 
(1,1,1),
(2,2,1),
(3,4,1),
(4,3,2),
(5,3,1),
(6,4,2),
(7,5,2),
(8,5,1),
(15,3,1),
(16,3,1),
(17,5,1),
(18,3,1),
(19,3,1);

/*Table structure for table `sac_app_activities` */

DROP TABLE IF EXISTS `sac_app_activities`;

CREATE TABLE `sac_app_activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `act_id` varchar(1024) NOT NULL,
  `org_name` varchar(1024) DEFAULT NULL,
  `act_name` varchar(1024) NOT NULL,
  `act_start_time` date NOT NULL,
  `act_end_time` date NOT NULL,
  `act_organizer_name` varchar(1024) DEFAULT NULL,
  `act_organizer_phone` varchar(128) NOT NULL,
  `act_type` int NOT NULL,
  `act_created_team_number` int DEFAULT NULL,
  `act_max_team_number` int DEFAULT NULL,
  `act_min_team_number` int DEFAULT NULL,
  `act_team_number` int DEFAULT NULL,
  `act_state` int DEFAULT NULL,
  `act_total_number` int DEFAULT NULL,
  `act_participated_number` int DEFAULT NULL,
  `act_available_team_number` int DEFAULT NULL,
  `act_available_number` int DEFAULT NULL,
  `act_flag` varchar(16) NOT NULL,
  `act_planning_book` varchar(100) DEFAULT NULL,
  `act_introduction` longtext NOT NULL,
  `act_organizer_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sac_app_activities_act_organizer_id_a7cfeb88_fk` (`act_organizer_id`),
  CONSTRAINT `sac_app_activities_act_organizer_id_a7cfeb88_fk` FOREIGN KEY (`act_organizer_id`) REFERENCES `sac_app_organizers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_activities` */

insert  into `sac_app_activities`(`id`,`act_id`,`org_name`,`act_name`,`act_start_time`,`act_end_time`,`act_organizer_name`,`act_organizer_phone`,`act_type`,`act_created_team_number`,`act_max_team_number`,`act_min_team_number`,`act_team_number`,`act_state`,`act_total_number`,`act_participated_number`,`act_available_team_number`,`act_available_number`,`act_flag`,`act_planning_book`,`act_introduction`,`act_organizer_id`) values 
(1,'1000001',NULL,'穿越虎溪','2021-07-18','2021-07-31','贾培森','1830000000000',0,0,0,0,0,2,1000,0,0,999,'可参加','穿越虎溪策划书.doc','户拓最帅协会',1),
(2,'1000002',NULL,'足球比赛','2021-07-24','2021-07-25','马祥','12312341234',1,1,10,2,100,2,0,0,100,0,'可参加','穿越虎溪策划书.doc','重大最火比赛',1),
(3,'1000003',NULL,'足球联赛','2021-07-17','2021-07-17','社长1号','5151515151',1,2,7,5,40,2,2,0,40,0,'可参加','穿越虎溪策划书.doc','最强选手等你来战',2),
(4,'1000004',NULL,'招生啦','2021-07-24','2021-08-21','社长1号','12345677',0,0,0,0,0,2,10000,0,0,9998,'可参加','穿越虎溪策划书.doc','足球社等你来',2),
(5,'1000005',NULL,'拳击比赛','2021-07-24','2021-07-25','社长2号','12312341230',1,1,5,3,10,2,0,0,10,0,'可参加','穿越虎溪策划书.doc','汪汪汪',3),
(6,'1000006',NULL,'校外游玩','2021-07-23','2021-07-31','马祥','12121212',0,0,0,0,0,2,100,0,0,100,'可参加','穿越虎溪策划书.doc','快来玩',1),
(7,'1000007',NULL,'英语竞赛','2021-07-18','2021-07-20','秦浩庭','156714537',0,0,0,0,0,2,100,0,0,100,'可参加','穿越虎溪策划书.doc','最强英语达人，等你来',4),
(8,'1000008',NULL,'数模团队赛','2021-07-25','2021-07-31','秦浩庭','19089077890',1,0,5,3,100,2,0,0,100,0,'可参加','穿越虎溪策划书.doc','勇敢牛牛，虫虫虫',4);

/*Table structure for table `sac_app_activities_modified` */

DROP TABLE IF EXISTS `sac_app_activities_modified`;

CREATE TABLE `sac_app_activities_modified` (
  `id` int NOT NULL AUTO_INCREMENT,
  `act_id` varchar(1024) NOT NULL,
  `act_name` varchar(1024) NOT NULL,
  `act_start_time` date NOT NULL,
  `act_end_time` date NOT NULL,
  `act_organizer_name` varchar(1024) DEFAULT NULL,
  `act_organizer_phone` varchar(1024) NOT NULL,
  `act_type` int NOT NULL,
  `act_created_team_number` int NOT NULL,
  `act_max_team_number` int NOT NULL,
  `act_min_team_number` int NOT NULL,
  `act_team_number` int NOT NULL,
  `act_state` int NOT NULL,
  `act_total_number` int NOT NULL,
  `act_participated_number` int NOT NULL,
  `act_available_number` int NOT NULL,
  `act_flag` varchar(16) NOT NULL,
  `act_planning_book` varchar(100) DEFAULT NULL,
  `act_introduction` longtext NOT NULL,
  `act_valid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_activities_modified` */

insert  into `sac_app_activities_modified`(`id`,`act_id`,`act_name`,`act_start_time`,`act_end_time`,`act_organizer_name`,`act_organizer_phone`,`act_type`,`act_created_team_number`,`act_max_team_number`,`act_min_team_number`,`act_team_number`,`act_state`,`act_total_number`,`act_participated_number`,`act_available_number`,`act_flag`,`act_planning_book`,`act_introduction`,`act_valid`) values 
(1,'1000003','足球联赛','2021-07-17','2021-07-17','社长1号','5151515151',1,0,7,5,40,2,2,0,0,'不可参加','穿越虎溪策划书.doc','最强选手等你来战',0);

/*Table structure for table `sac_app_bbs_comments` */

DROP TABLE IF EXISTS `sac_app_bbs_comments`;

CREATE TABLE `sac_app_bbs_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bbs_id` varchar(128) NOT NULL,
  `bbs_message` longtext NOT NULL,
  `bbs_create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_bbs_comments` */

insert  into `sac_app_bbs_comments`(`id`,`bbs_id`,`bbs_message`,`bbs_create_time`) values 
(1,'200032','大家冲啊','2021-07-16 18:09:15.104397');

/*Table structure for table `sac_app_managers` */

DROP TABLE IF EXISTS `sac_app_managers`;

CREATE TABLE `sac_app_managers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `man_id` varchar(128) NOT NULL,
  `man_password` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_managers` */

insert  into `sac_app_managers`(`id`,`man_id`,`man_password`) values 
(1,'10001','123456');

/*Table structure for table `sac_app_notices` */

DROP TABLE IF EXISTS `sac_app_notices`;

CREATE TABLE `sac_app_notices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `notice_title` varchar(64) NOT NULL,
  `notices_act_id` int DEFAULT NULL,
  `notices_create_time` datetime(6) NOT NULL,
  `notice_content` longtext NOT NULL,
  `notice_appendix` varchar(100) DEFAULT NULL,
  `notice_tag` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_notices` */

insert  into `sac_app_notices`(`id`,`notice_title`,`notices_act_id`,`notices_create_time`,`notice_content`,`notice_appendix`,`notice_tag`) values 
(1,'重庆大学出现了李先',NULL,'2021-07-16 16:59:15.253507','帅','',0),
(2,'1',NULL,'2021-07-16 17:01:56.660347','户拓协会发布活动啦','',1),
(3,'创建了跆拳道社',NULL,'2021-07-16 17:27:17.774850','跆拳道社虫虫','',0);

/*Table structure for table `sac_app_org_directmessages` */

DROP TABLE IF EXISTS `sac_app_org_directmessages`;

CREATE TABLE `sac_app_org_directmessages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `send_id` varchar(128) NOT NULL,
  `message` longtext NOT NULL,
  `accept_id` varchar(128) NOT NULL,
  `message_send_time` datetime(6) NOT NULL,
  `message_valid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_org_directmessages` */

insert  into `sac_app_org_directmessages`(`id`,`send_id`,`message`,`accept_id`,`message_send_time`,`message_valid`) values 
(1,'','您拟举办的活动穿越虎溪审核通过。 通过理由:henhao','20001','2021-07-16 17:03:09.671249',1),
(2,'','您拟修改的社团信息，审核成功。 通过理由:henhao','20001','2021-07-16 17:03:22.942857',1),
(3,'','您拟举办的活动足球比赛审核通过。 通过理由:henhao','20001','2021-07-16 17:21:33.925368',1),
(4,'','很遗憾的通知您，您拟举办的活动足球联赛审核不通过。 不通过理由:策划不够具体，详细策划','20002','2021-07-16 17:30:55.149137',1),
(5,'','您拟举办的活动招生啦审核通过。 通过理由:可以','20002','2021-07-16 17:31:05.691534',1),
(6,'','您拟举办的活动足球联赛审核通过。 通过理由:可以','20002','2021-07-16 17:59:45.481689',1),
(7,'','您拟举办的活动拳击比赛审核通过。 通过理由:s','20003','2021-07-16 18:25:03.109322',1),
(8,'','您拟举办的活动校外游玩审核通过。 通过理由:通过','20001','2021-07-16 19:18:45.462940',1),
(9,'','您拟举办的活动英语竞赛审核通过。 通过理由:通过','20004','2021-07-16 20:18:39.316151',1),
(10,'','您拟举办的活动数模团队赛审核通过。 通过理由:通过','20004','2021-07-16 20:18:47.291494',1),
(11,'','您拟修改的社团信息，审核成功。 通过理由:tongg','20004','2021-07-16 20:55:51.848930',1);

/*Table structure for table `sac_app_organizers` */

DROP TABLE IF EXISTS `sac_app_organizers`;

CREATE TABLE `sac_app_organizers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `org_id` varchar(128) NOT NULL,
  `org_name` varchar(128) NOT NULL,
  `org_header_name` varchar(128) NOT NULL,
  `org_password` varchar(128) NOT NULL,
  `org_header_phone` varchar(32) NOT NULL,
  `org_header_college` varchar(1024) DEFAULT NULL,
  `org_introduction` longtext NOT NULL,
  `org_valid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_organizers` */

insert  into `sac_app_organizers`(`id`,`org_id`,`org_name`,`org_header_name`,`org_password`,`org_header_phone`,`org_header_college`,`org_introduction`,`org_valid`) values 
(1,'20001','户外拓展协会','马祥','111111','15200000000','智科','最帅协会',1),
(2,'20002','足球社','社长1号','123456','12312341230','英语学院','足球最帅',0),
(3,'20003','跆拳道社','社长2号','123456','123456123456','体育学院','跆拳道无敌',0),
(4,'20004','猪猪侠','覃智科','123456','173443437','计算机学院','帅',1);

/*Table structure for table `sac_app_organizers_modified` */

DROP TABLE IF EXISTS `sac_app_organizers_modified`;

CREATE TABLE `sac_app_organizers_modified` (
  `id` int NOT NULL AUTO_INCREMENT,
  `org_id` varchar(128) DEFAULT NULL,
  `org_password` varchar(128) NOT NULL,
  `org_name` varchar(128) NOT NULL,
  `org_header_name` varchar(1024) NOT NULL,
  `org_header_phone` varchar(128) NOT NULL,
  `org_header_college` varchar(1024) NOT NULL,
  `org_introduction` longtext NOT NULL,
  `org_valid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_organizers_modified` */

insert  into `sac_app_organizers_modified`(`id`,`org_id`,`org_password`,`org_name`,`org_header_name`,`org_header_phone`,`org_header_college`,`org_introduction`,`org_valid`) values 
(1,'20001','111111','户外拓展协会','马祥','15200000000','智科','最帅协会',0),
(2,'20004','123456','猪猪侠','覃智科','15717151716','计算机学院','帅',0);

/*Table structure for table `sac_app_stu_directmessages` */

DROP TABLE IF EXISTS `sac_app_stu_directmessages`;

CREATE TABLE `sac_app_stu_directmessages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `send_id` varchar(128) NOT NULL,
  `message` longtext NOT NULL,
  `accept_id` varchar(128) NOT NULL,
  `message_send_time` datetime(6) NOT NULL,
  `message_valid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_stu_directmessages` */

/*Table structure for table `sac_app_stu_to_team` */

DROP TABLE IF EXISTS `sac_app_stu_to_team`;

CREATE TABLE `sac_app_stu_to_team` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stu_id` int NOT NULL,
  `team_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sac_app_stu_to_team_stu_id_b1ad106e_fk` (`stu_id`),
  KEY `sac_app_stu_to_team_team_id_a9ffeddc_fk` (`team_id`),
  CONSTRAINT `sac_app_stu_to_team_stu_id_b1ad106e_fk` FOREIGN KEY (`stu_id`) REFERENCES `sac_app_students` (`id`),
  CONSTRAINT `sac_app_stu_to_team_team_id_a9ffeddc_fk` FOREIGN KEY (`team_id`) REFERENCES `sac_app_teams` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_stu_to_team` */

insert  into `sac_app_stu_to_team`(`id`,`stu_id`,`team_id`) values 
(1,1,1),
(2,2,2),
(3,1,3),
(4,2,4),
(12,1,2),
(13,1,2),
(14,1,4),
(15,1,3),
(16,1,3);

/*Table structure for table `sac_app_students` */

DROP TABLE IF EXISTS `sac_app_students`;

CREATE TABLE `sac_app_students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stu_id` varchar(1024) NOT NULL,
  `stu_name` varchar(1024) NOT NULL,
  `stu_password` varchar(1024) NOT NULL,
  `stu_Email` varchar(1024) NOT NULL,
  `stu_phone` varchar(128) DEFAULT NULL,
  `stu_gender` varchar(128) NOT NULL,
  `stu_college` varchar(1024) DEFAULT NULL,
  `stu_major` varchar(1024) DEFAULT NULL,
  `stu_grade` int DEFAULT NULL,
  `stu_introduction` longtext,
  `stu_valid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_students` */

insert  into `sac_app_students`(`id`,`stu_id`,`stu_name`,`stu_password`,`stu_Email`,`stu_phone`,`stu_gender`,`stu_college`,`stu_major`,`stu_grade`,`stu_introduction`,`stu_valid`) values 
(1,'200031','学生3号','2222','22448479@qq.com','1222341234','男','计算机科学与技术','计算机',2020,'嘛',1),
(2,'200032','学生2号','123456','2425448477@qq.com','12341234567','女','英语','英语',2018,'漂亮',1),
(3,'200033','学生三号','123456','2425448479@qq.com','15151515151','男','生物医学院','生物科学',2019,'帅',1);

/*Table structure for table `sac_app_teams` */

DROP TABLE IF EXISTS `sac_app_teams`;

CREATE TABLE `sac_app_teams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `team_number` int NOT NULL,
  `team_name` varchar(128) DEFAULT NULL,
  `team_header_name` varchar(128) NOT NULL,
  `team_header_phone` varchar(128) NOT NULL,
  `team_introduction` varchar(1024) DEFAULT NULL,
  `team_act_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sac_app_teams_team_act_id_b2b94a70_fk` (`team_act_id`),
  CONSTRAINT `sac_app_teams_team_act_id_b2b94a70_fk` FOREIGN KEY (`team_act_id`) REFERENCES `sac_app_activities` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `sac_app_teams` */

insert  into `sac_app_teams`(`id`,`team_number`,`team_name`,`team_header_name`,`team_header_phone`,`team_introduction`,`team_act_id`) values 
(1,11,'12','学生1号','15202641449','无敌小组',2),
(2,5,'无敌寂寞','学生2号','14312341234','无敌寂寞',3),
(3,7,'冲','学生1号','1565656565','冲',3),
(4,7,'积极','学生2号','123123123','jiji',5);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
