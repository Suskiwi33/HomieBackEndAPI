DROP TABLE IF EXISTS `usuario`;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `usuario` WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS `vivienda`;
CREATE TABLE `vivienda` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `balcony` tinyint(1) DEFAULT NULL,
  `bath_num` int DEFAULT NULL,
  `condition` varchar(50) DEFAULT NULL,
  `floor` int DEFAULT NULL,
  `garage` tinyint(1) DEFAULT NULL,
  `garden` tinyint(1) DEFAULT NULL,
  `ground_size` decimal(10,2) DEFAULT NULL,
  `house_type` varchar(50) DEFAULT NULL,
  `lift` tinyint(1) DEFAULT NULL,
  `loc_city` varchar(100) DEFAULT NULL,
  `loc_district` varchar(100) DEFAULT NULL,
  `loc_neigh` varchar(100) DEFAULT NULL,
  `m2_real` decimal(10,2) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `room_numbers` int DEFAULT NULL,
  `swimming_pool` tinyint(1) DEFAULT NULL,
  `terrace` tinyint(1) DEFAULT NULL,
  `unfurnished` tinyint(1) DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `vivienda_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `vivienda` WRITE;
UNLOCK TABLES;

