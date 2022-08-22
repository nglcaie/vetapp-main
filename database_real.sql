-- phpMyAdmin SQL Dump
-- version 5.3.0-dev+20220821.84e30c2c86
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 22, 2022 at 12:45 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `database_real`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add breed', 7, 'add_breed'),
(26, 'Can change breed', 7, 'change_breed'),
(27, 'Can delete breed', 7, 'delete_breed'),
(28, 'Can view breed', 7, 'view_breed'),
(29, 'Can add gender', 8, 'add_gender'),
(30, 'Can change gender', 8, 'change_gender'),
(31, 'Can delete gender', 8, 'delete_gender'),
(32, 'Can view gender', 8, 'view_gender'),
(33, 'Can add petspecies', 9, 'add_petspecies'),
(34, 'Can change petspecies', 9, 'change_petspecies'),
(35, 'Can delete petspecies', 9, 'delete_petspecies'),
(36, 'Can view petspecies', 9, 'view_petspecies'),
(37, 'Can add product type', 10, 'add_producttype'),
(38, 'Can change product type', 10, 'change_producttype'),
(39, 'Can delete product type', 10, 'delete_producttype'),
(40, 'Can view product type', 10, 'view_producttype'),
(41, 'Can add services', 11, 'add_services'),
(42, 'Can change services', 11, 'change_services'),
(43, 'Can delete services', 11, 'delete_services'),
(44, 'Can view services', 11, 'view_services'),
(45, 'Can add vax type', 12, 'add_vaxtype'),
(46, 'Can change vax type', 12, 'change_vaxtype'),
(47, 'Can delete vax type', 12, 'delete_vaxtype'),
(48, 'Can view vax type', 12, 'view_vaxtype'),
(49, 'Can add staff profile', 13, 'add_staffprofile'),
(50, 'Can change staff profile', 13, 'change_staffprofile'),
(51, 'Can delete staff profile', 13, 'delete_staffprofile'),
(52, 'Can view staff profile', 13, 'view_staffprofile'),
(53, 'Can add profile', 14, 'add_profile'),
(54, 'Can change profile', 14, 'change_profile'),
(55, 'Can delete profile', 14, 'delete_profile'),
(56, 'Can view profile', 14, 'view_profile'),
(57, 'Can add product info', 15, 'add_productinfo'),
(58, 'Can change product info', 15, 'change_productinfo'),
(59, 'Can delete product info', 15, 'delete_productinfo'),
(60, 'Can view product info', 15, 'view_productinfo'),
(61, 'Can add product', 16, 'add_product'),
(62, 'Can change product', 16, 'change_product'),
(63, 'Can delete product', 16, 'delete_product'),
(64, 'Can view product', 16, 'view_product'),
(65, 'Can add pets', 17, 'add_pets'),
(66, 'Can change pets', 17, 'change_pets'),
(67, 'Can delete pets', 17, 'delete_pets'),
(68, 'Can view pets', 17, 'view_pets'),
(69, 'Can add service history', 18, 'add_servicehistory'),
(70, 'Can change service history', 18, 'change_servicehistory'),
(71, 'Can delete service history', 18, 'delete_servicehistory'),
(72, 'Can view service history', 18, 'view_servicehistory'),
(73, 'Can add medical history', 19, 'add_medicalhistory'),
(74, 'Can change medical history', 19, 'change_medicalhistory'),
(75, 'Can delete medical history', 19, 'delete_medicalhistory'),
(76, 'Can view medical history', 19, 'view_medicalhistory'),
(77, 'Can add charge slip', 20, 'add_chargeslip'),
(78, 'Can change charge slip', 20, 'change_chargeslip'),
(79, 'Can delete charge slip', 20, 'delete_chargeslip'),
(80, 'Can view charge slip', 20, 'view_chargeslip'),
(81, 'Can add vaccine history', 21, 'add_vaccinehistory'),
(82, 'Can change vaccine history', 21, 'change_vaccinehistory'),
(83, 'Can delete vaccine history', 21, 'delete_vaccinehistory'),
(84, 'Can view vaccine history', 21, 'view_vaccinehistory'),
(85, 'Can add transaction', 22, 'add_transaction'),
(86, 'Can change transaction', 22, 'change_transaction'),
(87, 'Can delete transaction', 22, 'delete_transaction'),
(88, 'Can view transaction', 22, 'view_transaction'),
(89, 'Can add service invoice', 23, 'add_serviceinvoice'),
(90, 'Can change service invoice', 23, 'change_serviceinvoice'),
(91, 'Can delete service invoice', 23, 'delete_serviceinvoice'),
(92, 'Can view service invoice', 23, 'view_serviceinvoice'),
(93, 'Can add product invoice', 24, 'add_productinvoice'),
(94, 'Can change product invoice', 24, 'change_productinvoice'),
(95, 'Can delete product invoice', 24, 'delete_productinvoice'),
(96, 'Can view product invoice', 24, 'view_productinvoice'),
(97, 'Can add lab history', 25, 'add_labhistory'),
(98, 'Can change lab history', 25, 'change_labhistory'),
(99, 'Can delete lab history', 25, 'delete_labhistory'),
(100, 'Can view lab history', 25, 'view_labhistory'),
(101, 'Can add schedule_slot', 26, 'add_schedule_slot'),
(102, 'Can change schedule_slot', 26, 'change_schedule_slot'),
(103, 'Can delete schedule_slot', 26, 'delete_schedule_slot'),
(104, 'Can view schedule_slot', 26, 'view_schedule_slot'),
(105, 'Can add scheduling', 27, 'add_scheduling'),
(106, 'Can change scheduling', 27, 'change_scheduling'),
(107, 'Can delete scheduling', 27, 'delete_scheduling'),
(108, 'Can view scheduling', 27, 'view_scheduling'),
(109, 'Can add flagsystem', 28, 'add_flagsystem'),
(110, 'Can change flagsystem', 28, 'change_flagsystem'),
(111, 'Can delete flagsystem', 28, 'delete_flagsystem'),
(112, 'Can view flagsystem', 28, 'view_flagsystem');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2022-08-22 07:17:30.769358', '2', 'javiersofia.as@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(2, '2022-08-22 07:17:41.622683', '1', 'Female', 1, '[{\"added\": {}}]', 8, 1),
(3, '2022-08-22 07:17:44.795892', '2', 'Male', 1, '[{\"added\": {}}]', 8, 1),
(4, '2022-08-22 07:17:50.123900', '3', 'Prefer Not to Say', 1, '[{\"added\": {}}]', 8, 1),
(5, '2022-08-22 07:17:55.549585', '1', 'Sofia Javier', 1, '[{\"added\": {}}]', 14, 1),
(6, '2022-08-22 07:18:09.398238', '3', 'pejenriquez@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(7, '2022-08-22 07:18:26.122639', '2', 'Peja Enriquez', 1, '[{\"added\": {}}]', 14, 1),
(8, '2022-08-22 07:19:07.508139', '4', 'antjav14@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(9, '2022-08-22 07:19:19.287537', '3', 'Anthony Mabilangan', 1, '[{\"added\": {}}]', 14, 1),
(10, '2022-08-22 07:19:31.298499', '4', 'antjav14@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Pet Owner\"]}}]', 6, 1),
(11, '2022-08-22 07:19:55.442459', '5', 'hecbautista@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(12, '2022-08-22 07:20:03.998227', '1', 'Hector Bautista', 1, '[{\"added\": {}}]', 13, 1),
(13, '2022-08-22 07:20:24.375627', '6', 'docdave@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(14, '2022-08-22 07:20:36.274481', '2', 'David Delos Trinos', 1, '[{\"added\": {}}]', 13, 1),
(15, '2022-08-22 07:21:04.299846', '7', 'nathcruz@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(16, '2022-08-22 07:21:10.793302', '3', 'Nathaniel Cruz', 1, '[{\"added\": {}}]', 13, 1),
(17, '2022-08-22 07:21:31.829148', '8', 'jethver@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(18, '2022-08-22 07:21:41.848251', '4', 'Jethro Villaverde', 1, '[{\"added\": {}}]', 13, 1),
(19, '2022-08-22 07:22:07.348337', '9', 'alicemedina@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(20, '2022-08-22 07:22:15.634170', '5', 'Alice Medina', 1, '[{\"added\": {}}]', 13, 1),
(21, '2022-08-22 07:22:47.047134', '1', 'Cat', 1, '[{\"added\": {}}]', 9, 1),
(22, '2022-08-22 07:22:53.325056', '2', 'Dog', 1, '[{\"added\": {}}]', 9, 1),
(23, '2022-08-22 07:23:03.269798', '1', 'Sphynx', 1, '[{\"added\": {}}]', 7, 1),
(24, '2022-08-22 07:23:36.749114', '2', 'Persian', 1, '[{\"added\": {}}]', 7, 1),
(25, '2022-08-22 07:23:47.681867', '3', 'Bengal', 1, '[{\"added\": {}}]', 7, 1),
(26, '2022-08-22 07:23:55.708074', '4', 'Ragdoll', 1, '[{\"added\": {}}]', 7, 1),
(27, '2022-08-22 07:24:15.515902', '5', 'Pomeranian', 1, '[{\"added\": {}}]', 7, 1),
(28, '2022-08-22 07:24:22.263999', '6', 'Shih Tzu', 1, '[{\"added\": {}}]', 7, 1),
(29, '2022-08-22 07:24:31.140878', '7', 'Dalmatian', 1, '[{\"added\": {}}]', 7, 1),
(30, '2022-08-22 07:25:04.930276', '8', 'Bulldog', 1, '[{\"added\": {}}]', 7, 1),
(31, '2022-08-22 07:25:12.619983', '9', 'Poodle', 1, '[{\"added\": {}}]', 7, 1),
(32, '2022-08-22 07:25:22.660841', '10', 'Pug', 1, '[{\"added\": {}}]', 7, 1),
(33, '2022-08-22 07:25:44.456339', '11', 'Somali Cat', 1, '[{\"added\": {}}]', 7, 1),
(34, '2022-08-22 07:26:16.477001', '1', 'Food', 1, '[{\"added\": {}}]', 10, 1),
(35, '2022-08-22 07:26:24.012910', '2', 'Medecine', 1, '[{\"added\": {}}]', 10, 1),
(36, '2022-08-22 07:26:31.653172', '2', 'Medicine', 2, '[{\"changed\": {\"fields\": [\"Vaccine Type\"]}}]', 10, 1),
(37, '2022-08-22 07:26:43.437449', '3', 'Vaccine', 1, '[{\"added\": {}}]', 10, 1),
(38, '2022-08-22 07:28:32.829100', '1', 'Maxime Dry Dog Food - Beef', 1, '[{\"added\": {}}]', 15, 1),
(39, '2022-08-22 08:16:24.778046', '3', 'scheduling object (3)', 2, '[{\"changed\": {\"fields\": [\"Code\"]}}]', 27, 1),
(40, '2022-08-22 08:16:28.184662', '3', 'scheduling object (3)', 2, '[]', 27, 1),
(41, '2022-08-22 08:16:33.074396', '2', 'scheduling object (2)', 2, '[{\"changed\": {\"fields\": [\"Code\"]}}]', 27, 1),
(42, '2022-08-22 08:16:38.527802', '1', 'scheduling object (1)', 2, '[{\"changed\": {\"fields\": [\"Code\"]}}]', 27, 1),
(43, '2022-08-22 08:16:46.395636', '3', 'scheduling object (3)', 2, '[]', 27, 1),
(44, '2022-08-22 08:16:56.198790', '2', 'scheduling object (2)', 2, '[{\"changed\": {\"fields\": [\"Pet\"]}}]', 27, 1),
(45, '2022-08-22 08:21:49.024033', '3', 'Anthony Mabilangan-3', 2, '[{\"changed\": {\"fields\": [\"Balance\", \"Status\"]}}]', 20, 1),
(46, '2022-08-22 08:21:54.657396', '2', 'Anthony Mabilangan-2', 2, '[]', 20, 1),
(47, '2022-08-22 08:26:31.013220', '1', 'flagsystem object (1)', 1, '[{\"added\": {}}]', 28, 1),
(48, '2022-08-22 08:26:58.766443', '5', 'scheduling object (5)', 2, '[{\"changed\": {\"fields\": [\"Code\"]}}]', 27, 1),
(49, '2022-08-22 08:27:11.929580', '4', 'scheduling object (4)', 2, '[{\"changed\": {\"fields\": [\"Code\", \"Status\"]}}]', 27, 1),
(50, '2022-08-22 08:27:21.666899', '3', 'scheduling object (3)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 27, 1),
(51, '2022-08-22 08:27:26.181388', '2', 'scheduling object (2)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 27, 1),
(52, '2022-08-22 08:27:36.725248', '1', 'scheduling object (1)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 27, 1),
(53, '2022-08-22 08:27:43.402967', '5', 'scheduling object (5)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 27, 1),
(54, '2022-08-22 08:27:45.897328', '4', 'scheduling object (4)', 2, '[]', 27, 1),
(55, '2022-08-22 08:27:49.534311', '2', 'scheduling object (2)', 2, '[]', 27, 1),
(56, '2022-08-22 08:28:02.904577', '2', 'flagsystem object (2)', 1, '[{\"added\": {}}]', 28, 1),
(57, '2022-08-22 08:28:04.886745', '2', 'flagsystem object (2)', 2, '[]', 28, 1),
(58, '2022-08-22 10:38:42.378048', '5', 'secretary@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Email\"]}}]', 6, 1),
(59, '2022-08-22 10:40:40.564910', '5', 'secretary@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(60, '2022-08-22 10:41:12.017329', '10', 'awllabore@gmail.com', 1, '[{\"added\": {}}]', 6, 1),
(61, '2022-08-22 10:41:19.142637', '10', 'awllabore@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Is used\"]}}]', 6, 1),
(62, '2022-08-22 10:41:52.029692', '4', 'Beatrize Balderama', 1, '[{\"added\": {}}]', 14, 1),
(63, '2022-08-22 10:44:18.506146', '2', 'javiersofia.as@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(64, '2022-08-22 10:44:36.397569', '3', 'pejenriquez@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(65, '2022-08-22 10:44:41.534246', '4', 'antjav14@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(66, '2022-08-22 10:44:48.031839', '6', 'docdave@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(67, '2022-08-22 10:44:54.176469', '7', 'nathcruz@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(68, '2022-08-22 10:45:00.665448', '8', 'jethver@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(69, '2022-08-22 10:45:06.436868', '9', 'alicemedina@gmail.com', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(7, 'vet', 'breed'),
(20, 'vet', 'chargeslip'),
(28, 'vet', 'flagsystem'),
(8, 'vet', 'gender'),
(25, 'vet', 'labhistory'),
(19, 'vet', 'medicalhistory'),
(17, 'vet', 'pets'),
(9, 'vet', 'petspecies'),
(16, 'vet', 'product'),
(15, 'vet', 'productinfo'),
(24, 'vet', 'productinvoice'),
(10, 'vet', 'producttype'),
(14, 'vet', 'profile'),
(26, 'vet', 'schedule_slot'),
(27, 'vet', 'scheduling'),
(18, 'vet', 'servicehistory'),
(23, 'vet', 'serviceinvoice'),
(11, 'vet', 'services'),
(13, 'vet', 'staffprofile'),
(22, 'vet', 'transaction'),
(6, 'vet', 'user'),
(21, 'vet', 'vaccinehistory'),
(12, 'vet', 'vaxtype');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'vet', '0001_initial', '2022-08-22 07:13:31.333366'),
(2, 'contenttypes', '0001_initial', '2022-08-22 07:13:31.382528'),
(3, 'admin', '0001_initial', '2022-08-22 07:13:31.501181'),
(4, 'admin', '0002_logentry_remove_auto_add', '2022-08-22 07:13:31.514225'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2022-08-22 07:13:31.529160'),
(6, 'contenttypes', '0002_remove_content_type_name', '2022-08-22 07:13:31.608422'),
(7, 'auth', '0001_initial', '2022-08-22 07:13:31.914251'),
(8, 'auth', '0002_alter_permission_name_max_length', '2022-08-22 07:13:31.971227'),
(9, 'auth', '0003_alter_user_email_max_length', '2022-08-22 07:13:31.985274'),
(10, 'auth', '0004_alter_user_username_opts', '2022-08-22 07:13:31.996306'),
(11, 'auth', '0005_alter_user_last_login_null', '2022-08-22 07:13:32.009350'),
(12, 'auth', '0006_require_contenttypes_0002', '2022-08-22 07:13:32.015373'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2022-08-22 07:13:32.029417'),
(14, 'auth', '0008_alter_user_username_max_length', '2022-08-22 07:13:32.042460'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2022-08-22 07:13:32.056506'),
(16, 'auth', '0010_alter_group_name_max_length', '2022-08-22 07:13:32.088613'),
(17, 'auth', '0011_update_proxy_permissions', '2022-08-22 07:13:32.113694'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2022-08-22 07:13:32.125734'),
(19, 'sessions', '0001_initial', '2022-08-22 07:13:32.168877'),
(20, 'vet', '0002_delete_veterinarianprofile', '2022-08-22 07:13:32.179914'),
(21, 'vet', '0003_productinfo_low_margin_productinfo_medium_margin', '2022-08-22 07:13:32.240114'),
(22, 'vet', '0004_alter_productinfo_low_margin_and_more', '2022-08-22 07:13:32.358293'),
(23, 'vet', '0005_services_is_vaccination_alter_breed_kind_and_more', '2022-08-22 07:13:32.802950'),
(24, 'vet', '0006_alter_servicehistory_medhistory', '2022-08-22 07:13:37.324784'),
(25, 'vet', '0007_medicalhistory_dateofreturn_medicalhistory_reason', '2022-08-22 07:13:37.367925'),
(26, 'vet', '0008_alter_servicehistory_options', '2022-08-22 07:13:37.379650'),
(27, 'vet', '0009_chargeslip_alter_servicehistory_options_and_more', '2022-08-22 07:13:38.925715'),
(28, 'vet', '0010_labhistory_vet_vaccinehistory_vet', '2022-08-22 07:13:39.044238'),
(29, 'vet', '0011_labhistory_code_servicehistory_code_and_more', '2022-08-22 07:13:39.495872'),
(30, 'vet', '0012_serviceinvoice_servicecode', '2022-08-22 07:13:39.521275'),
(31, 'vet', '0013_chargeslip_date_of_delete_chargeslip_is_deleted_and_more', '2022-08-22 07:13:39.861195'),
(32, 'vet', '0014_transaction_code', '2022-08-22 07:13:39.906183'),
(33, 'vet', '0015_pets_user_image_profile_user_image_and_more', '2022-08-22 07:13:40.001500'),
(34, 'vet', '0016_schedule_slot_scheduling', '2022-08-22 07:13:40.199310'),
(35, 'vet', '0017_auto_20220723_1320', '2022-08-22 07:13:40.222386'),
(36, 'vet', '0018_alter_schedule_slot_timein_and_more', '2022-08-22 07:13:40.608221'),
(37, 'vet', '0019_scheduling_date', '2022-08-22 07:13:40.635309'),
(38, 'vet', '0020_scheduling_date_of_cancelled', '2022-08-22 07:13:40.660153'),
(39, 'vet', '0021_flagsystem', '2022-08-22 07:13:40.768510'),
(40, 'vet', '0022_productinvoice_date_serviceinvoice_date_and_more', '2022-08-22 07:13:40.924230'),
(41, 'vet', '0023_alter_transaction_date', '2022-08-22 07:13:41.061971'),
(42, 'vet', '0024_remove_pets_user_image_pets_pet_image', '2022-08-22 07:13:41.117153'),
(43, 'vet', '0025_scheduling_received', '2022-08-22 07:13:41.150264'),
(44, 'vet', '0026_remove_scheduling_arrived_and_more', '2022-08-22 07:13:41.256614'),
(45, 'vet', '0027_alter_scheduling_status', '2022-08-22 07:13:41.271946'),
(46, 'vet', '0028_alter_user_is_used', '2022-08-22 07:15:53.662393'),
(47, 'vet', '0029_alter_user_is_used', '2022-08-22 10:35:31.109208');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('37osswioqj7duraqyg7tgq3un4s6q2d8', '.eJxVjMsOwiAQRf-FtSFAeUxduvcbyDCMUjWQlHZl_HdD0oVu7znnvkXEfStx77zGJYuz0OL0uyWkJ9cB8gPrvUlqdVuXJIciD9rltWV-XQ7376BgL6P2TpOiZMwMGsG52RCbYBkAkqGAymbtyXqbppsmqwJzDqwCODYKJvH5As8_N0Q:1oQ4va:G2Xe_cNqisqL-9W7LEb_2UCeHy8iQG3tROZGHq2UmSw', '2022-09-05 10:45:06.447569'),
('qx1olq8nbhzjeuxbjwhl2gppfqjtrnbt', '.eJxVjMsOwiAQRf-FtSFAeUxduvcbyDCMUjWQlHZl_HdD0oVu7znnvkXEfStx77zGJYuz0OL0uyWkJ9cB8gPrvUlqdVuXJIciD9rltWV-XQ7376BgL6P2TpOiZMwMGsG52RCbYBkAkqGAymbtyXqbppsmqwJzDqwCODYKJvH5As8_N0Q:1oQ2We:dXGhmYr_2IhvcfW-z3cUG6IHC8dMgm1OHbAZQvT98Bg', '2022-09-05 08:11:12.839351');

-- --------------------------------------------------------

--
-- Table structure for table `vet_breed`
--

CREATE TABLE `vet_breed` (
  `id` bigint(20) NOT NULL,
  `breed` varchar(50) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `kind_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_breed`
--

INSERT INTO `vet_breed` (`id`, `breed`, `is_deleted`, `date_of_delete`, `kind_id`) VALUES
(1, 'Sphynx', 0, NULL, 1),
(2, 'Persian', 0, NULL, 1),
(3, 'Bengal', 0, NULL, 1),
(4, 'Ragdoll', 0, NULL, 1),
(5, 'Pomeranian', 0, NULL, 2),
(6, 'Shih Tzu', 0, NULL, 2),
(7, 'Dalmatian', 0, NULL, 2),
(8, 'Bulldog', 0, NULL, 2),
(9, 'Poodle', 0, NULL, 2),
(10, 'Pug', 0, NULL, 2),
(11, 'Somali Cat', 0, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `vet_chargeslip`
--

CREATE TABLE `vet_chargeslip` (
  `id` bigint(20) NOT NULL,
  `code` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `totalAmount` decimal(20,2) NOT NULL,
  `balance` decimal(20,2) NOT NULL,
  `status` varchar(200) DEFAULT NULL,
  `petowner_id` bigint(20) DEFAULT NULL,
  `staff_id` bigint(20) DEFAULT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `last_modified` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_chargeslip`
--

INSERT INTO `vet_chargeslip` (`id`, `code`, `date`, `totalAmount`, `balance`, `status`, `petowner_id`, `staff_id`, `date_of_delete`, `is_deleted`, `last_modified`) VALUES
(1, 'CSefded', '2022-08-22', '400.00', '0.00', 'Fully Paid', 2, 2, NULL, 0, '2022-08-22 08:20:04.185248'),
(2, 'CS7eb82', '2022-08-22', '250.00', '0.00', 'Fully Paid', 3, 2, NULL, 0, '2022-08-22 08:21:54.656016'),
(3, 'CS81df9', '2022-08-22', '250.00', '0.00', 'Fully Paid', 3, 2, NULL, 0, '2022-08-22 08:21:49.022028'),
(4, 'CS2fb95', '2022-08-22', '550.00', '0.00', 'Fully Paid', 1, 2, NULL, 0, '2022-08-22 08:22:07.254970'),
(5, 'CSf2aef', '2022-08-22', '13995.00', '0.00', 'Fully Paid', NULL, NULL, NULL, 0, '2022-08-22 08:20:54.420322');

-- --------------------------------------------------------

--
-- Table structure for table `vet_flagsystem`
--

CREATE TABLE `vet_flagsystem` (
  `id` bigint(20) NOT NULL,
  `flagpoints` int(11) DEFAULT NULL,
  `is_restricted` tinyint(1) NOT NULL,
  `petOwner_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_flagsystem`
--

INSERT INTO `vet_flagsystem` (`id`, `flagpoints`, `is_restricted`, `petOwner_id`) VALUES
(1, 1, 0, 2),
(2, 1, 0, 3);

-- --------------------------------------------------------

--
-- Table structure for table `vet_gender`
--

CREATE TABLE `vet_gender` (
  `id` bigint(20) NOT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_gender`
--

INSERT INTO `vet_gender` (`id`, `gender`, `is_deleted`) VALUES
(1, 'Female', 0),
(2, 'Male', 0),
(3, 'Prefer Not to Say', 0);

-- --------------------------------------------------------

--
-- Table structure for table `vet_labhistory`
--

CREATE TABLE `vet_labhistory` (
  `id` bigint(20) NOT NULL,
  `dateofService` date NOT NULL,
  `dateofResult` date DEFAULT NULL,
  `interpretation` varchar(1000) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `last_modified` datetime(6) DEFAULT NULL,
  `medHistory_id` bigint(20) NOT NULL,
  `service_id` bigint(20) NOT NULL,
  `vet_id` bigint(20) DEFAULT NULL,
  `code` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_labhistory`
--

INSERT INTO `vet_labhistory` (`id`, `dateofService`, `dateofResult`, `interpretation`, `is_deleted`, `date_of_delete`, `last_modified`, `medHistory_id`, `service_id`, `vet_id`, `code`) VALUES
(1, '2022-08-04', '2022-08-04', '', 0, NULL, '2022-08-22 08:10:55.989976', 4, 11, 5, 'LT6eebf');

-- --------------------------------------------------------

--
-- Table structure for table `vet_medicalhistory`
--

CREATE TABLE `vet_medicalhistory` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `weight` varchar(100) DEFAULT NULL,
  `symptoms` varchar(1000) DEFAULT NULL,
  `treatment` varchar(1000) DEFAULT NULL,
  `prescription` varchar(1000) DEFAULT NULL,
  `instruction` varchar(1000) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `pet_id` bigint(20) NOT NULL,
  `vet_id` bigint(20) DEFAULT NULL,
  `dateofReturn` date DEFAULT NULL,
  `reason` varchar(1000) DEFAULT NULL,
  `code` varchar(200) DEFAULT NULL,
  `last_modified` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_medicalhistory`
--

INSERT INTO `vet_medicalhistory` (`id`, `date`, `weight`, `symptoms`, `treatment`, `prescription`, `instruction`, `is_deleted`, `date_of_delete`, `pet_id`, `vet_id`, `dateofReturn`, `reason`, `code`, `last_modified`) VALUES
(1, '2021-12-08', '5 kg', '', '', '', '', 0, NULL, 1, 2, NULL, '', 'PTe1366', '2022-08-22 08:05:35.256479'),
(2, '2022-08-05', '2', '', '', '', '', 0, NULL, 2, 3, NULL, '', 'PTb84ee', '2022-08-22 08:06:19.784930'),
(3, '2022-08-05', '2 kg', '', '', '', '', 0, NULL, 3, 3, NULL, '', 'PTa3293', '2022-08-22 08:11:59.044864'),
(4, '2022-08-04', '5 kg', 'Fever and Diarrhea', 'Medicine', 'Propyrin Analgesic', '2 ml / day', 0, NULL, 4, 5, '2022-08-12', 'Follow-up', 'PTaf5a4', '2022-08-22 08:10:32.294432');

-- --------------------------------------------------------

--
-- Table structure for table `vet_pets`
--

CREATE TABLE `vet_pets` (
  `id` bigint(20) NOT NULL,
  `petName` varchar(50) DEFAULT NULL,
  `dob` date NOT NULL,
  `sex` varchar(50) DEFAULT NULL,
  `colorMarking` varchar(50) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `description_id` bigint(20) DEFAULT NULL,
  `petOwner_id` bigint(20) DEFAULT NULL,
  `species_id` bigint(20) DEFAULT NULL,
  `pet_image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_pets`
--

INSERT INTO `vet_pets` (`id`, `petName`, `dob`, `sex`, `colorMarking`, `is_deleted`, `date_of_delete`, `description_id`, `petOwner_id`, `species_id`, `pet_image`) VALUES
(1, 'Coco', '2018-09-22', 'Male', 'White-Brown', 0, NULL, 6, 2, 2, 'pet_img/pet_img.png'),
(2, 'Chip', '2022-06-02', 'Male', 'Brown', 0, NULL, 9, 3, 2, 'pet_img/pet_img.png'),
(3, 'Chap', '2022-06-02', 'Female', 'Black', 0, NULL, 9, 3, 2, 'pet_img/pet_img.png'),
(4, 'Mollie', '2021-07-01', 'Female', 'White', 0, NULL, 6, 1, 2, 'pet_img/pet_img.png');

-- --------------------------------------------------------

--
-- Table structure for table `vet_petspecies`
--

CREATE TABLE `vet_petspecies` (
  `id` bigint(20) NOT NULL,
  `species` varchar(50) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_petspecies`
--

INSERT INTO `vet_petspecies` (`id`, `species`, `is_deleted`, `date_of_delete`) VALUES
(1, 'Cat', 0, NULL),
(2, 'Dog', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `vet_product`
--

CREATE TABLE `vet_product` (
  `id` bigint(20) NOT NULL,
  `manuDate` date DEFAULT NULL,
  `expireDate` date DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_product`
--

INSERT INTO `vet_product` (`id`, `manuDate`, `expireDate`, `quantity`, `is_deleted`, `date_of_delete`, `product_id`) VALUES
(1, '2022-06-02', '2023-04-21', 70, 0, NULL, 1),
(2, '2021-12-31', '2023-06-10', 50, 0, NULL, 2),
(3, '2021-12-11', '2022-12-03', 295, 0, NULL, 3),
(4, '2022-04-06', '2022-12-23', 250, 0, NULL, 4),
(5, '2022-03-04', '2023-02-10', 350, 0, NULL, 5),
(6, '2022-08-05', '2023-08-23', 498, 0, NULL, 14),
(7, '2022-07-01', '2023-03-23', 500, 0, NULL, 13),
(8, '2022-04-01', '2023-02-01', 100, 0, NULL, 7),
(9, '2022-04-01', '2023-04-22', 50, 0, NULL, 9),
(10, '2022-08-05', '2023-03-31', 30, 0, NULL, 10),
(11, '2022-05-06', '2022-11-26', 10, 0, NULL, 11);

-- --------------------------------------------------------

--
-- Table structure for table `vet_productinfo`
--

CREATE TABLE `vet_productinfo` (
  `id` bigint(20) NOT NULL,
  `product_name` varchar(200) NOT NULL,
  `description` varchar(200) NOT NULL,
  `price` decimal(20,2) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `total_quantity` int(11) DEFAULT NULL,
  `product_type_id` bigint(20) NOT NULL,
  `low_margin` int(11) DEFAULT NULL,
  `medium_margin` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_productinfo`
--

INSERT INTO `vet_productinfo` (`id`, `product_name`, `description`, `price`, `is_deleted`, `date_of_delete`, `status`, `total_quantity`, `product_type_id`, `low_margin`, `medium_margin`) VALUES
(1, 'Maxime Dry Dog Food - Beef', '400g Beef Flavor', '76.00', 0, NULL, 'High in Stock', 70, 1, 20, 50),
(2, 'Aozi Beef Wet Dog Food', '430 g', '158.00', 0, NULL, 'Medium in Stock', 50, 1, 20, 50),
(3, 'Royal Canin Mini Puppy Dry Dog Food', '8 kg', '2799.00', 0, NULL, 'High in Stock', 300, 1, 5, 10),
(4, 'Royal Canin Mini Adult Dry Dog Food', '8kg', '2671.00', 0, NULL, 'High in Stock', 250, 1, 5, 10),
(5, 'Bow Wow Canned Dog Food Beef and Vegetables', '375g', '89.00', 0, NULL, 'High in Stock', 350, 1, 20, 50),
(6, 'Aozi Organic Puppy Dog Food (Beef, Egg and Spinach Flavor)', '1kg', '180.00', 0, NULL, 'No Stock', 0, 1, 20, 50),
(7, 'Propyrin Analgesic', 'Fever Wound Medicine for Dogs', '279.00', 0, NULL, 'High in Stock', 100, 2, 20, 50),
(8, 'DHPP', '5 in 1', '0.00', 0, NULL, 'No Stock', 0, 3, 50, 100),
(9, 'Papi Doxy cycline', 'anti-bacterial', '249.00', 0, NULL, 'Medium in Stock', 50, 2, 20, 50),
(10, 'Himalaya Immunol', '60 tablets', '379.00', 0, NULL, 'Medium in Stock', 30, 2, 20, 50),
(11, 'LC VIT Multivitamins for Dogs Syrup', '60 ml', '78.00', 0, NULL, 'Low in Stock', 10, 2, 20, 50),
(12, 'LC VIT Multivitamins for Dogs Syrup', '120 ml', '125.00', 0, NULL, 'No Stock', 0, 2, 20, 50),
(13, 'Anti-Parvo', 'vaccin for parvo', '0.00', 0, NULL, 'High in Stock', 500, 3, 50, 100),
(14, 'Anti-Rabies', 'vaccine for rabies', '0.00', 0, NULL, 'High in Stock', 498, 3, 50, 100);

-- --------------------------------------------------------

--
-- Table structure for table `vet_productinvoice`
--

CREATE TABLE `vet_productinvoice` (
  `id` bigint(20) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total` decimal(20,2) NOT NULL,
  `chargeslip_id` bigint(20) DEFAULT NULL,
  `product_id` bigint(20) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `last_modified` datetime(6) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_productinvoice`
--

INSERT INTO `vet_productinvoice` (`id`, `quantity`, `total`, `chargeslip_id`, `product_id`, `date_of_delete`, `is_deleted`, `last_modified`, `date`) VALUES
(1, 5, '13995.00', 5, 3, NULL, 0, '2022-08-22 08:20:45.579119', '2022-08-22');

-- --------------------------------------------------------

--
-- Table structure for table `vet_producttype`
--

CREATE TABLE `vet_producttype` (
  `id` bigint(20) NOT NULL,
  `prodType` varchar(50) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_producttype`
--

INSERT INTO `vet_producttype` (`id`, `prodType`, `is_deleted`, `date_of_delete`) VALUES
(1, 'Food', 0, NULL),
(2, 'Medicine', 0, NULL),
(3, 'Vaccine', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `vet_profile`
--

CREATE TABLE `vet_profile` (
  `id` bigint(20) NOT NULL,
  `firstName` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `contactNum` varchar(50) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `gender_id` bigint(20) DEFAULT NULL,
  `useracc_id` bigint(20) DEFAULT NULL,
  `user_image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_profile`
--

INSERT INTO `vet_profile` (`id`, `firstName`, `lastName`, `contactNum`, `address`, `is_deleted`, `date_of_delete`, `gender_id`, `useracc_id`, `user_image`) VALUES
(1, 'Sofia', 'Javier', '09954146136', '1454 Franco St. Tondo, Manila', 0, NULL, 1, 2, 'profile_pic/image.jpg'),
(2, 'Peja', 'Enriquez', NULL, 'Quezon City', 0, NULL, 2, 3, 'profile_pic/image.jpg'),
(3, 'Anthony', 'Mabilangan', NULL, 'Manila', 0, NULL, 1, 4, 'profile_pic/image.jpg'),
(4, 'Beatrize', 'Balderama', NULL, NULL, 0, NULL, 1, 10, 'profile_pic/image.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `vet_schedule_slot`
--

CREATE TABLE `vet_schedule_slot` (
  `id` bigint(20) NOT NULL,
  `code` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `timeIn` time(6) DEFAULT NULL,
  `timeOut` time(6) DEFAULT NULL,
  `is_reserved` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `vet_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_schedule_slot`
--

INSERT INTO `vet_schedule_slot` (`id`, `code`, `date`, `timeIn`, `timeOut`, `is_reserved`, `is_deleted`, `date_of_delete`, `vet_id`) VALUES
(1, 'CSc3e25', '2022-08-10', '08:30:00.000000', '09:00:00.000000', 1, 0, NULL, 2),
(2, 'CS3f728', '2022-08-10', '09:00:00.000000', '09:30:00.000000', 1, 0, NULL, 2),
(3, 'CSeecca', '2022-08-10', '08:30:00.000000', '09:00:00.000000', 0, 0, NULL, 3),
(4, 'CS5f3b8', '2022-08-10', '10:00:00.000000', '10:30:00.000000', 0, 0, NULL, 2),
(5, 'CSd9345', '2022-08-10', '11:00:00.000000', '11:30:00.000000', 0, 0, NULL, 3),
(6, 'CSa2290', '2022-08-11', '08:30:00.000000', '09:00:00.000000', 0, 0, NULL, 3),
(7, 'CS38dfd', '2022-08-11', '09:00:00.000000', '09:30:00.000000', 0, 0, NULL, 3),
(8, 'CS96532', '2022-08-11', '10:00:00.000000', '10:30:00.000000', 0, 0, NULL, 3),
(9, 'CSbb5d6', '2022-08-10', '13:00:00.000000', '13:30:00.000000', 0, 0, NULL, 3),
(10, 'CSe1dfa', '2022-08-10', '14:00:00.000000', '14:30:00.000000', 0, 0, NULL, 4),
(11, 'CS53b42', '2022-08-11', '14:00:00.000000', '14:30:00.000000', 1, 0, NULL, 3),
(12, 'CScdc19', '2022-08-12', '09:00:00.000000', '09:30:00.000000', 1, 0, NULL, 5),
(13, 'CSb85f6', '2022-08-12', '08:30:00.000000', '09:00:00.000000', 0, 0, NULL, 5),
(14, 'CSeb29e', '2022-08-12', '10:00:00.000000', '10:30:00.000000', 1, 0, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `vet_scheduling`
--

CREATE TABLE `vet_scheduling` (
  `id` bigint(20) NOT NULL,
  `code` varchar(200) DEFAULT NULL,
  `reason` varchar(200) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `pet_id` bigint(20) NOT NULL,
  `slot_id` bigint(20) NOT NULL,
  `date` date DEFAULT NULL,
  `date_of_cancelled` datetime(6) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_scheduling`
--

INSERT INTO `vet_scheduling` (`id`, `code`, `reason`, `is_deleted`, `date_of_delete`, `pet_id`, `slot_id`, `date`, `date_of_cancelled`, `status`) VALUES
(1, 'PS3jj35', 'Consultation', 0, NULL, 2, 1, '2022-08-10', NULL, 'Did Not Arrive'),
(2, 'PS4js35', 'Consultation', 0, NULL, 1, 2, '2022-08-10', NULL, 'Arrived'),
(3, 'PS4jj35', 'Consultation', 0, NULL, 3, 12, '2022-08-12', NULL, 'Arrived'),
(4, 'PS4jj366', 'Consultation', 0, NULL, 1, 14, '2022-08-12', NULL, 'Did Not Arrive'),
(5, 'PS34jj35', 'Consultation', 0, NULL, 4, 11, '2022-08-11', NULL, 'Arrived');

-- --------------------------------------------------------

--
-- Table structure for table `vet_servicehistory`
--

CREATE TABLE `vet_servicehistory` (
  `id` bigint(20) NOT NULL,
  `dateofService` date NOT NULL,
  `interpretation` varchar(1000) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `medHistory_id` bigint(20) NOT NULL,
  `service_id` bigint(20) NOT NULL,
  `vet_id` bigint(20) DEFAULT NULL,
  `last_modified` datetime(6) DEFAULT NULL,
  `code` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_servicehistory`
--

INSERT INTO `vet_servicehistory` (`id`, `dateofService`, `interpretation`, `is_deleted`, `date_of_delete`, `medHistory_id`, `service_id`, `vet_id`, `last_modified`, `code`) VALUES
(1, '2021-12-08', '', 0, NULL, 1, 1, 2, '2022-08-22 08:05:49.392707', 'GS6a0fd'),
(2, '2022-08-04', '', 0, NULL, 4, 2, 5, '2022-08-22 08:10:41.958073', 'GS28c73');

-- --------------------------------------------------------

--
-- Table structure for table `vet_serviceinvoice`
--

CREATE TABLE `vet_serviceinvoice` (
  `id` bigint(20) NOT NULL,
  `total` decimal(20,2) NOT NULL,
  `chargeslip_id` bigint(20) NOT NULL,
  `service_id` bigint(20) NOT NULL,
  `servicecode` varchar(200) DEFAULT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `last_modified` datetime(6) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_serviceinvoice`
--

INSERT INTO `vet_serviceinvoice` (`id`, `total`, `chargeslip_id`, `service_id`, `servicecode`, `date_of_delete`, `is_deleted`, `last_modified`, `date`) VALUES
(1, '400.00', 1, 1, 'GS6a0fd', NULL, 0, '2022-08-22 08:11:38.182501', '2022-08-22'),
(2, '250.00', 2, 5, 'VSc5090', NULL, 0, '2022-08-22 08:11:50.304048', '2022-08-22'),
(3, '250.00', 3, 5, 'VS49a2c', NULL, 0, '2022-08-22 08:12:02.269731', '2022-08-22'),
(4, '250.00', 4, 2, 'GS28c73', NULL, 0, '2022-08-22 08:12:11.504595', '2022-08-22'),
(5, '300.00', 4, 11, 'LT6eebf', NULL, 0, '2022-08-22 08:12:11.508611', '2022-08-22');

-- --------------------------------------------------------

--
-- Table structure for table `vet_services`
--

CREATE TABLE `vet_services` (
  `id` bigint(20) NOT NULL,
  `serviceName` varchar(50) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `is_labTest` tinyint(1) NOT NULL,
  `price` decimal(20,2) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `is_vaccination` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_services`
--

INSERT INTO `vet_services` (`id`, `serviceName`, `description`, `is_labTest`, `price`, `is_deleted`, `date_of_delete`, `is_vaccination`) VALUES
(1, 'Grooming', 'Bathing and Cleaning', 0, '400.00', 0, NULL, 0),
(2, 'Consultation/Professional Fee', 'Check-up', 0, '250.00', 0, NULL, 0),
(3, 'Dog Vaccination (5 in 1)', 'Dog vaccine', 0, '400.00', 0, NULL, 1),
(4, 'Cat Vaccination (5 in 1)', 'Cat vaccine', 0, '650.00', 0, NULL, 1),
(5, 'Anti-Rabies', 'anti-rabies', 0, '250.00', 0, NULL, 1),
(6, 'Deworming', 'treatment to free pets from worm', 0, '250.00', 0, NULL, 1),
(7, 'Parvo Test', 'test for parvo', 0, '500.00', 0, NULL, 0),
(8, 'Blood Test (CBC & Blood Chem)', 'test for blood', 1, '800.00', 0, NULL, 0),
(9, 'Urinalysis', 'urine test', 1, '500.00', 0, NULL, 0),
(10, 'Ultrasound', 'ultrasound', 1, '650.00', 0, NULL, 0),
(11, 'Fecalysis', 'stool test', 1, '300.00', 0, NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `vet_staffprofile`
--

CREATE TABLE `vet_staffprofile` (
  `id` bigint(20) NOT NULL,
  `firstName` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `contactNum` varchar(50) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `gender_id` bigint(20) DEFAULT NULL,
  `useracc_id` bigint(20) DEFAULT NULL,
  `user_image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_staffprofile`
--

INSERT INTO `vet_staffprofile` (`id`, `firstName`, `lastName`, `contactNum`, `address`, `is_deleted`, `date_of_delete`, `gender_id`, `useracc_id`, `user_image`) VALUES
(1, 'Hector', 'Bautista', NULL, NULL, 0, NULL, 2, 5, 'profile_pic/image.jpg'),
(2, 'David', 'Delos Trinos', NULL, NULL, 0, NULL, 2, 6, 'profile_pic/image.jpg'),
(3, 'Nathaniel', 'Cruz', NULL, NULL, 0, NULL, 2, 7, 'profile_pic/image.jpg'),
(4, 'Jethro', 'Villaverde', NULL, NULL, 0, NULL, 2, 8, 'profile_pic/image.jpg'),
(5, 'Alice', 'Medina', NULL, NULL, 0, NULL, 1, 9, 'profile_pic/image.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `vet_transaction`
--

CREATE TABLE `vet_transaction` (
  `id` bigint(20) NOT NULL,
  `date` date DEFAULT NULL,
  `grandTotal` decimal(20,2) NOT NULL,
  `tenderedAmount` decimal(20,2) NOT NULL,
  `changeAmount` decimal(20,2) NOT NULL,
  `chargeslip_id` bigint(20) NOT NULL,
  `staff_id` bigint(20) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `last_modified` datetime(6) DEFAULT NULL,
  `code` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_transaction`
--

INSERT INTO `vet_transaction` (`id`, `date`, `grandTotal`, `tenderedAmount`, `changeAmount`, `chargeslip_id`, `staff_id`, `date_of_delete`, `is_deleted`, `last_modified`, `code`) VALUES
(1, '2022-08-22', '400.00', '500.00', '100.00', 1, 1, NULL, 0, '2022-08-22 08:20:04.183244', 'THe674a'),
(2, '2022-08-22', '13995.00', '14000.00', '5.00', 5, 1, NULL, 0, '2022-08-22 08:20:54.416308', 'THa9774'),
(3, '2022-08-22', '250.00', '500.00', '250.00', 2, 1, NULL, 0, '2022-08-22 08:21:03.037012', 'THe53c'),
(4, '2022-08-22', '550.00', '1000.00', '450.00', 4, 1, NULL, 0, '2022-08-22 08:22:07.252963', 'TH8c0ba');

-- --------------------------------------------------------

--
-- Table structure for table `vet_user`
--

CREATE TABLE `vet_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(60) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_of_inactive` datetime(6) DEFAULT NULL,
  `is_used` tinyint(1) NOT NULL,
  `is_secretary` tinyint(1) NOT NULL,
  `is_headveterinarian` tinyint(1) NOT NULL,
  `is_veterinarian` tinyint(1) NOT NULL,
  `is_petowner` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_user`
--

INSERT INTO `vet_user` (`id`, `password`, `email`, `date_joined`, `last_login`, `is_admin`, `is_active`, `date_of_inactive`, `is_used`, `is_secretary`, `is_headveterinarian`, `is_veterinarian`, `is_petowner`) VALUES
(1, 'pbkdf2_sha256$320000$EnzfRpAoD5hdo02iPpz70j$lTTPBzhH2MkfIonbRldRiLpfjJDqMXlQK0XP5/jaFaE=', 'admin@gmail.com', '2022-08-22 07:14:11.892946', '2022-08-22 10:38:21.924036', 1, 1, NULL, 0, 0, 0, 0, 0),
(2, 'pbkdf2_sha256$320000$DCF1Yf5BH4wn15RhpXcr1C$Nv7zQuBsvJgFZlCFXbP+fwIpAFLNrvyYvExZIcHqd3c=', 'javiersofia.as@gmail.com', '2022-08-22 07:17:30.768354', '2022-08-22 08:19:06.335479', 0, 1, NULL, 1, 0, 0, 0, 1),
(3, 'pbkdf2_sha256$320000$hqoMRdUnUyHaGOfgx5EmW4$32MSfpqATwicWrkHtgrW5uK0KPYp1WzM2sSml/hbnY0=', 'pejenriquez@gmail.com', '2022-08-22 07:18:09.396228', '2022-08-22 08:18:43.046526', 0, 1, NULL, 1, 0, 0, 0, 1),
(4, 'pbkdf2_sha256$320000$cwPKEsMl2dzBrHM7bTkgdZ$dI/47No4uvj2irFv5PLWvYD5wuY/YdNhw/dTwAA6ZZ0=', 'antjav14@gmail.com', '2022-08-22 07:19:07.507135', '2022-08-22 08:13:34.069715', 0, 1, NULL, 1, 0, 0, 0, 1),
(5, 'pbkdf2_sha256$320000$kDGQGFDUWoeqdj14jmgAcv$UpFKltfyk/q51JAx7gvBfrOYdVm2n0c4GcwnOHCcUTs=', 'secretary@gmail.com', '2022-08-22 07:19:55.441455', '2022-08-22 10:37:25.820249', 0, 1, NULL, 1, 1, 0, 0, 0),
(6, 'pbkdf2_sha256$320000$909daG3tOtY9KkFAwqi0F7$r5aYEs7gjGv5fcHUUHiGSCeTb6Mfg5RyVBHC4h2e8vE=', 'docdave@gmail.com', '2022-08-22 07:20:24.373620', '2022-08-22 08:11:27.414533', 0, 1, NULL, 1, 0, 1, 0, 0),
(7, 'pbkdf2_sha256$320000$JgLNhb75qSsdkR2SjbMHiv$UQGH0T7VY5bL5v/kgbj1e2ZWzyTf7a6A/fQD0XHd+oA=', 'nathcruz@gmail.com', '2022-08-22 07:21:04.299004', NULL, 0, 1, NULL, 1, 0, 0, 1, 0),
(8, 'pbkdf2_sha256$320000$vkJAv4yCY9zn2cb5EoowLk$KIqnRxwOwR4UTHNOstqp5fdZRlfPxcysnFTznjkppzA=', 'jethver@gmail.com', '2022-08-22 07:21:31.828252', NULL, 0, 1, NULL, 1, 0, 0, 1, 0),
(9, 'pbkdf2_sha256$320000$CM2jk3RayibnORsogNeWvb$k8SPEr8NrTwsyMvT2YVNUWRg4WXi0HJmk8rriMNliVw=', 'alicemedina@gmail.com', '2022-08-22 07:22:07.347211', NULL, 0, 1, NULL, 1, 0, 0, 1, 0),
(10, 'pbkdf2_sha256$320000$gxZCoxlnRzqF22BLrsSyN8$9t+5aTPvTA7tbStqDD+jn2WYccrXdNUyQielOTMY6yE=', 'awllabore@gmail.com', '2022-08-22 10:41:12.016325', NULL, 0, 1, NULL, 1, 0, 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `vet_vaccinehistory`
--

CREATE TABLE `vet_vaccinehistory` (
  `id` bigint(20) NOT NULL,
  `dateofService` date NOT NULL,
  `interpretation` varchar(1000) DEFAULT NULL,
  `dateofReturn` date DEFAULT NULL,
  `reason` varchar(1000) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL,
  `last_modified` datetime(6) DEFAULT NULL,
  `medHistory_id` bigint(20) NOT NULL,
  `service_id` bigint(20) NOT NULL,
  `vaccine_id` bigint(20) NOT NULL,
  `vet_id` bigint(20) DEFAULT NULL,
  `code` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vet_vaccinehistory`
--

INSERT INTO `vet_vaccinehistory` (`id`, `dateofService`, `interpretation`, `dateofReturn`, `reason`, `is_deleted`, `date_of_delete`, `last_modified`, `medHistory_id`, `service_id`, `vaccine_id`, `vet_id`, `code`) VALUES
(1, '2022-08-05', 'no bath', '2023-08-22', '', 0, NULL, '2022-08-22 08:06:47.408780', 2, 5, 6, 2, 'VSc5090'),
(2, '2022-08-05', 'no bath', '2023-08-22', '', 0, NULL, '2022-08-22 08:07:44.549054', 3, 5, 6, 3, 'VS49a2c');

-- --------------------------------------------------------

--
-- Table structure for table `vet_vaxtype`
--

CREATE TABLE `vet_vaxtype` (
  `id` bigint(20) NOT NULL,
  `vaccineType` varchar(50) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `date_of_delete` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_vet_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `vet_breed`
--
ALTER TABLE `vet_breed`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `breed` (`breed`),
  ADD KEY `vet_breed_kind_id_f6da4ed5_fk_vet_petspecies_id` (`kind_id`);

--
-- Indexes for table `vet_chargeslip`
--
ALTER TABLE `vet_chargeslip`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_chargeslip_petowner_id_ba6e58ec_fk_vet_profile_id` (`petowner_id`),
  ADD KEY `vet_chargeslip_staff_id_ac72cec3_fk_vet_staffprofile_id` (`staff_id`);

--
-- Indexes for table `vet_flagsystem`
--
ALTER TABLE `vet_flagsystem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_flagsystem_petOwner_id_744b5564_fk_vet_profile_id` (`petOwner_id`);

--
-- Indexes for table `vet_gender`
--
ALTER TABLE `vet_gender`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `gender` (`gender`);

--
-- Indexes for table `vet_labhistory`
--
ALTER TABLE `vet_labhistory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_labhistory_medHistory_id_37577a0a_fk_vet_medicalhistory_id` (`medHistory_id`),
  ADD KEY `vet_labhistory_service_id_b8515d90_fk_vet_services_id` (`service_id`),
  ADD KEY `vet_labhistory_vet_id_aa2f655b_fk_vet_staffprofile_id` (`vet_id`);

--
-- Indexes for table `vet_medicalhistory`
--
ALTER TABLE `vet_medicalhistory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_medicalhistory_pet_id_8c766384_fk_vet_pets_id` (`pet_id`),
  ADD KEY `vet_medicalhistory_vet_id_145c8179_fk_vet_staffprofile_id` (`vet_id`);

--
-- Indexes for table `vet_pets`
--
ALTER TABLE `vet_pets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_pets_description_id_efa1e5dd_fk_vet_breed_id` (`description_id`),
  ADD KEY `vet_pets_petOwner_id_51b3e0b2_fk_vet_profile_id` (`petOwner_id`),
  ADD KEY `vet_pets_species_id_fef1dca8_fk_vet_petspecies_id` (`species_id`);

--
-- Indexes for table `vet_petspecies`
--
ALTER TABLE `vet_petspecies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `species` (`species`);

--
-- Indexes for table `vet_product`
--
ALTER TABLE `vet_product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_product_product_id_e267bfd3_fk_vet_productinfo_id` (`product_id`);

--
-- Indexes for table `vet_productinfo`
--
ALTER TABLE `vet_productinfo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_productinfo_product_type_id_7bdd26cf_fk_vet_producttype_id` (`product_type_id`);

--
-- Indexes for table `vet_productinvoice`
--
ALTER TABLE `vet_productinvoice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_productinvoice_product_id_94765dae_fk_vet_product_id` (`product_id`),
  ADD KEY `vet_productinvoice_chargeslip_id_d073e4e7_fk_vet_chargeslip_id` (`chargeslip_id`);

--
-- Indexes for table `vet_producttype`
--
ALTER TABLE `vet_producttype`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `prodType` (`prodType`);

--
-- Indexes for table `vet_profile`
--
ALTER TABLE `vet_profile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_profile_gender_id_545bfd5d_fk_vet_gender_id` (`gender_id`),
  ADD KEY `vet_profile_useracc_id_44b0beb6_fk_vet_user_id` (`useracc_id`);

--
-- Indexes for table `vet_schedule_slot`
--
ALTER TABLE `vet_schedule_slot`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_schedule_slot_vet_id_63518e59_fk_vet_staffprofile_id` (`vet_id`);

--
-- Indexes for table `vet_scheduling`
--
ALTER TABLE `vet_scheduling`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_scheduling_pet_id_3a05526c_fk_vet_pets_id` (`pet_id`),
  ADD KEY `vet_scheduling_slot_id_54571fa3_fk_vet_schedule_slot_id` (`slot_id`);

--
-- Indexes for table `vet_servicehistory`
--
ALTER TABLE `vet_servicehistory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_servicehistory_service_id_ecbc8f63_fk_vet_services_id` (`service_id`),
  ADD KEY `vet_servicehistory_medHistory_id_7cba46c6_fk_vet_medic` (`medHistory_id`),
  ADD KEY `vet_servicehistory_vet_id_6d1639ca_fk_vet_staffprofile_id` (`vet_id`);

--
-- Indexes for table `vet_serviceinvoice`
--
ALTER TABLE `vet_serviceinvoice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_serviceinvoice_chargeslip_id_4e4ed6d3_fk_vet_chargeslip_id` (`chargeslip_id`),
  ADD KEY `vet_serviceinvoice_service_id_6d320f2e_fk_vet_services_id` (`service_id`);

--
-- Indexes for table `vet_services`
--
ALTER TABLE `vet_services`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `serviceName` (`serviceName`);

--
-- Indexes for table `vet_staffprofile`
--
ALTER TABLE `vet_staffprofile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vet_staffprofile_gender_id_b40a94bc_fk_vet_gender_id` (`gender_id`),
  ADD KEY `vet_staffprofile_useracc_id_4a04fe8c_fk_vet_user_id` (`useracc_id`);

--
-- Indexes for table `vet_transaction`
--
ALTER TABLE `vet_transaction`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_transaction_chargeslip_id_79ce121c_fk_vet_chargeslip_id` (`chargeslip_id`),
  ADD KEY `vet_transaction_staff_id_b91a3272_fk_vet_staffprofile_id` (`staff_id`);

--
-- Indexes for table `vet_user`
--
ALTER TABLE `vet_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `vet_vaccinehistory`
--
ALTER TABLE `vet_vaccinehistory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `vet_vaccinehistory_medHistory_id_25325ace_fk_vet_medic` (`medHistory_id`),
  ADD KEY `vet_vaccinehistory_service_id_a2ea5201_fk_vet_services_id` (`service_id`),
  ADD KEY `vet_vaccinehistory_vaccine_id_c33916ce_fk_vet_product_id` (`vaccine_id`),
  ADD KEY `vet_vaccinehistory_vet_id_87f4ea7f_fk_vet_staffprofile_id` (`vet_id`);

--
-- Indexes for table `vet_vaxtype`
--
ALTER TABLE `vet_vaxtype`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `vaccineType` (`vaccineType`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `vet_breed`
--
ALTER TABLE `vet_breed`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `vet_chargeslip`
--
ALTER TABLE `vet_chargeslip`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `vet_flagsystem`
--
ALTER TABLE `vet_flagsystem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vet_gender`
--
ALTER TABLE `vet_gender`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `vet_labhistory`
--
ALTER TABLE `vet_labhistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `vet_medicalhistory`
--
ALTER TABLE `vet_medicalhistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `vet_pets`
--
ALTER TABLE `vet_pets`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `vet_petspecies`
--
ALTER TABLE `vet_petspecies`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vet_product`
--
ALTER TABLE `vet_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `vet_productinfo`
--
ALTER TABLE `vet_productinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `vet_productinvoice`
--
ALTER TABLE `vet_productinvoice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `vet_producttype`
--
ALTER TABLE `vet_producttype`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `vet_profile`
--
ALTER TABLE `vet_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `vet_schedule_slot`
--
ALTER TABLE `vet_schedule_slot`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `vet_scheduling`
--
ALTER TABLE `vet_scheduling`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `vet_servicehistory`
--
ALTER TABLE `vet_servicehistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vet_serviceinvoice`
--
ALTER TABLE `vet_serviceinvoice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `vet_services`
--
ALTER TABLE `vet_services`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `vet_staffprofile`
--
ALTER TABLE `vet_staffprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `vet_transaction`
--
ALTER TABLE `vet_transaction`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `vet_user`
--
ALTER TABLE `vet_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `vet_vaccinehistory`
--
ALTER TABLE `vet_vaccinehistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vet_vaxtype`
--
ALTER TABLE `vet_vaxtype`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_vet_user_id` FOREIGN KEY (`user_id`) REFERENCES `vet_user` (`id`);

--
-- Constraints for table `vet_breed`
--
ALTER TABLE `vet_breed`
  ADD CONSTRAINT `vet_breed_kind_id_f6da4ed5_fk_vet_petspecies_id` FOREIGN KEY (`kind_id`) REFERENCES `vet_petspecies` (`id`);

--
-- Constraints for table `vet_chargeslip`
--
ALTER TABLE `vet_chargeslip`
  ADD CONSTRAINT `vet_chargeslip_petowner_id_ba6e58ec_fk_vet_profile_id` FOREIGN KEY (`petowner_id`) REFERENCES `vet_profile` (`id`),
  ADD CONSTRAINT `vet_chargeslip_staff_id_ac72cec3_fk_vet_staffprofile_id` FOREIGN KEY (`staff_id`) REFERENCES `vet_staffprofile` (`id`);

--
-- Constraints for table `vet_flagsystem`
--
ALTER TABLE `vet_flagsystem`
  ADD CONSTRAINT `vet_flagsystem_petOwner_id_744b5564_fk_vet_profile_id` FOREIGN KEY (`petOwner_id`) REFERENCES `vet_profile` (`id`);

--
-- Constraints for table `vet_labhistory`
--
ALTER TABLE `vet_labhistory`
  ADD CONSTRAINT `vet_labhistory_medHistory_id_37577a0a_fk_vet_medicalhistory_id` FOREIGN KEY (`medHistory_id`) REFERENCES `vet_medicalhistory` (`id`),
  ADD CONSTRAINT `vet_labhistory_service_id_b8515d90_fk_vet_services_id` FOREIGN KEY (`service_id`) REFERENCES `vet_services` (`id`),
  ADD CONSTRAINT `vet_labhistory_vet_id_aa2f655b_fk_vet_staffprofile_id` FOREIGN KEY (`vet_id`) REFERENCES `vet_staffprofile` (`id`);

--
-- Constraints for table `vet_medicalhistory`
--
ALTER TABLE `vet_medicalhistory`
  ADD CONSTRAINT `vet_medicalhistory_pet_id_8c766384_fk_vet_pets_id` FOREIGN KEY (`pet_id`) REFERENCES `vet_pets` (`id`),
  ADD CONSTRAINT `vet_medicalhistory_vet_id_145c8179_fk_vet_staffprofile_id` FOREIGN KEY (`vet_id`) REFERENCES `vet_staffprofile` (`id`);

--
-- Constraints for table `vet_pets`
--
ALTER TABLE `vet_pets`
  ADD CONSTRAINT `vet_pets_description_id_efa1e5dd_fk_vet_breed_id` FOREIGN KEY (`description_id`) REFERENCES `vet_breed` (`id`),
  ADD CONSTRAINT `vet_pets_petOwner_id_51b3e0b2_fk_vet_profile_id` FOREIGN KEY (`petOwner_id`) REFERENCES `vet_profile` (`id`),
  ADD CONSTRAINT `vet_pets_species_id_fef1dca8_fk_vet_petspecies_id` FOREIGN KEY (`species_id`) REFERENCES `vet_petspecies` (`id`);

--
-- Constraints for table `vet_product`
--
ALTER TABLE `vet_product`
  ADD CONSTRAINT `vet_product_product_id_e267bfd3_fk_vet_productinfo_id` FOREIGN KEY (`product_id`) REFERENCES `vet_productinfo` (`id`);

--
-- Constraints for table `vet_productinfo`
--
ALTER TABLE `vet_productinfo`
  ADD CONSTRAINT `vet_productinfo_product_type_id_7bdd26cf_fk_vet_producttype_id` FOREIGN KEY (`product_type_id`) REFERENCES `vet_producttype` (`id`);

--
-- Constraints for table `vet_productinvoice`
--
ALTER TABLE `vet_productinvoice`
  ADD CONSTRAINT `vet_productinvoice_chargeslip_id_d073e4e7_fk_vet_chargeslip_id` FOREIGN KEY (`chargeslip_id`) REFERENCES `vet_chargeslip` (`id`),
  ADD CONSTRAINT `vet_productinvoice_product_id_94765dae_fk_vet_product_id` FOREIGN KEY (`product_id`) REFERENCES `vet_product` (`id`);

--
-- Constraints for table `vet_profile`
--
ALTER TABLE `vet_profile`
  ADD CONSTRAINT `vet_profile_gender_id_545bfd5d_fk_vet_gender_id` FOREIGN KEY (`gender_id`) REFERENCES `vet_gender` (`id`),
  ADD CONSTRAINT `vet_profile_useracc_id_44b0beb6_fk_vet_user_id` FOREIGN KEY (`useracc_id`) REFERENCES `vet_user` (`id`);

--
-- Constraints for table `vet_schedule_slot`
--
ALTER TABLE `vet_schedule_slot`
  ADD CONSTRAINT `vet_schedule_slot_vet_id_63518e59_fk_vet_staffprofile_id` FOREIGN KEY (`vet_id`) REFERENCES `vet_staffprofile` (`id`);

--
-- Constraints for table `vet_scheduling`
--
ALTER TABLE `vet_scheduling`
  ADD CONSTRAINT `vet_scheduling_pet_id_3a05526c_fk_vet_pets_id` FOREIGN KEY (`pet_id`) REFERENCES `vet_pets` (`id`),
  ADD CONSTRAINT `vet_scheduling_slot_id_54571fa3_fk_vet_schedule_slot_id` FOREIGN KEY (`slot_id`) REFERENCES `vet_schedule_slot` (`id`);

--
-- Constraints for table `vet_servicehistory`
--
ALTER TABLE `vet_servicehistory`
  ADD CONSTRAINT `vet_servicehistory_medHistory_id_7cba46c6_fk_vet_medic` FOREIGN KEY (`medHistory_id`) REFERENCES `vet_medicalhistory` (`id`),
  ADD CONSTRAINT `vet_servicehistory_service_id_ecbc8f63_fk_vet_services_id` FOREIGN KEY (`service_id`) REFERENCES `vet_services` (`id`),
  ADD CONSTRAINT `vet_servicehistory_vet_id_6d1639ca_fk_vet_staffprofile_id` FOREIGN KEY (`vet_id`) REFERENCES `vet_staffprofile` (`id`);

--
-- Constraints for table `vet_serviceinvoice`
--
ALTER TABLE `vet_serviceinvoice`
  ADD CONSTRAINT `vet_serviceinvoice_chargeslip_id_4e4ed6d3_fk_vet_chargeslip_id` FOREIGN KEY (`chargeslip_id`) REFERENCES `vet_chargeslip` (`id`),
  ADD CONSTRAINT `vet_serviceinvoice_service_id_6d320f2e_fk_vet_services_id` FOREIGN KEY (`service_id`) REFERENCES `vet_services` (`id`);

--
-- Constraints for table `vet_staffprofile`
--
ALTER TABLE `vet_staffprofile`
  ADD CONSTRAINT `vet_staffprofile_gender_id_b40a94bc_fk_vet_gender_id` FOREIGN KEY (`gender_id`) REFERENCES `vet_gender` (`id`),
  ADD CONSTRAINT `vet_staffprofile_useracc_id_4a04fe8c_fk_vet_user_id` FOREIGN KEY (`useracc_id`) REFERENCES `vet_user` (`id`);

--
-- Constraints for table `vet_transaction`
--
ALTER TABLE `vet_transaction`
  ADD CONSTRAINT `vet_transaction_chargeslip_id_79ce121c_fk_vet_chargeslip_id` FOREIGN KEY (`chargeslip_id`) REFERENCES `vet_chargeslip` (`id`),
  ADD CONSTRAINT `vet_transaction_staff_id_b91a3272_fk_vet_staffprofile_id` FOREIGN KEY (`staff_id`) REFERENCES `vet_staffprofile` (`id`);

--
-- Constraints for table `vet_vaccinehistory`
--
ALTER TABLE `vet_vaccinehistory`
  ADD CONSTRAINT `vet_vaccinehistory_medHistory_id_25325ace_fk_vet_medic` FOREIGN KEY (`medHistory_id`) REFERENCES `vet_medicalhistory` (`id`),
  ADD CONSTRAINT `vet_vaccinehistory_service_id_a2ea5201_fk_vet_services_id` FOREIGN KEY (`service_id`) REFERENCES `vet_services` (`id`),
  ADD CONSTRAINT `vet_vaccinehistory_vaccine_id_c33916ce_fk_vet_product_id` FOREIGN KEY (`vaccine_id`) REFERENCES `vet_product` (`id`),
  ADD CONSTRAINT `vet_vaccinehistory_vet_id_87f4ea7f_fk_vet_staffprofile_id` FOREIGN KEY (`vet_id`) REFERENCES `vet_staffprofile` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
