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
  `ID_master_account` int NOT NULL AUTO_INCREMENT,
  `master_account_email` varchar(45) DEFAULT NULL,
  `master_account_name` varchar(45) DEFAULT NULL,
  `master_account_password` varchar(256) DEFAULT NULL,
  `totp_secret` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`ID_master_account`),
  UNIQUE KEY `ID_master_account_UNIQUE` (`ID_master_account`),
  UNIQUE KEY `master_account_email_UNIQUE` (`master_account_email`),
  UNIQUE KEY `master_account_name_UNIQUE` (`master_account_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_table`
--

LOCK TABLES `account_table` WRITE;
/*!40000 ALTER TABLE `account_table` DISABLE KEYS */;
INSERT INTO `account_table` VALUES (1,'444@gmail.com','444','444','VZGKS6R2DEPEJ6LWAVRAUY7N55X3KXJ2'),(3,'erwqerwq@yahoo.com','666','666','VZGKS6R2DEPEJ6LWAVRAUY7N55X3KXJ2'),(4,'rweqrqw@gmail.com','777','777','IDMNEZKRXV6GRGBZHNTCJ2MVNOCSGM7U'),(5,'oku_san@yahoo.com','999','999','4FWWMEVQFGUTYUVYKF52EJUFW6KG73ZX'),(7,'gorbino@yahoo.com','525','$2b$12$wc3Btq6XKiOJzE1GFBZuEubA2ltKF8s01OdSzb8fHb0PVg1ahKH0O','F3D27JBFFYRXNNHOSKBOLYSX52QFWBRZ');
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
  `details` varchar(100) DEFAULT NULL,
  `ID_master_account` int DEFAULT NULL,
  PRIMARY KEY (`ID_account`),
  UNIQUE KEY `ID_account_UNIQUE` (`ID_account`),
  KEY `ID_master_account_idx` (`ID_master_account`),
  CONSTRAINT `ID_master_account` FOREIGN KEY (`ID_master_account`) REFERENCES `account_table` (`ID_master_account`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_management_table`
--

LOCK TABLES `password_management_table` WRITE;
/*!40000 ALTER TABLE `password_management_table` DISABLE KEYS */;
INSERT INTO `password_management_table` VALUES (1,'teams','andrew_m@gmail.com','andrew.mackenzie','+un}QzYF*M','ye',1),(2,'facebook','andrew_m@gmail.com','andrew123','I~vT)E|_|$','ne',5),(5,'youtube','benjamin@gmail.com','benjamin_gaming','4756sfdg','32532e',5),(6,'facebook','benjamax@gmail.com','terwtewgs','etqwarasz','dsadas',7),(7,'epantofi.ro','dude@yahoo.com','dude','Dueud1234.','no',3),(10,'facebook.com','444@gmail.com','gasgadfaf','AEoZELVHpG/PTUNhHlMP+4IbnhdUz8FfJMT+Pn7XJPz1Q76bxLtoLp4dmCNaukCLhSR3EC4=','fwqrqw',7);
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

-- Dump completed on 2025-01-09 11:18:12
