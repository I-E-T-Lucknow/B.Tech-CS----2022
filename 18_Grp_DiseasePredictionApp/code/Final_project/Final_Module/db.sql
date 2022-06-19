/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - creditcard
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`creditcard` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `creditcard`;

/*Table structure for table `userdetailes` */

DROP TABLE IF EXISTS `userdetailes`;

CREATE TABLE `userdetailes` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) default NULL,
  `address` varchar(200) default NULL,
  `phone` varchar(200) default NULL,
  `email` varchar(200) default NULL,
  `password` varchar(200) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `userdetailes` */

insert  into `userdetailes`(`id`,`name`,`address`,`phone`,`email`,`password`) values (2,'yash','india','9090909090','y@gmail.com','a'),(4,'sushant','india','9090909090','stawar59@gmail.com','123'),(5,'aarushi','india','9090909090','aarushi@gmail.com','1234');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
