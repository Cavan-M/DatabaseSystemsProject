CREATE DATABASE  IF NOT EXISTS `licensestore` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `licensestore`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: licensestore
-- ------------------------------------------------------
-- Server version	5.7.41-log

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
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `email` varchar(70) NOT NULL,
  `password` varchar(60) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES ('123@123.com','cavan','Cavan','McLellan'),('carl@carl.com','carl','Carl','Parl'),('cavan@cavan.com','cavan','Cavan','McLellan'),('kali@kali.com','kali','Kali','Apperley'),('mclellan@cavan.com','mclellan','Mac','Lellan'),('ramis@ramis.com','ramis','Ramis','Qureshi');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `features`
--

DROP TABLE IF EXISTS `features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `features` (
  `package` int(11) NOT NULL,
  `feature` varchar(255) NOT NULL,
  PRIMARY KEY (`package`,`feature`),
  CONSTRAINT `package` FOREIGN KEY (`package`) REFERENCES `packages` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `features`
--

LOCK TABLES `features` WRITE;
/*!40000 ALTER TABLE `features` DISABLE KEYS */;
INSERT INTO `features` VALUES (1001,'Access to the cutting-edge Photoshop program by Adobe'),(1001,'Adobe Creative Cloud Saves and Features'),(1001,'Product Updates'),(1002,'Microsoft Excel'),(1002,'Microsoft Powerpoint'),(1002,'Microsoft Teams'),(1002,'Microsoft Word'),(1002,'Outlook Email'),(1003,'Stream Video in Other Countries'),(1003,'Surf the Web Anonymously'),(1003,'Up to 10 Devices'),(1004,'Download Music for Listening On-The-Go!'),(1004,'Listen to Millions of Songs on Demand'),(1004,'Listen To Music Ad-Free'),(1005,'2 TB of Storage in the Cloud'),(1005,'3 free eSignatures per month'),(1005,'30-Day file and account history'),(1005,'Single User'),(1005,'Unlimited Device Linking'),(1006,'2 TB of Storage in the Cloud'),(1006,'A Single Bill for the Whole Family'),(1006,'Access to Family Room folder'),(1006,'Individual Accounts Up to 6 Users'),(1007,'2 Audio Editors'),(1007,'91 Instruments & Effects'),(1007,'Free Samples, Loops, and Presets'),(1007,'Lifetime Free Product Updates'),(1008,'24/7 Email & Chat Support'),(1008,'300+ Integrations'),(1008,'5 Users'),(1008,'6,000 Monthly Email Sends'),(1008,'Pre-built Email Templates'),(1009,'Audio and video conversations with screen sharing with up to 50 people'),(1009,'Secure collaboration with outside organizations or guests from within Slack'),(1009,'The full context of your organization’s message history at your fingertips'),(1009,'Timely info and actions in one place with unlimited integrations');
/*!40000 ALTER TABLE `features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `licenses`
--

DROP TABLE IF EXISTS `licenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `licenses` (
  `lkey` varchar(100) NOT NULL,
  `expiry` varchar(50) NOT NULL,
  `package` int(11) NOT NULL,
  `owner` varchar(70) NOT NULL,
  PRIMARY KEY (`lkey`),
  UNIQUE KEY `key_UNIQUE` (`lkey`),
  KEY `pkg_idx` (`package`),
  KEY `own_idx` (`owner`),
  CONSTRAINT `own` FOREIGN KEY (`owner`) REFERENCES `customers` (`email`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pkg` FOREIGN KEY (`package`) REFERENCES `packages` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `licenses`
--

