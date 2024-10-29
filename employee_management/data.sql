-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 29, 2024 at 11:25 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `management`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add employee profile', 1, 'add_employeeprofile'),
(2, 'Can change employee profile', 1, 'change_employeeprofile'),
(3, 'Can delete employee profile', 1, 'delete_employeeprofile'),
(4, 'Can view employee profile', 1, 'view_employeeprofile'),
(5, 'Can add ticket', 2, 'add_ticket'),
(6, 'Can change ticket', 2, 'change_ticket'),
(7, 'Can delete ticket', 2, 'delete_ticket'),
(8, 'Can view ticket', 2, 'view_ticket'),
(9, 'Can add log entry', 3, 'add_logentry'),
(10, 'Can change log entry', 3, 'change_logentry'),
(11, 'Can delete log entry', 3, 'delete_logentry'),
(12, 'Can view log entry', 3, 'view_logentry'),
(13, 'Can add permission', 4, 'add_permission'),
(14, 'Can change permission', 4, 'change_permission'),
(15, 'Can delete permission', 4, 'delete_permission'),
(16, 'Can view permission', 4, 'view_permission'),
(17, 'Can add group', 5, 'add_group'),
(18, 'Can change group', 5, 'change_group'),
(19, 'Can delete group', 5, 'delete_group'),
(20, 'Can view group', 5, 'view_group'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add content type', 7, 'add_contenttype'),
(26, 'Can change content type', 7, 'change_contenttype'),
(27, 'Can delete content type', 7, 'delete_contenttype'),
(28, 'Can view content type', 7, 'view_contenttype'),
(29, 'Can add session', 8, 'add_session'),
(30, 'Can change session', 8, 'change_session'),
(31, 'Can delete session', 8, 'delete_session'),
(32, 'Can view session', 8, 'view_session');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(12, 'pbkdf2_sha256$600000$B2QQOVRcndLTvC5i2GDwYj$Ql7Shjmra+2rsNTQPLwnzla28oUxJ109NV7hBVt/EZE=', '2024-10-29 06:04:30.030426', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2024-10-25 09:04:39.482323'),
(13, 'pbkdf2_sha256$600000$f8DmTqWfeOGbTm72fd5pAb$muim+iKMHt4IGxwssxjMUdkVcytUSFNDyQSmqulHenE=', '2024-10-29 08:39:08.370251', 0, 'sanjeev', 'sanjeev', 'kumar', 'sanjeev@gmail.com', 0, 1, '2024-10-25 09:35:53.197315'),
(14, 'pbkdf2_sha256$600000$9lThxBjICjJ4OyVvBVHWts$fAXrWQhLT+V4gf0B+N6/h9PNa9PktSdamBNzaDaazag=', '2024-10-29 09:27:43.066686', 0, 'Ajil', 'Ajil', 'TU', 'ajil@gmail.com', 0, 1, '2024-10-25 09:38:10.503884'),
(15, 'pbkdf2_sha256$600000$pZ3F32yjPfSpXFAsaVaIfX$TX1DaGyKSpLt7CXQ4Zb14FvpPxAPFF78o4Dh+WYQRks=', '2024-10-29 09:27:05.162074', 0, 'Jayamohan', 'Jayamohan', 'x', 'jayamohan@gmail.com', 0, 1, '2024-10-25 10:57:17.559935'),
(16, 'pbkdf2_sha256$600000$RmmQaw7LOqBnvTF00zMvoR$9Zh0gyPknaXFnzcWaYT8a7zZMbx6Kn0xNa3D7XZWvPk=', '2024-10-29 06:37:49.166024', 0, 'Georgy', 'Georgy', 'Cheriyan', 'Georgy@gmail.com', 0, 1, '2024-10-28 06:58:42.078089'),
(17, 'pbkdf2_sha256$600000$pCIXsYCDKtCUWJ9oFE5UVx$QQRyWznGi7iG9nKIWUt8kdoCB2afDa4zgSJOmzyFlN4=', '2024-10-29 09:30:39.647185', 0, 'jobin', 'jobin', 'ps', 'jobin@gmail.com', 0, 1, '2024-10-29 05:46:56.459314'),
(18, 'pbkdf2_sha256$600000$VOGstnPjqJROKoQlMpLUAr$Z/skEG1BQUYK4yxAPvPJwSFvjfXtxsR8hl0V0kvBpfs=', NULL, 0, 'didith', 'didith', 'antony', 'didith@gmail.com', 0, 1, '2024-10-29 05:48:06.536978'),
(23, 'pbkdf2_sha256$600000$t7ObAVGZGE0Z4dvZjdmCgf$e5WqOrVXtk78D2N65gpUGcjo2IUgWK2KKaXrrReYB3I=', NULL, 0, 'manuel', 'manuel', 'sijo', 'manuel@gmail.com', 0, 1, '2024-10-29 06:05:37.039900');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(11, '2024-10-29 05:52:11.489505', '19', 'manuel', 3, '', 6, 12),
(12, '2024-10-29 05:55:05.801795', '20', 'manuel', 3, '', 6, 12),
(13, '2024-10-29 06:04:45.583087', '22', 'aa', 3, '', 6, 12),
(14, '2024-10-29 06:04:45.583087', '21', 'manuel', 3, '', 6, 12);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(3, 'admin', 'logentry'),
(5, 'auth', 'group'),
(4, 'auth', 'permission'),
(6, 'auth', 'user'),
(7, 'contenttypes', 'contenttype'),
(1, 'employee', 'employeeprofile'),
(2, 'employee', 'ticket'),
(8, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-10-01 11:04:14.909236'),
(2, 'auth', '0001_initial', '2024-10-01 11:04:15.780359'),
(3, 'admin', '0001_initial', '2024-10-01 11:04:16.043379'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-10-01 11:04:16.065528'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-10-01 11:04:16.081155'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-10-01 11:04:16.197037'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-10-01 11:04:16.328550'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-10-01 11:04:16.350685'),
(9, 'auth', '0004_alter_user_username_opts', '2024-10-01 11:04:16.381944'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-10-01 11:04:16.533653'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-10-01 11:04:16.533653'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-10-01 11:04:16.563956'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-10-01 11:04:16.614556'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-10-01 11:04:16.675164'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-10-01 11:04:16.715609'),
(16, 'auth', '0011_update_proxy_permissions', '2024-10-01 11:04:16.774259'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-10-01 11:04:16.976797'),
(18, 'employee', '0001_initial', '2024-10-01 11:04:17.128396'),
(19, 'employee', '0002_alter_employeeprofile_skill', '2024-10-01 11:04:17.144023'),
(20, 'employee', '0003_alter_employeeprofile_level', '2024-10-01 11:04:17.309828'),
(21, 'employee', '0004_alter_employeeprofile_level', '2024-10-01 11:04:17.350185'),
(22, 'employee', '0005_alter_employeeprofile_skill', '2024-10-01 11:04:17.398641'),
(23, 'employee', '0006_alter_employeeprofile_level', '2024-10-01 11:04:17.429179'),
(24, 'employee', '0007_ticket', '2024-10-01 11:04:17.681960'),
(25, 'employee', '0008_alter_ticket_group', '2024-10-01 11:04:17.704179'),
(26, 'sessions', '0001_initial', '2024-10-01 11:04:17.825125'),
(27, 'employee', '0009_employeeprofile_status', '2024-10-03 05:12:28.241259'),
(28, 'employee', '0010_employeeprofile_login_time_and_more', '2024-10-03 05:26:31.263988'),
(29, 'employee', '0011_employeeprofile_total_time', '2024-10-03 05:28:39.739243'),
(30, 'employee', '0012_employeeprofile_is_active', '2024-10-03 06:11:09.937970'),
(31, 'employee', '0013_employeeprofile_is_on_break', '2024-10-03 07:13:46.124618'),
(32, 'employee', '0014_employeeprofile_promoted_to_admin', '2024-10-21 09:47:05.683950');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0ekgik4knjthy1dfl8xw22j9ri4mi9li', 'e30:1t381I:3_4GN_Ua7-sokfQfmFtwtCBArfp8q_DGWQ6bOHA_T5A', '2024-11-05 06:05:28.763483'),
('0ovr1jvd3je0f2kclpix31kp3nly52e9', 'e30:1t2nSV:IXukymgVm5cbExNRdHeGpwPJMvT_EK9Rp7n4Ouwk6uo', '2024-11-04 08:08:11.462121'),
('abbmixseln47o8qc91e9oagcliuydt1z', 'e30:1t2pwa:FarzfkC6p4YqXbiUQr1aMMdFdoNQUT7O8azCsTfnTDk', '2024-11-04 10:47:24.590209'),
('l3p97cg39qycsuu4bd1qs77uvw6acsvo', 'e30:1t4EEt:nddDYHalbSJhztSVzuUSHs2kJP7OaCuNGjk4SUFElEc', '2024-11-08 06:56:03.126802'),
('nsqhgyjpo1xp5bbt2eqs53gwzr55u2im', 'e30:1t2mRj:IlfHbnnB0QiLACUhmWaOL1tnreL4pdLGqcMEc0v_0bY', '2024-11-04 07:03:19.757767'),
('p86zxp2if7cqm1eixtoplwi4auvt4xjc', 'e30:1t2puy:w363FdJ44WG_ue7HvcbsN0Y7UCCQryCGWx8oafn48Kg', '2024-11-04 10:45:44.887258'),
('tbxjvxr4pesu4qtk6v8gs4ccoy3qcrwy', 'e30:1t2nbJ:wo6yYZJiS1icSZwaJZzmTl1iYT3f8c7mypuG-1jYdiE', '2024-11-04 08:17:17.946809'),
('w9mkuftk9etc1niuw7i7ogadg6bdmahg', 'e30:1t2nYI:O9YT5WCXh10gT2Mde5nStD2G9LzQHULaBfRtY3y9UaU', '2024-11-04 08:14:10.255715'),
('xxrfvx3z1wn6378j19n7hm9ehunwn92a', 'e30:1t2puW:joT8UyslB0c-szbcaZV4QkKkavtKv1_e3ND1HtQua-k', '2024-11-04 10:45:16.670213'),
('zwmebvbq4rcotojmzj2dxj7x148mpjhf', 'e30:1t4G5s:5c_cz2lp1wKGsilFpcOm1lDGydDc73HeStmWOGf8sYo', '2024-11-08 08:54:52.955239');

-- --------------------------------------------------------

--
-- Table structure for table `employee_employeeprofile`
--

CREATE TABLE `employee_employeeprofile` (
  `id` bigint(20) NOT NULL,
  `level` varchar(10) NOT NULL,
  `skill` varchar(20) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `login_time` datetime(6) DEFAULT NULL,
  `logout_time` datetime(6) DEFAULT NULL,
  `total_time` bigint(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_on_break` tinyint(1) NOT NULL,
  `promoted_to_admin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_employeeprofile`
--

INSERT INTO `employee_employeeprofile` (`id`, `level`, `skill`, `is_admin`, `user_id`, `status`, `login_time`, `logout_time`, `total_time`, `is_active`, `is_on_break`, `promoted_to_admin`) VALUES
(9, '', '', 0, 12, 'offline', NULL, NULL, 0, 0, 0, 0),
(10, '', '', 1, 13, 'offline', NULL, NULL, 0, 0, 0, 0),
(11, '1', 'Windows', 0, 14, 'offline', NULL, NULL, 0, 0, 0, 0),
(12, '1', 'Windows', 0, 15, 'offline', NULL, NULL, 0, 0, 0, 0),
(13, '1', 'Linux', 1, 16, 'offline', NULL, NULL, 0, 0, 0, 0),
(14, '1', 'Windows', 0, 17, 'offline', NULL, NULL, 0, 0, 0, 0),
(15, '1', 'Linux', 0, 18, 'offline', NULL, NULL, 0, 0, 0, 0),
(16, '1', 'Linux', 1, 23, 'offline', NULL, NULL, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `employee_ticket`
--

CREATE TABLE `employee_ticket` (
  `id` bigint(20) NOT NULL,
  `subject` varchar(300) NOT NULL,
  `status` varchar(50) NOT NULL,
  `group` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_ticket`
--

INSERT INTO `employee_ticket` (`id`, `subject`, `status`, `group`, `created_at`, `created_by_id`) VALUES
(8, 'dxuagdygayi', 'resolved', 'Windows', '2024-10-25 10:18:25.800686', 14),
(9, 'gsyugcys', 'pending', 'Windows', '2024-10-25 10:19:07.172916', 14),
(10, 'djbadyigdgsiucuhsucb hcbsygych', 'initial_response', 'Windows', '2024-10-25 10:57:52.462685', 15),
(11, 'dgdauuhu', 'closed', 'Windows', '2024-10-25 10:58:05.930800', 15),
(12, 'kbgijnijvbd jdnvudnv', 'waiting_on_customer', 'Windows', '2024-10-25 10:59:24.717282', 14),
(13, 'uwduud', 'resolved', 'Windows', '2024-10-28 09:30:08.665452', 14),
(14, 'bdyb chsvcbsucy', 'waiting_on_customer', 'Windows', '2024-10-29 08:38:12.281910', 17),
(15, 'okfoofjijkfi', 'pending', 'Windows', '2024-10-29 08:38:28.027810', 17);

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
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

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
-- Indexes for table `employee_employeeprofile`
--
ALTER TABLE `employee_employeeprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `employee_ticket`
--
ALTER TABLE `employee_ticket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_ticket_created_by_id_ffc4d110_fk_auth_user_id` (`created_by_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `employee_employeeprofile`
--
ALTER TABLE `employee_employeeprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `employee_ticket`
--
ALTER TABLE `employee_ticket`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

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
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `employee_employeeprofile`
--
ALTER TABLE `employee_employeeprofile`
  ADD CONSTRAINT `employee_employeeprofile_user_id_d5e61f5c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `employee_ticket`
--
ALTER TABLE `employee_ticket`
  ADD CONSTRAINT `employee_ticket_created_by_id_ffc4d110_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
