/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - creditcard155
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`creditcard155` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `creditcard155`;

/*Table structure for table `fraud` */

DROP TABLE IF EXISTS `fraud`;

CREATE TABLE `fraud` (
  `id` int(11) NOT NULL auto_increment,
  `userid` varchar(2000) default NULL,
  `user_amount` varchar(2000) default NULL,
  `fraud_user_zip` varchar(255) default NULL,
  `user_lat` double default NULL,
  `user_long` double default NULL,
  `user_merch_lat` double default NULL,
  `user_merch_long` double default NULL,
  `age` double default NULL,
  `fraud_status` varchar(199) default NULL,
  `fraud_proba` double default NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `fraud` */

insert  into `fraud`(`id`,`userid`,`user_amount`,`fraud_user_zip`,`user_lat`,`user_long`,`user_merch_lat`,`user_merch_long`,`age`,`fraud_status`,`fraud_proba`) values (1,'2','275  ','78201 ',28.44,-98.45,25.786426,-93.68341,57,'FraudDetected',0.51);

/*Table structure for table `nofraud` */

DROP TABLE IF EXISTS `nofraud`;

CREATE TABLE `nofraud` (
  `id` int(50) NOT NULL auto_increment,
  `userid` varchar(2000) default NULL,
  `amount` varchar(2000) default NULL,
  `user_zip` double default NULL,
  `user_lat` double default NULL,
  `user_long` double default NULL,
  `user_merch_lat` double default NULL,
  `user_merch_long` double default NULL,
  `age` varchar(2000) default NULL,
  `nofraud_status` varchar(2000) default NULL,
  `nofraud_proba` double default NULL,
  `user_opi` varchar(2000) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `nofraud` */

insert  into `nofraud`(`id`,`userid`,`amount`,`user_zip`,`user_lat`,`user_long`,`user_merch_lat`,`user_merch_long`,`age`,`nofraud_status`,`nofraud_proba`,`user_opi`) values (1,'2','2500',28611,32.9,-81.72,36.43,43.9,'34','NoFraudDetected',0.91,NULL),(2,'2','340',456,32.9,-90.76,36.09,-81.17,'22','NoFraudDetected',0.83,NULL),(3,'2','340',456,32.9,-90.76,36.09,-81.17,'22','NoFraudDetected',0.83,NULL),(4,'2','290',72,78.9,31.9,-34.9,-81.17,'45','NoFraudDetected',0.71,NULL),(5,'2','314',678,78.9,-81.98,36.09,-81.17,'22','NoFraudDetected',0.77,NULL),(6,'6','2590',531,42.9,-91.9,39.9,-81.17,'49','NoFraudDetected',0.74,NULL),(7,'2','2300',456,32.9,-81.72,56.89,-82.01,'22','NoFraudDetected',0.89,NULL);

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

insert  into `userdetailes`(`id`,`name`,`address`,`phone`,`email`,`password`) values (2,'yash','india','9090909090','y@gmail.com','a'),(4,'sushant','india','9090909090','stawar59@gmail.com','123'),(5,'aarushi','india','9090909090','aarushi@gmail.com','1234'),(6,'kedar','india','9898982929','kedar@gmail.com','12345');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
