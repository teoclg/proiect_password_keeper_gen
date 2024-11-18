-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: password_management
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `account_table`
--

DROP TABLE IF EXISTS `account_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_table` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `master_account_name` varchar(128) DEFAULT NULL,
  `master_account_password` varchar(128) DEFAULT NULL,
  `master_account_email` varchar(128) DEFAULT NULL,
  `totp_secret` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_table`
--

LOCK TABLES `account_table` WRITE;
/*!40000 ALTER TABLE `account_table` DISABLE KEYS */;
INSERT INTO `account_table` VALUES (8,'1111','1111','121@31231','LIUXBLRRQD4K6SKX33EZ7WHGORBJSDQJ'),(9,'2222','2222','gorbino@yahoo.com','VLHQS6MOC4FDHXOHV4PYTBSSS7FIEZGS'),(10,'333','333','hugh_giorno@gmail.com','4FDAITYIOBBN43CQN67LNGFWBC7URTHQ'),(11,'444','444','121@31231','2OYGN3PO4ZEHZQY3Y4QXARODJFOLKRMU');
/*!40000 ALTER TABLE `account_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_management_table`
--

DROP TABLE IF EXISTS `password_management_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_management_table` (
  `ID_account` int NOT NULL AUTO_INCREMENT,
  `site_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `account_name` varchar(50) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`ID_account`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_management_table`
--

LOCK TABLES `password_management_table` WRITE;
/*!40000 ALTER TABLE `password_management_table` DISABLE KEYS */;
INSERT INTO `password_management_table` VALUES (1,'teams','andrew_m@gmail.com','andrew.mackenzie','+un}QzYF*M'),(22,'www.reddit.com','old_fuck_mcgay@gmail.com','benjamin_gaming','4412412'),(23,'rrqwqr','erwaea@yahoo.com','tqwrwqr','wrrw'),(24,'www.temu.com','benjamin@gmail.com','benjamin_gaming','sfafa'),(25,'https://account.booking.com/sign-in','stefan@gmail.com','stefan','stefan'),(26,'epantofi.ro','oku@gmail.com','oku','oku');
/*!40000 ALTER TABLE `password_management_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-18 19:43:45
