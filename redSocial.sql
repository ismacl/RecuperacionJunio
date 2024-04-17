-- MariaDB dump 10.19  Distrib 10.11.4-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: redSocial
-- ------------------------------------------------------
-- Server version	10.11.4-MariaDB-1~deb12u1

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
-- Table structure for table `aficionados`
--

DROP TABLE IF EXISTS `aficionados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aficionados` (
  `Id_aficionado` int(50) NOT NULL,
  `UserName` varchar(50) NOT NULL,
  `Gmail` varchar(50) NOT NULL,
  `Password` varchar(10) NOT NULL,
  `birthDate` date NOT NULL,
  `RegisterDate` date NOT NULL,
  `url_avatar` varchar(255) DEFAULT NULL,
  `Token_Sesion` bigint(20) DEFAULT NULL,
  `Id_Equipo` int(50) NOT NULL,
  PRIMARY KEY (`Id_aficionado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aficionados`
--

LOCK TABLES `aficionados` WRITE;
/*!40000 ALTER TABLE `aficionados` DISABLE KEYS */;
INSERT INTO `aficionados` VALUES
(1,'luis_garcia','luis.garcia@example.com','1234','1990-05-15','2022-04-14','https://cdn-icons-png.flaticon.com/512/4792/4792929.png',1234567890,1),
(2,'maria_rodriguez','maria.rodriguez@example.com','1234','1985-09-22','2022-04-15','https://cdn-icons-png.flaticon.com/512/4792/4792929.png',9876543210,2),
(3,'pedro_martinez','pedro.martinez@example.com','1234','1992-11-30','2022-04-16','https://cdn-icons-png.flaticon.com/512/4792/4792929.png',1357924680,3);
/*!40000 ALTER TABLE `aficionados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comentarios`
--

DROP TABLE IF EXISTS `comentarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comentarios` (
  `id_Comentarios` int(50) NOT NULL,
  `Id_Contenido` int(50) NOT NULL,
  `Id_aficionado` int(50) NOT NULL,
  `Comentario` varchar(50) NOT NULL,
  `Fecha_comentario` date NOT NULL,
  PRIMARY KEY (`id_Comentarios`),
  KEY `fk_comentarios_contenido` (`Id_Contenido`),
  KEY `fk_comentarios_aficionado` (`Id_aficionado`),
  CONSTRAINT `fk_comentarios_aficionado` FOREIGN KEY (`Id_aficionado`) REFERENCES `aficionados` (`Id_aficionado`),
  CONSTRAINT `fk_comentarios_contenido` FOREIGN KEY (`Id_Contenido`) REFERENCES `contenido` (`Id_Contenido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comentarios`
--

LOCK TABLES `comentarios` WRITE;
/*!40000 ALTER TABLE `comentarios` DISABLE KEYS */;
INSERT INTO `comentarios` VALUES
(1,1,2,'¡Gran imagen!','2022-04-01'),
(2,2,1,'Excelente gol','2022-04-02'),
(3,3,3,'Interesante artículo','2022-04-03');
/*!40000 ALTER TABLE `comentarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contenido`
--

DROP TABLE IF EXISTS `contenido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contenido` (
  `Id_Contenido` int(50) NOT NULL,
  `Id_aficionado` int(50) NOT NULL,
  `Id_Equipo` int(50) NOT NULL,
  `Tipo_Contenido` varchar(50) NOT NULL,
  `URL` varchar(1000) DEFAULT NULL,
  `Descripcion` varchar(1000) DEFAULT NULL,
  `Fecha_Publicacion` date NOT NULL,
  PRIMARY KEY (`Id_Contenido`),
  KEY `fk_contenido_aficionado` (`Id_aficionado`),
  KEY `fk_contenido_equipo` (`Id_Equipo`),
  CONSTRAINT `fk_contenido_aficionado` FOREIGN KEY (`Id_aficionado`) REFERENCES `aficionados` (`Id_aficionado`),
  CONSTRAINT `fk_contenido_equipo` FOREIGN KEY (`Id_Equipo`) REFERENCES `equipos` (`Id_Equipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contenido`
--

LOCK TABLES `contenido` WRITE;
/*!40000 ALTER TABLE `contenido` DISABLE KEYS */;
INSERT INTO `contenido` VALUES
(1,1,1,'Foto','https://www.elgrafico.com.ar/media/cache/pub_news_details_large/media/i/d1/af/d1af47273c0c876f9631ed2ec3461da7fad13741.jpg','¡Gran victoria del Real Madrid!','2022-04-01'),
(2,2,2,'Video','https://www.youtube.com/watch?v=cie7RQBlBTE','Golazo del Manchester United','2022-04-02'),
(3,3,3,'Texto',NULL,'El Bayern Munich se prepara para la próxima temporada','2022-04-03');
/*!40000 ALTER TABLE `contenido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipos`
--

DROP TABLE IF EXISTS `equipos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipos` (
  `Id_Equipo` int(50) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Liga` varchar(50) NOT NULL,
  `Pais` varchar(50) NOT NULL,
  `Año_Fundacion` year(4) NOT NULL,
  `Estadio` varchar(50) NOT NULL,
  `url_equipo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id_Equipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipos`
--

LOCK TABLES `equipos` WRITE;
/*!40000 ALTER TABLE `equipos` DISABLE KEYS */;
INSERT INTO `equipos` VALUES
(1,'Real Madrid','La Liga','España',1902,'Santiago Bernabéu','https://cdn-icons-png.flaticon.com/512/4792/4792929.png'),
(2,'Manchester United','Premier League','Inglaterra',1902,'Old Trafford','https://cdn-icons-png.flaticon.com/512/4792/4792929.png'),
(3,'Bayern Munich','Bundesliga','Alemania',1902,'Allianz Arena','https://cdn-icons-png.flaticon.com/512/4792/4792929.png');
/*!40000 ALTER TABLE `equipos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-17 10:49:00
