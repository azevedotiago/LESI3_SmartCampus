-- MariaDB dump 10.19  Distrib 10.5.15-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: smartenergy
-- ------------------------------------------------------
-- Server version	10.5.15-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `smartenergy`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `smartenergy` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `smartenergy`;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `iddevices` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `macaddress` varchar(18) COLLATE utf8_bin DEFAULT NULL,
  `coordinatex` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `coordinatey` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`iddevices`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,'2022-11-18 11:51:07','00:00:b3:02:d3:00','0','0'),(2,'2022-11-18 11:51:07','00:00:b3:02:d3:01','0','0'),(3,'2022-11-18 11:55:05','00:00:b3:02:d3:03','0','0'),(4,'2022-11-18 11:55:36','00:00:b3:02:d3:04','0','0'),(5,'2022-11-18 12:00:52','00:ff:b3:02:d3:00','0','0'),(6,'2022-11-18 12:06:47','00:ff:b3:02:d3:05','0','0');
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `idlogs` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `ipaddress` varchar(16) DEFAULT NULL,
  `valled` tinyint(3) unsigned DEFAULT NULL,
  `stateled` tinyint(3) unsigned DEFAULT NULL,
  `valldr` smallint(5) unsigned DEFAULT NULL,
  `valldrnew` tinyint(3) unsigned DEFAULT NULL,
  `valpir` tinyint(3) unsigned DEFAULT NULL,
  `statepir` tinyint(3) unsigned DEFAULT NULL,
  `devices_iddevices` int(11) NOT NULL,
  PRIMARY KEY (`idlogs`,`devices_iddevices`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'2022-11-18 11:59:55','10.10.10.100',200,1,543,50,30,0,4),(2,'2022-11-18 12:00:14','10.10.10.100',200,1,543,50,30,0,4),(3,'2022-11-18 12:00:33','10.10.10.100',200,1,543,50,30,0,4),(4,'2022-11-18 12:00:37','10.10.10.100',200,1,543,50,30,0,1),(5,'2022-11-18 12:00:57','10.10.10.100',200,1,543,50,30,0,5),(6,'2022-11-18 12:03:41','10.10.10.100',200,1,543,50,30,0,5),(7,'2022-11-18 12:04:25','10.10.10.100',200,1,543,50,30,0,5),(8,'2022-11-18 12:04:25','10.10.10.100',200,1,543,50,30,0,5),(9,'2022-11-18 12:05:34','10.10.10.100',200,1,543,50,30,0,5),(10,'2022-11-18 12:06:34','10.10.10.100',200,1,543,50,30,0,5),(11,'2022-11-18 12:07:06','10.10.10.100',200,1,543,50,30,0,6),(12,'2022-11-18 12:12:07','10.10.10.100',200,1,543,50,30,0,6),(13,'2022-11-18 12:12:08','10.10.10.100',200,1,543,50,30,0,6),(14,'2022-11-18 12:12:19','10.10.10.100',200,1,543,50,30,0,6);
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permissions` (
  `idpermissions` int(11) NOT NULL,
  `datetime` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `type` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`idpermissions`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `idusers` int(11) NOT NULL,
  `datetime` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `username` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `name` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `password` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `permissions_idpermissions` int(11) NOT NULL,
  PRIMARY KEY (`idusers`,`permissions_idpermissions`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-18 12:16:00
