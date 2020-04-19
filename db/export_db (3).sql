CREATE DATABASE  IF NOT EXISTS `shool_db` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `shool_db`;
-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: shool_db
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `firms`
--

DROP TABLE IF EXISTS `firms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `firms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cari_code` varchar(20) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `adress` varchar(200) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `fax` varchar(20) DEFAULT NULL,
  `web` varchar(200) DEFAULT NULL,
  `sector_code` varchar(20) DEFAULT NULL,
  `sector_desc` varchar(45) DEFAULT NULL,
  `hr_name` varchar(20) DEFAULT NULL,
  `hr_telephone` varchar(20) DEFAULT NULL,
  `hr_email` varchar(45) DEFAULT NULL,
  `notes` varchar(300) DEFAULT NULL,
  `record_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `cari_code_UNIQUE` (`cari_code`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firms`
--

LOCK TABLES `firms` WRITE;
/*!40000 ALTER TABLE `firms` DISABLE KEYS */;
INSERT INTO `firms` VALUES (1,'11','delta',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Note 1','2020-04-12 14:19:38'),(2,'12','cms','45424',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Note 2','2020-04-12 14:19:38'),(3,'13','bakioglu','40475',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Note 3','2020-04-12 14:19:38'),(4,'14','Norm civata','100447','izmir','çiğli','0232115556','','','1515','tekstil','','','','Note 4','2020-04-12 14:19:38'),(5,'15','kms 2555','2002','izmir','çiğli','0232','','','123214','','','','','Note 6','2020-04-12 14:22:44'),(6,'16','kms 2 ','2002','','','0232','','','','','','','','Note 6','2020-04-12 14:19:38'),(7,'17','ipek','10038','izmir','çiğli','32424','234242','www.ipek.com','34525','tekstil','serkan','052122120','serkan@serkan','asdfasfasfsafa','2020-04-12 14:19:38'),(8,'18','barem','10038','izmir','çiğli','32424','234242','wrwrqeqwr','34525','wretwet','mehmet','052122120','serkan@serkan','asdfasfasfsafa','2020-04-12 14:19:38'),(11,'19','kms 5','10335','İzmir','çiğli','2320000','','','1515','','','','','Note 5','2020-04-12 14:21:44'),(12,'20','Pilipis','10037','izmir','çiğli','232552254','232552254','www.pilipis','5542','tekstil','','','','','2020-04-12 14:26:58');
/*!40000 ALTER TABLE `firms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `internship`
--

DROP TABLE IF EXISTS `internship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internship` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(45) DEFAULT NULL,
  `quota_id` varchar(45) DEFAULT NULL,
  `start_date` varchar(45) DEFAULT NULL,
  `finish_date` varchar(45) DEFAULT NULL,
  `internship_day` varchar(45) DEFAULT NULL,
  `notes` varchar(300) DEFAULT NULL,
  `username_id` varchar(45) DEFAULT NULL,
  `record_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internship`
--

LOCK TABLES `internship` WRITE;
/*!40000 ALTER TABLE `internship` DISABLE KEYS */;
INSERT INTO `internship` VALUES (3,'9','5','2012','12','5','basarılı bir staj oalcak','ed','2020-04-13 09:26:03'),(5,'6','2','2015','24.1.2018','2','','ed','2020-04-12 16:57:38'),(6,'8','5','15.7.2020','14.1.2020','5','','ed','2020-04-13 09:27:06'),(7,'10','3','2110','2111','45','yokkk','ed','2020-04-12 16:56:18'),(8,'12','2','02.05.2015','02.05.2015','','','ed','2020-04-12 16:56:18'),(9,'14','1','16.1.2018','25.1.2018','2','','ed','2020-04-12 16:56:18');
/*!40000 ALTER TABLE `internship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `internship_capacity`
--

DROP TABLE IF EXISTS `internship_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internship_capacity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session` varchar(45) DEFAULT NULL,
  `internship_type` varchar(45) DEFAULT NULL,
  `firm_id` int DEFAULT NULL,
  `firm_staff_name` varchar(45) DEFAULT NULL,
  `firm_staff_title` varchar(45) DEFAULT NULL,
  `capacity_girl` varchar(45) DEFAULT NULL,
  `capacity_boy` varchar(45) DEFAULT NULL,
  `skills_req` varchar(45) DEFAULT NULL,
  `report` varchar(2500) DEFAULT NULL,
  `username_id` varchar(45) DEFAULT NULL,
  `record_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internship_capacity`
--

LOCK TABLES `internship_capacity` WRITE;
/*!40000 ALTER TABLE `internship_capacity` DISABLE KEYS */;
INSERT INTO `internship_capacity` VALUES (1,'2020','1.Yaz Stajı -10. Sınıf',7,'selim','','1','1','','otomasyon','ed','2020-04-12 15:19:31'),(2,'2020','1.Yaz Stajı -10. Sınıf',2,'mehmet','hr','4','5','çizim','olumlu','ed',NULL),(3,'2020','2.Yaz Stajı -11. Sınıf',3,'23423','2342','4','5','24feefefewqf','qfqfcwcqwfecqfwfwe','ed',NULL),(4,'2022','2.Yaz Stajı -11. Sınıf',4,'dertli','2342','2','2','24feefefewqf','xvbxbxbxvxbvxb','ed',NULL),(5,'2020','1.Yaz Stajı -10. Sınıf',5,'gull','','7','7','yokkk','kız istemiyor','ed','2020-04-12 15:17:15'),(6,'2021','1.Yaz Stajı -10. Sınıf',2,'mert','ty','3','3',NULL,NULL,NULL,NULL),(7,'2021','1.Yaz Stajı -10. Sınıf',8,'ahmet','hr','1','0','yok','alındııı','ed',NULL),(8,'2020','2.Yaz Stajı -11. Sınıf',5,'eray','','2','1','kodku','olumduz\nasdfasdf \nads\nasdfs\n\n\nasdf\na\ndsf\na\n\n\nas\nfsa \ndf\nasd\nf\nsdfsdfsdafasf\n\nadsf\nasd\nfasd\nfa','ed','2020-04-12 15:24:02'),(9,'2020','1.Yaz Stajı -10. Sınıf',0,'','','','','','','ed',NULL),(10,'2020','1.Yaz Stajı -10. Sınıf',12,'serdar','','1','0','elektrik','olumlu','ed',NULL);
/*!40000 ALTER TABLE `internship_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `surname` varchar(45) DEFAULT NULL,
  `birthday` varchar(45) DEFAULT '01.01.2000',
  `tc_no` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT 'name',
  `telephone` varchar(20) DEFAULT NULL,
  `parent_name` varchar(20) DEFAULT NULL,
  `parent_telephone` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `adress` varchar(300) DEFAULT NULL,
  `register_date` varchar(45) DEFAULT NULL,
  `school_number` varchar(10) DEFAULT NULL,
  `departure` varchar(20) DEFAULT NULL,
  `class_level` varchar(45) DEFAULT NULL,
  `class` varchar(20) DEFAULT NULL,
  `image_link` varchar(200) DEFAULT NULL,
  `notes` varchar(500) DEFAULT NULL,
  `record_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `tc_no_UNIQUE` (`tc_no`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (2,'','','','234242','','','','','','','ed@ed','','','EETA','9','A','','',NULL),(3,'','','','123','','','','','','','','','','EETA','9','A','','',NULL),(4,'ahmet','hay','','11','','','','','','','','','','EETA','9','A','','',NULL),(5,'murat','deva','','1234','','','','','','','','','','EETA','9','A','','',NULL),(6,'ahmet','verta','','3456','','','','','','','','','111','EETA','9','A','3456_resim.png','',NULL),(7,'mehmet','dert','','2222','','','','','','','','','','EETA','10','A','2222_resim.png','',NULL),(8,'memo','dur','','34','','','','','','','','','','MKTA','9','A','34_resim.png','',NULL),(9,'İpek','BAl','19.1.2000','12','','1512','ahmet','05112244','','','','16.1.2018','45','EETA','9','A','12_resim.png','',NULL),(10,'Yavuz','Bektas','10.7.1982','514','ybektas@gmail','050555555','yılmaz','054232313','izmir','karşıyaka','bostanlı','10.05.2018','5005','EETA','9','A','514_resim.png','karşıyaka',NULL),(11,'Serkan','Uslu','21/02/2000','50221112445','serkan@gmail.com','5052211445','ahmet uslu','5544558554','izmir','çiğli','karabağlar','04/12/2020','111','EETA','9','A','50221112445_resim.png','tembel',NULL),(12,'Mira','Bektaş','1.7.2020','51433333','mira@gmail','0532','yavuz Bektaş','053222155','izmir','karşıyaka','bostanlı','15.9.2022','5005','EETA','9','A','51433333_resim.png','çalışkan',NULL),(13,'Ogün','Bektaş','20.1.2011','12345','','532412343','selim bektas','505045554','izmir','karşıyaka','şemikler','8.7.2020','4421','EOTA','9','A','12345_resim.png','pub g hayranı','2020-04-12 12:56:19'),(14,'Ogün','Bektaş','20.1.2011','333423','','532457475','selim bektas','505045554','izmir','karşıyaka','şemikler','8.7.2020','4421','EOTA','9','A','12345_resim.png','pub g hayranı',NULL),(15,'Lara','Bektaş','8.6.2020','50878170770','','0535255255','Eda Bektas','0505222222','','','','15.12.2020','1123','EOTA','9','A','50878170770_resim.png','çok zekii bir kız','2020-04-12 13:20:40');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_detail`
--

DROP TABLE IF EXISTS `teacher_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_detail` (
  `idteacher_detail` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `departure` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `status` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `start_year` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `state` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `adress` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `pers_email` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `telephone` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `university` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `uni_departure` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `profile_image` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `cv_file` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `fb_link` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `linkedin_link` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `blog_link` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `other_link` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `record_date` varchar(45) CHARACTER SET utf8 DEFAULT 'CURRENT_TIMESTAMP',
  PRIMARY KEY (`idteacher_detail`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_detail`
--

LOCK TABLES `teacher_detail` WRITE;
/*!40000 ALTER TABLE `teacher_detail` DISABLE KEYS */;
INSERT INTO `teacher_detail` VALUES (7,'ed','EOTA','EVET','23/23/23','ilçeee','adresss','eda@mail','(050)-(505055)','celalll','elektrik','(225)-(345)ed.png','225345ed.pdf','erfeff','linkk','bloggg','digerrr','CURRENT_TIMESTAMP');
/*!40000 ALTER TABLE `teacher_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(16) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(32) NOT NULL,
  `tc_no` int NOT NULL DEFAULT '1',
  `user_name_surname` varchar(45) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `admin` varchar(1) DEFAULT 'N',
  PRIMARY KEY (`username`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `tc_no_UNIQUE` (`tc_no`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('ed','ed@ed','12',225345,'eda bektas','2020-04-08 09:58:07','E');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-13 15:13:25
