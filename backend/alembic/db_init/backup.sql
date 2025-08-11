mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 8.4.6, for Linux (x86_64)
--
-- Host: localhost    Database: llearn
-- ------------------------------------------------------
-- Server version	8.4.6

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('75c172de024e');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookmarks`
--

DROP TABLE IF EXISTS `bookmarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookmarks` (
  `id` varchar(26) NOT NULL,
  `curriculum_id` varchar(26) NOT NULL,
  `user_id` varchar(26) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_curriculum_bookmark` (`curriculum_id`,`user_id`),
  KEY `idx_bookmark_created_at` (`created_at`),
  KEY `idx_bookmark_curriculum` (`curriculum_id`),
  KEY `idx_bookmark_user` (`user_id`),
  CONSTRAINT `bookmarks_ibfk_1` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculums` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bookmarks_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookmarks`
--

LOCK TABLES `bookmarks` WRITE;
/*!40000 ALTER TABLE `bookmarks` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookmarks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` varchar(26) NOT NULL,
  `name` varchar(30) NOT NULL,
  `description` text,
  `color` varchar(7) NOT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `sort_order` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `idx_category_active_sort` (`is_active`,`sort_order`),
  KEY `idx_category_created_at` (`created_at`),
  KEY `idx_category_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` varchar(26) NOT NULL,
  `curriculum_id` varchar(26) NOT NULL,
  `user_id` varchar(26) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_comment_created_at` (`created_at`),
  KEY `idx_comment_curriculum` (`curriculum_id`),
  KEY `idx_comment_updated_at` (`updated_at`),
  KEY `idx_comment_user` (`user_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculums` (`id`) ON DELETE CASCADE,
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curriculum_categories`
--

DROP TABLE IF EXISTS `curriculum_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curriculum_categories` (
  `id` varchar(53) NOT NULL,
  `curriculum_id` varchar(26) NOT NULL,
  `category_id` varchar(26) NOT NULL,
  `assigned_by` varchar(26) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_curriculum_category` (`curriculum_id`),
  KEY `idx_curriculum_category_assigned_by` (`assigned_by`),
  KEY `idx_curriculum_category_category` (`category_id`),
  KEY `idx_curriculum_category_created_at` (`created_at`),
  KEY `idx_curriculum_category_curriculum` (`curriculum_id`),
  CONSTRAINT `curriculum_categories_ibfk_1` FOREIGN KEY (`assigned_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `curriculum_categories_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE,
  CONSTRAINT `curriculum_categories_ibfk_3` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculums` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curriculum_categories`
--

LOCK TABLES `curriculum_categories` WRITE;
/*!40000 ALTER TABLE `curriculum_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `curriculum_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curriculum_tags`
--

DROP TABLE IF EXISTS `curriculum_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curriculum_tags` (
  `id` varchar(53) NOT NULL,
  `curriculum_id` varchar(26) NOT NULL,
  `tag_id` varchar(26) NOT NULL,
  `added_by` varchar(26) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_curriculum_tag` (`curriculum_id`,`tag_id`),
  KEY `idx_curriculum_tag_added_by` (`added_by`),
  KEY `idx_curriculum_tag_created_at` (`created_at`),
  KEY `idx_curriculum_tag_curriculum` (`curriculum_id`),
  KEY `idx_curriculum_tag_tag` (`tag_id`),
  CONSTRAINT `curriculum_tags_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `curriculum_tags_ibfk_2` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculums` (`id`) ON DELETE CASCADE,
  CONSTRAINT `curriculum_tags_ibfk_3` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curriculum_tags`
--

LOCK TABLES `curriculum_tags` WRITE;
/*!40000 ALTER TABLE `curriculum_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `curriculum_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curriculums`
--

DROP TABLE IF EXISTS `curriculums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curriculums` (
  `id` varchar(26) NOT NULL,
  `user_id` varchar(26) NOT NULL,
  `title` varchar(50) NOT NULL,
  `visibility` varchar(10) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `curriculums_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curriculums`
--

LOCK TABLES `curriculums` WRITE;
/*!40000 ALTER TABLE `curriculums` DISABLE KEYS */;
INSERT INTO `curriculums` VALUES ('01K2CFH3HKDF0FZDKNNYXF7Z8W','01K2CFEH2V9ED5SW9D0WFE5TS7','2508111151 3개월 안에 Python 웹 개발 기본 마스터','PRIVATE','2025-08-11 11:51:23','2025-08-11 11:51:23'),('01K2CFKB6CFP5T994YC5KKGP99','01K2CFEHB2A81K2T3QABRPGKAM','2508111152 3개월 안에 React 웹 개발 기본 마스터','PRIVATE','2025-08-11 11:52:36','2025-08-11 11:52:36'),('01K2CFKRMTKHXP7C66MCQ1J9M3','01K2CFEH2V9ED5SW9D0WFE5TS7','2508111152 데이터 분석 기본 익히기','PRIVATE','2025-08-11 11:52:50','2025-08-11 11:52:50'),('01K2CFKYMF0TWRV3Q206136Y0E','01K2CFEH2V9ED5SW9D0WFE5TS7','2508111152 4개월 안에 프론트엔드 React 기초 완성','PRIVATE','2025-08-11 11:52:56','2025-08-11 11:52:56'),('01K2CFM2DVSXE2TNH99ZXR88FS','01K2CFEH2V9ED5SW9D0WFE5TS7','2508111153 Git과 협업 툴 숙련 커리큘럼','PRIVATE','2025-08-11 11:53:00','2025-08-11 11:53:00'),('01K2CFM8E5RMZJWTKWGDC3GSP6','01K2CFEH2V9ED5SW9D0WFE5TS7','2508111153 5개월 안에 머신러닝 기본 모델 구현','PRIVATE','2025-08-11 11:53:06','2025-08-11 11:53:06'),('01K2CFMHADC8BQSAFWNAZF55Q7','01K2CFEHB2A81K2T3QABRPGKAM','2508111153 Node.js와 Express 기본 익히기','PRIVATE','2025-08-11 11:53:15','2025-08-11 11:53:15'),('01K2CFMNJRGQXD8Z73EARATKMK','01K2CFEHB2A81K2T3QABRPGKAM','2508111153 데이터 시각화 프로젝트 커리큘럼','PRIVATE','2025-08-11 11:53:20','2025-08-11 11:53:20');
/*!40000 ALTER TABLE `curriculums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbacks`
--

DROP TABLE IF EXISTS `feedbacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedbacks` (
  `id` varchar(26) NOT NULL,
  `summary_id` varchar(26) NOT NULL,
  `comment` text NOT NULL,
  `score` float NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `summary_id` (`summary_id`),
  CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`summary_id`) REFERENCES `summaries` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbacks`
--

LOCK TABLES `feedbacks` WRITE;
/*!40000 ALTER TABLE `feedbacks` DISABLE KEYS */;
INSERT INTO `feedbacks` VALUES ('01K2CFRXAW04VEVJZXX6PE08WD','01K2CFRDK5CRT6B7RF0S5XV26S','머신러닝의 정의와 주요 학습 방식에 대한 이해가 잘 드러나 있습니다. 그러나 각 학습 방식의 예시나 실제 응용 사례를 추가하면 더욱 풍부한 내용이 될 것입니다. 또한, 머신러닝의 기술적 세부사항이나 최근 동향에 대한 언급이 있으면 좋겠습니다.',8.5,'2025-08-11 11:55:39','2025-08-11 11:55:39'),('01K2CFST8C8FN2P105K6SC9HKK','01K2CFSHH1TPV5S74K5BY7AN5K','Git의 설치와 설정, 기본 명령어 사용법을 잘 이해하고 실습한 점이 인상적입니다. 추가적으로, 각 명령어의 사용 사례나 상황을 더 구체적으로 설명하면 이해도가 더욱 높아질 것입니다. 협업 시 발생할 수 있는 문제와 그 해결 방법에 대한 학습도 고려해보세요.',8.5,'2025-08-11 11:56:08','2025-08-11 11:56:08');
/*!40000 ALTER TABLE `feedbacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `follows` (
  `id` varchar(26) NOT NULL,
  `follower_id` varchar(26) NOT NULL,
  `followee_id` varchar(26) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_follow_relation` (`follower_id`,`followee_id`),
  KEY `idx_follow_created_at` (`created_at`),
  KEY `idx_follow_followee` (`followee_id`),
  KEY `idx_follow_followee_created` (`followee_id`,`created_at`),
  KEY `idx_follow_follower` (`follower_id`),
  KEY `idx_follow_follower_created` (`follower_id`,`created_at`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`followee_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `id` varchar(26) NOT NULL,
  `curriculum_id` varchar(26) NOT NULL,
  `user_id` varchar(26) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_curriculum_like` (`curriculum_id`,`user_id`),
  KEY `idx_like_created_at` (`created_at`),
  KEY `idx_like_curriculum` (`curriculum_id`),
  KEY `idx_like_user` (`user_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculums` (`id`) ON DELETE CASCADE,
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `summaries`
--

DROP TABLE IF EXISTS `summaries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `summaries` (
  `id` varchar(26) NOT NULL,
  `curriculum_id` varchar(26) NOT NULL,
  `week_number` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `owner_id` varchar(26) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `curriculum_id` (`curriculum_id`),
  CONSTRAINT `summaries_ibfk_1` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculums` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `summaries`
--

LOCK TABLES `summaries` WRITE;
/*!40000 ALTER TABLE `summaries` DISABLE KEYS */;
INSERT INTO `summaries` VALUES ('01K2CFRDK5CRT6B7RF0S5XV26S','01K2CFM8E5RMZJWTKWGDC3GSP6',1,'머신러닝의 정의와 핵심 개념을 이해하고, 주요 학습 방식(지도, 비지도, 강화 학습)의 특징과 차이를 학습한다. 다양한 산업 분야에서의 응용 사례를 살펴보며 기술의 활용 범위를 파악하고, 전체 커리큘럼에서 머신러닝이 차지하는 위치와 역할을 조망한다.','2025-08-11 11:55:23','2025-08-11 11:55:23','01K2CFEH2V9ED5SW9D0WFE5TS7'),('01K2CFSHH1TPV5S74K5BY7AN5K','01K2CFM2DVSXE2TNH99ZXR88FS',1,'Git의 설치와 환경설정을 진행하고, 버전 관리의 개념과 필요성을 학습한다. 로컬 저장소 생성과 커밋 과정을 실습하며, 주요 명령어를 익혀 코드 변경 사항을 체계적으로 기록·관리하는 방법을 배운다. 협업 전 필수적으로 이해해야 할 기초 단계이다.','2025-08-11 11:55:59','2025-08-11 11:55:59','01K2CFEH2V9ED5SW9D0WFE5TS7');
/*!40000 ALTER TABLE `summaries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `id` varchar(26) NOT NULL,
  `name` varchar(20) NOT NULL,
  `usage_count` int NOT NULL,
  `created_by` varchar(26) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `idx_tag_created_at` (`created_at`),
  KEY `idx_tag_created_by` (`created_by`),
  KEY `idx_tag_name` (`name`),
  KEY `idx_tag_usage_count` (`usage_count`),
  CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES ('01K2CFWY8B3WZY94MZAB1GPVKA','프레임워크',0,'01K2CFEH2V9ED5SW9D0WFE5TS7','2025-08-11 11:57:51','2025-08-11 11:57:51'),('01K2CFX4FCBQAXPMQ1AXP2HP4T','프로그래밍',0,'01K2CFEH2V9ED5SW9D0WFE5TS7','2025-08-11 11:57:57','2025-08-11 11:57:57'),('01K2CFX8GW2N9TKTTTW65SKCVY','웹',0,'01K2CFEH2V9ED5SW9D0WFE5TS7','2025-08-11 11:58:01','2025-08-11 11:58:01');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(26) NOT NULL,
  `email` varchar(64) NOT NULL,
  `name` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `role` enum('USER','ADMIN') NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('01K2CDVXKFD8TXDJ8G5VP96VC3','admin@admin.com','admin','$2b$12$5nwPMsEaPdCVF5Nf.hNKmeyEJfvtYphx4ptE739jrYaQQeP1UDMdO','ADMIN','2025-08-11 11:22:20','2025-08-11 11:22:20'),('01K2CFEH2V9ED5SW9D0WFE5TS7','user1@user.com','user1','$2b$12$lU0dZ7Y4xSj3Ok0AejTmweWvE3vvUdon9zjiQ2JqHhkFeePruKQUS','USER','2025-08-11 11:49:58','2025-08-11 11:49:58'),('01K2CFEHB2A81K2T3QABRPGKAM','user2@user.com','user2','$2b$12$E/eO/ixslp6Uf6aqNjZ4muSupgM8admVzCNQI0McM2yJcNM8T0Apy','USER','2025-08-11 11:49:59','2025-08-11 11:49:59'),('01K2CFEHKJ9JAGGK5SDT2MG00R','user3@user.com','user3','$2b$12$vCW48kyfdOHYON/9NL73NefR8u6v2rdDzPNVy3AQ1veDeqUn.LTG.','USER','2025-08-11 11:49:59','2025-08-11 11:49:59'),('01K2CFEHVV1BFN5QNQX4EJR7R3','user4@user.com','user4','$2b$12$rMOKhL3DMjYEEP4BxLW0eeZ/yePXUPlh0VGgnLSxffAu6Cmn9G7A2','USER','2025-08-11 11:49:59','2025-08-11 11:49:59'),('01K2CFEJ41T8X6T72M1XD07NZ6','user5@user.com','user5','$2b$12$rD6MeJ16IaPN4EOUJraMEuUWaYwMyA8eomdIEonUqmmm5322KQDku','USER','2025-08-11 11:49:59','2025-08-11 11:49:59'),('01K2CFEJCBJNAKWR19MCZ2T17C','user6@user.com','user6','$2b$12$hWIUqIzrrn9GlwTE1H4AReZOWbLoqOSqELG180Ig/xeCvTctwJzLu','USER','2025-08-11 11:50:00','2025-08-11 11:50:00'),('01K2CFEJMJVS40GD0TZPA3CQM2','user7@user.com','user7','$2b$12$7mC6gYLgQfGF4PmbUDKx9eGBE1QBT4SuTSamnbkqV251aXcVS8Y6O','USER','2025-08-11 11:50:00','2025-08-11 11:50:00'),('01K2CFEJWRWKA24VVY8X7MR2XV','user8@user.com','user8','$2b$12$/NAosF3LjE9Ma0v8CMcW5eu7pgjN2lLMOcm9lTrao3HPIBS8UcqFu','USER','2025-08-11 11:50:00','2025-08-11 11:50:00'),('01K2CFEK5HVQYSPK2D0KE5PQXJ','user9@user.com','user9','$2b$12$WTYnZRJq9B0WEJvBuY8qPerWyXWRrtyDwttUaqxk2RsbfXmqdngG.','USER','2025-08-11 11:50:00','2025-08-11 11:50:00'),('01K2CFEKDWDQE90VJZDEDDE9KF','user10@user.com','user10','$2b$12$sYVnASVhxuXCbjzba2hENuJzHMGUEFy8j5Kkji2cgTP3vWBj3wUvq','USER','2025-08-11 11:50:01','2025-08-11 11:50:01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `week_schedules`
--

DROP TABLE IF EXISTS `week_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `week_schedules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `curriculum_id` varchar(26) NOT NULL,
  `week_number` int NOT NULL,
  `lessons` json NOT NULL,
  `title` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `curriculum_id` (`curriculum_id`),
  CONSTRAINT `week_schedules_ibfk_1` FOREIGN KEY (`curriculum_id`) REFERENCES `curriculums` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `week_schedules`
--

LOCK TABLES `week_schedules` WRITE;
/*!40000 ALTER TABLE `week_schedules` DISABLE KEYS */;
INSERT INTO `week_schedules` VALUES (1,'01K2CFH3HKDF0FZDKNNYXF7Z8W',1,'[\"Python 설치 및 기본 문법\", \"FastAPI 소개 및 설치\", \"MySQL 설치 및 기본 쿼리\"]','개발환경 세팅'),(2,'01K2CFH3HKDF0FZDKNNYXF7Z8W',2,'[\"FastAPI로 기본 CRUD API 만들기\", \"MySQL과 FastAPI 연동하기\", \"API 테스트 및 디버깅\"]','CRUD API 구현'),(3,'01K2CFH3HKDF0FZDKNNYXF7Z8W',3,'[\"Docker 기본 개념 이해\", \"FastAPI 애플리케이션 Dockerize하기\", \"Docker Compose를 이용한 배포\"]','Docker로 배포'),(4,'01K2CFKB6CFP5T994YC5KKGP99',1,'[\"Node.js 및 npm 설치\", \"React 프로젝트 생성\", \"FastAPI 설치 및 기본 설정\"]','개발환경 세팅'),(5,'01K2CFKB6CFP5T994YC5KKGP99',2,'[\"React 컴포넌트 구조\", \"JSX 문법 이해\", \"상태 관리 및 props 사용법\"]','React 기본 개념 이해'),(6,'01K2CFKB6CFP5T994YC5KKGP99',3,'[\"FastAPI로 REST API 구축\", \"React에서 API 호출하기\", \"데이터 표시 및 상태 업데이트\"]','FastAPI와의 연동'),(7,'01K2CFKRMTKHXP7C66MCQ1J9M3',1,'[\"데이터 분석의 정의\", \"데이터 분석의 중요성\", \"데이터 분석 프로세스 소개\"]','데이터 분석 개요'),(8,'01K2CFKRMTKHXP7C66MCQ1J9M3',2,'[\"Python 설치하기\", \"Pandas 라이브러리 설치\", \"Jupyter Notebook 사용법\"]','Python과 Pandas 설치'),(9,'01K2CFKRMTKHXP7C66MCQ1J9M3',3,'[\"데이터 불러오기\", \"결측치 처리하기\", \"데이터 타입 변환\"]','데이터 전처리 기초'),(10,'01K2CFKRMTKHXP7C66MCQ1J9M3',4,'[\"기초 통계량 계산\", \"데이터 필터링 및 정렬\", \"그룹화와 집계\"]','데이터 탐색 및 분석'),(11,'01K2CFKRMTKHXP7C66MCQ1J9M3',5,'[\"Matplotlib 설치 및 기본 사용법\", \"선 그래프 그리기\", \"막대 그래프와 히스토그램\"]','데이터 시각화 기초'),(12,'01K2CFKRMTKHXP7C66MCQ1J9M3',6,'[\"실제 데이터셋 선택\", \"데이터 전처리 및 분석\", \"결과 시각화 및 발표\"]','프로젝트: 데이터 분석 실습'),(13,'01K2CFKYMF0TWRV3Q206136Y0E',1,'[\"React 소개\", \"컴포넌트와 Props\", \"상태 관리의 기초\"]','React 기초 이해'),(14,'01K2CFKYMF0TWRV3Q206136Y0E',2,'[\"useState 훅 사용법\", \"useEffect 훅 사용법\", \"커스텀 훅 만들기\"]','React Hook 활용하기'),(15,'01K2CFKYMF0TWRV3Q206136Y0E',3,'[\"React Router 소개\", \"라우팅 설정하기\", \"동적 라우팅 구현하기\"]','React Router로 페이지 관리'),(16,'01K2CFKYMF0TWRV3Q206136Y0E',4,'[\"Axios 설치 및 기본 사용법\", \"API 호출하기\", \"데이터 처리 및 에러 핸들링\"]','Axios를 이용한 데이터 통신'),(17,'01K2CFM2DVSXE2TNH99ZXR88FS',1,'[\"Git 설치 및 설정\", \"기본 명령어 사용법\", \"버전 관리 개념 이해\", \"로컬 저장소 생성 및 커밋\"]','Git 기본 개념 이해'),(18,'01K2CFM2DVSXE2TNH99ZXR88FS',2,'[\"GitHub를 통한 원격 저장소 관리\", \"Jira를 이용한 프로젝트 관리\", \"Slack을 통한 팀 커뮤니케이션\", \"GitHub와 Jira 통합하기\"]','협업 툴 활용 실습'),(19,'01K2CFM8E5RMZJWTKWGDC3GSP6',1,'[\"머신러닝의 정의\", \"머신러닝의 종류\", \"머신러닝의 응용 분야\"]','머신러닝 개요 이해'),(20,'01K2CFM8E5RMZJWTKWGDC3GSP6',2,'[\"Scikit-learn 설치하기\", \"기본 API 이해하기\", \"데이터셋 로딩 및 탐색\"]','Scikit-learn 설치 및 기본 사용법'),(21,'01K2CFM8E5RMZJWTKWGDC3GSP6',3,'[\"선형 회귀 모델 이해\", \"Scikit-learn을 이용한 선형 회귀 구현\", \"모델 성능 평가 방법\"]','회귀 모델 구현'),(22,'01K2CFM8E5RMZJWTKWGDC3GSP6',4,'[\"로지스틱 회귀 모델 이해\", \"Scikit-learn을 이용한 로지스틱 회귀 구현\", \"혼동 행렬 및 정확도 평가\"]','분류 모델 구현'),(23,'01K2CFM8E5RMZJWTKWGDC3GSP6',5,'[\"하이퍼파라미터 튜닝\", \"교차 검증 이해\", \"최종 모델 성능 평가 및 결과 분석\"]','모델 성능 최적화 및 평가'),(24,'01K2CFMHADC8BQSAFWNAZF55Q7',1,'[\"Node.js 설치\", \"Express 프레임워크 소개\", \"첫 번째 Express 앱 만들기\"]','개발환경 세팅'),(25,'01K2CFMHADC8BQSAFWNAZF55Q7',2,'[\"REST API 개념 이해\", \"라우팅 설정하기\", \"CRUD 기능 구현하기\", \"미들웨어 활용하기\"]','REST API 구축'),(26,'01K2CFMNJRGQXD8Z73EARATKMK',1,'[\"프로젝트 목표 설정\", \"데이터 수집 방법론\", \"요구사항 정의서 작성\"]','프로젝트 개요 및 요구사항 분석'),(27,'01K2CFMNJRGQXD8Z73EARATKMK',2,'[\"D3.js 소개\", \"개발 환경 세팅\", \"첫 번째 D3.js 차트 만들기\"]','D3.js 기초 및 환경 설정'),(28,'01K2CFMNJRGQXD8Z73EARATKMK',3,'[\"Chart.js 소개\", \"Chart.js 설치 및 설정\", \"차트 유형별 사용법\"]','Chart.js를 이용한 데이터 시각화'),(29,'01K2CFMNJRGQXD8Z73EARATKMK',4,'[\"D3.js와 Chart.js 통합\", \"사용자 인터랙션 추가\", \"프로젝트 최종 점검 및 발표 준비\"]','인터랙티브 데이터 시각화 구현');
/*!40000 ALTER TABLE `week_schedules` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-11 12:01:24
