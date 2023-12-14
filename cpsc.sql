-- MySQL dump 10.13  Distrib 8.1.0, for Linux (x86_64)
--
-- Host: localhost    Database: cpsc
-- ------------------------------------------------------
-- Server version	8.1.0

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
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `CustomerName` varchar(255) NOT NULL,
  `ContactName` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `City` varchar(100) DEFAULT NULL,
  `PostalCode` varchar(20) DEFAULT NULL,
  `Country` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customers`
--

LOCK TABLES `Customers` WRITE;
/*!40000 ALTER TABLE `Customers` DISABLE KEYS */;
INSERT INTO `Customers` VALUES (1,'Eco Shopper','Alice Johnson','789 Eco Ave','EcoTown','ET789','EcoCountry'),(2,'Green Buyer','Bob Brown','321 Green St','EcoVille','EV321','EcoLand'),(3,'Green Living Store','Olivia Green','456 Nature Road','EcoTown','ET456','EcoCountry'),(4,'Earth Friendly Goods','Sam Earth','654 Eco Boulevard','GreenVille','GV654','Greenland'),(5,'EcoLife Essentials','Lily Green','111 Nature Blvd','EcoCity','EC111','EcoNation'),(6,'Sustainable Living Solutions','Oscar Organic','222 Green Lane','GreenVille','GV222','Greenland'),(7,'Natural Home Goods','Emma Earth','333 Eco Road','EcoTopia','ET333','EcoNation'),(8,'GreenTech Gadgets','Henry Green','444 Eco Street','Green Valley','GV444','Greenland'),(9,'EcoFriendly Creations','Sophia Sustainable','555 Green Ave','EcoVista','EV555','EcoNation');
/*!40000 ALTER TABLE `Customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrderDetails`
--

DROP TABLE IF EXISTS `OrderDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `OrderDetails` (
  `OrderDetailID` int NOT NULL AUTO_INCREMENT,
  `OrderID` int DEFAULT NULL,
  `ProductID` int DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`OrderDetailID`),
  KEY `OrderID` (`OrderID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `OrderDetails_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `Orders` (`OrderID`),
  CONSTRAINT `OrderDetails_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `Products` (`ProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrderDetails`
--

LOCK TABLES `OrderDetails` WRITE;
/*!40000 ALTER TABLE `OrderDetails` DISABLE KEYS */;
INSERT INTO `OrderDetails` VALUES (1,1,1,2,2.99),(2,1,3,1,15.99),(3,2,2,1,10.50),(4,3,1,15,15.00),(5,3,1,3,5.99),(6,3,2,2,19.99),(7,4,3,4,8.50),(8,6,2,15,13.00),(9,8,1,2,14.99),(10,8,3,1,24.99),(11,9,2,2,9.50),(12,9,4,3,19.99),(13,10,5,1,39.95);
/*!40000 ALTER TABLE `OrderDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int DEFAULT NULL,
  `OrderDate` date DEFAULT NULL,
  `ShipDate` date DEFAULT NULL,
  `ShipAddress` varchar(255) DEFAULT NULL,
  `ShipCity` varchar(100) DEFAULT NULL,
  `ShipPostalCode` varchar(20) DEFAULT NULL,
  `ShipCountry` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `Orders_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customers` (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (1,1,'2023-11-01','2023-11-05','789 Eco Ave','EcoTown','ET789','EcoCountry'),(2,2,'2023-11-03','2023-11-08','321 Green St','EcoVille','EV321','EcoLand'),(3,1,'2023-12-14','2023-12-16','One Chapman Road','Orange','92620','US'),(4,1,'2023-12-01','2023-12-05','456 Nature Road','EcoTown','ET456','EcoCountry'),(5,2,'2023-12-03','2023-12-08','654 Eco Boulevard','GreenVille','GV654','Greenland'),(6,3,'2023-12-15','2023-12-16','123 Joe St','Joeville','JO154','USA'),(7,3,'2024-05-01','2024-05-05','111 Nature Blvd','EcoCity','EC111','EcoNation'),(8,4,'2024-05-03','2024-05-08','222 Green Lane','GreenVille','GV222','Greenland'),(9,5,'2024-05-05','2024-05-10','333 Eco Road','EcoTopia','ET333','EcoNation'),(10,6,'2024-05-07','2024-05-12','444 Eco Street','Green Valley','GV444','Greenland'),(11,7,'2024-05-09','2024-05-14','555 Green Ave','EcoVista','EV555','EcoNation');
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Products`
--

DROP TABLE IF EXISTS `Products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Products` (
  `ProductID` int NOT NULL AUTO_INCREMENT,
  `ProductName` varchar(255) NOT NULL,
  `SupplierID` int DEFAULT NULL,
  `Category` varchar(100) DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL,
  `UnitsInStock` int DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  KEY `SupplierID` (`SupplierID`),
  CONSTRAINT `Products_ibfk_1` FOREIGN KEY (`SupplierID`) REFERENCES `Suppliers` (`SupplierID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Products`
--

LOCK TABLES `Products` WRITE;
/*!40000 ALTER TABLE `Products` DISABLE KEYS */;
INSERT INTO `Products` VALUES (1,'Bamboo Toothbrush',1,'Personal Care',2.99,15097),(2,'Reusable Water Bottle',1,'Outdoor',10.50,185),(3,'Organic Cotton T-shirt',2,'Clothing',15.99,150),(4,'Bobs T-shirt',2,'Clothing',69.99,15),(5,'Recycled Paper Notebook',2,'Stationery',5.99,50),(6,'Solar-Powered LED Lamp',1,'Home Decor',19.99,75),(7,'Bamboo Cutlery Set',1,'Kitchen',8.50,100),(8,'Recyclable Phone Case',3,'Electronics',14.99,50),(9,'Bamboo Cutting Board',4,'Kitchen',9.50,100),(10,'Solar-Powered Charger',5,'Electronics',24.99,30),(11,'Organic Fruit Basket',1,'Food',19.99,20),(12,'Eco-Friendly Backpack',2,'Fashion',39.95,15);
/*!40000 ALTER TABLE `Products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Suppliers`
--

DROP TABLE IF EXISTS `Suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Suppliers` (
  `SupplierID` int NOT NULL AUTO_INCREMENT,
  `SupplierName` varchar(255) NOT NULL,
  `ContactName` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `City` varchar(100) DEFAULT NULL,
  `PostalCode` varchar(20) DEFAULT NULL,
  `Country` varchar(100) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`SupplierID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Suppliers`
--

LOCK TABLES `Suppliers` WRITE;
/*!40000 ALTER TABLE `Suppliers` DISABLE KEYS */;
INSERT INTO `Suppliers` VALUES (1,'EcoFriendly Ltd','John Doe','123 Green Road','EcoCity','EC123','Ecoland','123-456-7890'),(2,'NatureGoods Inc','Jane Smith','456 Natural Way','GreenVille','GV456','Greenland','987-654-3210'),(3,'GreenTech Supplies','Mark Green','567 Eco Street','EcoCity','EC567','Ecoland','555-123-4567'),(4,'NaturalLiving Co.','Emily Nature','789 Green Lane','GreenVille','GV789','Greenland','987-654-3210'),(5,'GreenTech Innovations','Alex Greenfield','456 Eco Avenue','EcoCity','EC456','EcoNation','111-222-3333'),(6,'EcoSolutions Unlimited','Emma Evergreen','789 Nature Street','GreenVille','GV789','Greenland','444-555-6666'),(7,'Sustainable Living Co.','Oliver Organic','123 Green Blvd','EcoTopia','ET123','Greenland','777-888-9999'),(8,'Natural Wonders Supply','Sophie Sustainable','987 Eco Lane','EcoHaven','EH987','Greenland','555-666-7777'),(9,'EcoGoods Emporium','Charlie Green','321 Eco Road','EcoVista','EV321','EcoNation','888-999-0000');
/*!40000 ALTER TABLE `Suppliers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-14 20:42:18
