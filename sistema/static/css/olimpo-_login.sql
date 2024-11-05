-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 21, 2024 at 05:31 AM
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
-- Database: `olimpo- login`
--

-- --------------------------------------------------------

--
-- Table structure for table `empleados`
--

CREATE TABLE `empleados` (
  `cc_usu` varchar(15) NOT NULL,
  `nombre` varchar(30) DEFAULT NULL,
  `apellido` varchar(30) DEFAULT NULL,
  `direcion` varchar(80) DEFAULT NULL,
  `contacto_ememergenci` varchar(50) DEFAULT NULL,
  `nombre_contacto` varchar(30) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo` varchar(70) DEFAULT NULL,
  `eps` varchar(20) DEFAULT NULL,
  `contrasenaU` varchar(400) DEFAULT NULL,
  `caja_de_compensacion` varchar(50) DEFAULT NULL,
  `codigo_usu` varchar(20) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `empleados`
--

INSERT INTO `empleados` (`cc_usu`, `nombre`, `apellido`, `direcion`, `contacto_ememergenci`, `nombre_contacto`, `telefono`, `correo`, `eps`, `contrasenaU`, `caja_de_compensacion`, `codigo_usu`, `estado`) VALUES
('123456789', 'Thomas', 'Alvarez', 'luna', '911', 'Police', '3025317882', 'ta87t', 'fami', '11111111', '5214524', 'ADM1', 'Cansado'),
('987654321', 'Andrey', 'Gonzales', 'Infierno', '75435', 'Diablo', '666', 'fel12', 'Nose', '22222222', '1531351', 'AML2', 'Sapo');

-- --------------------------------------------------------

--
-- Table structure for table `tipo_empleado`
--

CREATE TABLE `tipo_empleado` (
  `tipo_empleado` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tipo_empleado`
--

INSERT INTO `tipo_empleado` (`tipo_empleado`) VALUES
('ADM1'),
('AML2'),
('CL'),
('CMR3'),
('RCP4'),
('RMS5');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `empleados`
--
ALTER TABLE `empleados`
  ADD KEY `fk_tipo_empleado` (`codigo_usu`);

--
-- Indexes for table `tipo_empleado`
--
ALTER TABLE `tipo_empleado`
  ADD PRIMARY KEY (`tipo_empleado`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `fk_tipo_empleado` FOREIGN KEY (`codigo_usu`) REFERENCES `tipo_empleado` (`tipo_empleado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