LOCK TABLES `licenses` WRITE;
/*!40000 ALTER TABLE `licenses` DISABLE KEYS */;
INSERT INTO `licenses` VALUES ('325ca26e730c68cc4ce48e9e801f0312','2024-03-21',1002,'kali@kali.com'),('33af962dbd3c1f9b14e04dadcfae1550','2023-04-25',1009,'123@123.com'),('3671c11470b622065768d3e1c3c53caa','2023-04-22',1009,'kali@kali.com'),('41ce68b492b0d3071bd6e1fba9277e7b','2023-04-26',1005,'cavan@cavan.com'),('44b48e534ad1ec7c29e36fce0fbce49f','2023-04-24',1005,'ramis@ramis.com'),('73303115bcfa7bf342e6c381c554c3a8','2023-09-24',1008,'kali@kali.com'),('7f183e2c77b9b23be52628b0a8715a15','2023-04-25',1001,'ramis@ramis.com'),('8f045fc19588eb21f98c297a982b22e2','2023-04-25',1001,'carl@carl.com'),('9bbfaeffbe7ec3e3470789264f1d3bd7','2023-04-24',1001,'ramis@ramis.com'),('a8d3faf855360755bffdc85b10028b79','2023-09-27',1008,'123@123.com'),('e48baa339c90b7c8d85b72b351bdf2b9','2023-04-25',1005,'123@123.com'),('ea8fccc5a0c4ec091f926c0d2f08f207','2023-09-28',1008,'cavan@cavan.com'),('f49d99b8be0dc3828594407fbcd987af','2023-04-25',1001,'123@123.com');
/*!40000 ALTER TABLE `licenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_packages`
--

DROP TABLE IF EXISTS `order_packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_packages` (
  `item` int(11) NOT NULL AUTO_INCREMENT,
  `ordr` int(11) NOT NULL,
  `package` int(11) NOT NULL,
  PRIMARY KEY (`item`),
  KEY `order_ref_idx` (`ordr`),
  KEY `pkg_ref_idx` (`package`),
  CONSTRAINT `order_ref` FOREIGN KEY (`ordr`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pkg_ref` FOREIGN KEY (`package`) REFERENCES `packages` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_packages`
--

LOCK TABLES `order_packages` WRITE;
/*!40000 ALTER TABLE `order_packages` DISABLE KEYS */;
INSERT INTO `order_packages` VALUES (8,10,1001),(9,10,1007),(10,10,1005),(11,11,1001),(12,11,1002),(13,11,1004),(14,12,1002),(15,12,1008),(16,12,1001),(17,13,1003),(18,13,1004),(19,13,1005),(22,15,1001);
/*!40000 ALTER TABLE `order_packages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total` float NOT NULL DEFAULT '0',
  `date` varchar(50) NOT NULL,
  `customer` varchar(70) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `user_idx` (`customer`),
  CONSTRAINT `user` FOREIGN KEY (`customer`) REFERENCES `customers` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,19.99,'2023-03-23 21:04:26','cavan@cavan.com'),(2,19.99,'2023-03-23 21:05:45','cavan@cavan.com'),(3,19.99,'2023-03-23 21:06:25','cavan@cavan.com'),(4,19.99,'2023-03-23 21:06:45','cavan@cavan.com'),(5,19.99,'2023-03-23 21:09:03','cavan@cavan.com'),(6,19.99,'2023-03-23 21:10:37','cavan@cavan.com'),(10,332.97,'2023-03-24 22:30:05','ramis@ramis.com'),(11,89.97,'2023-03-25 11:00:19','ramis@ramis.com'),(12,229.97,'2023-03-25 12:50:49','123@123.com'),(13,62.97,'2023-03-25 12:51:17','123@123.com'),(15,19.99,'2023-03-25 12:52:18','123@123.com');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages`
--

DROP TABLE IF EXISTS `packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `packages` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `cost` float NOT NULL,
  `period` varchar(10) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1010 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages`
--

LOCK TABLES `packages` WRITE;
/*!40000 ALTER TABLE `packages` DISABLE KEYS */;
INSERT INTO `packages` VALUES (1001,'Adobe Photoshop',19.99,'1m'),(1002,'Microsoft Office Premium',59.99,'1y'),(1003,'Express VPN',39.99,'6m'),(1004,'Spotify Premium',9.99,'1m'),(1005,'Dropbox Plus',12.99,'1m'),(1006,'Dropbox Family',21.99,'1m'),(1007,'FL Studio Producer Edition',299.99,'1t'),(1008,'Mailchimp',149.99,'6m'),(1009,'Slack Pro',9.99,'1m');
/*!40000 ALTER TABLE `packages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `refunds`
--

DROP TABLE IF EXISTS `refunds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `refunds` (
  `orderid` int(11) NOT NULL,
  `staff` varchar(70) NOT NULL,
  `date` varchar(60) NOT NULL,
  `customer` varchar(70) NOT NULL,
  `total` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`orderid`),
  KEY `staff_ref_idx` (`staff`),
  KEY `customer_ref_idx` (`customer`),
  CONSTRAINT `cust_ref` FOREIGN KEY (`customer`) REFERENCES `customers` (`email`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `staff_ref` FOREIGN KEY (`staff`) REFERENCES `staff` (`email`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refunds`
--

LOCK TABLES `refunds` WRITE;
/*!40000 ALTER TABLE `refunds` DISABLE KEYS */;
INSERT INTO `refunds` VALUES (14,'cavan@cavan.ca','2023-03-26 19:31:38','123@123.com',309.98),(16,'cavan@cavan.ca','2023-03-26 15:31:42','123@123.com',59.99);
/*!40000 ALTER TABLE `refunds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revocations`
--

DROP TABLE IF EXISTS `revocations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `revocations` (
  `lkey` varchar(100) NOT NULL,
  `staff` varchar(70) NOT NULL,
  `date` varchar(45) NOT NULL,
  `package` int(11) NOT NULL,
  `customer` varchar(70) NOT NULL,
  PRIMARY KEY (`lkey`),
  KEY `staf_ref_idx` (`staff`),
  KEY `cust_ref_idx` (`customer`),
  KEY `pkg_idx` (`package`),
  CONSTRAINT `cust` FOREIGN KEY (`customer`) REFERENCES `customers` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `package_reference` FOREIGN KEY (`package`) REFERENCES `packages` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `usr` FOREIGN KEY (`staff`) REFERENCES `staff` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revocations`
--

LOCK TABLES `revocations` WRITE;
/*!40000 ALTER TABLE `revocations` DISABLE KEYS */;
INSERT INTO `revocations` VALUES ('1e674d4434a0a6e18ddb32ca8a981ef1','cavan@cavan.ca','2023-03-26 18:32:42',1002,'ramis@ramis.com'),('394853073b3e8505425e60b7e2dffe13','cavan@cavan.ca','2023-03-26 18:32:41',1007,'123@123.com'),('d2c87a924ff7582956bfea4c81c8a688','cavan@cavan.ca','2023-03-26 18:32:41',1007,'ramis@ramis.com');
/*!40000 ALTER TABLE `revocations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `email` varchar(70) NOT NULL,
  `password` varchar(100) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES ('cavan@cavan.ca','cavan','Cavan','McLellan');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-26 19:49:42
