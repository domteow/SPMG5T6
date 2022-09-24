-- phpMyAdmin SQL Dump
-- version 4.9.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 22, 2021 at 10:24 AM
-- Server version: 5.7.26
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `is212_example`
--
CREATE DATABASE IF NOT EXISTS `all_in_one_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `all_in_one_db`;

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE staff (
  staff_id int NOT NULL PRIMARY KEY,
  role_id int NOT NULL,
  staff_fname varchar(50) NOT NULL,
  staff_lname varchar(50) NOT NULL,
  email varchar(50) NOT NULL,
  constraint staff_fk foreign key(role_id) references role(role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE role (
  role_id int NOT NULL PRIMARY KEY,
  role_name varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE course (
  course_id varchar(20) NOT NULL PRIMARY KEY,
  course_name varchar(50) NOT NULL,
  course_desc varchar(255) DEFAULT NULL,
  course_status varchar(15) DEFAULT NULL,
  course_type varchar(10) DEFAULT NULL,
  course_category varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `attached_skill`
--

CREATE TABLE attached_skill (
  attached_skill_id int NOT NULL PRIMARY KEY,
  skill_id int NOT NULL,
  course_id int NOT NULL,
  constraint attached_skill_fk foreign key(skill_id) references skill(skill_id), 
  constraint attached_skill_fk2 foreign key(course_id) references course(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `registration`
--

CREATE TABLE registration (
  reg_id int NOT NULL PRIMARY KEY,
  course_id int NOT NULL,
  staff_id int NOT NULL,
  reg_status varchar(20) NOT NULL,
  completion_status varchar(20) NOT NULL, 
  constraint reg_fk foreign key(course_id) references course(course_id), 
  constraint reg_fk2 foreign key(staff_id) references staff(staff_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `skill`
--

CREATE TABLE skill (
  skill_id int NOT NULL PRIMARY KEY,
  skill_desc varchar(255) NOT NULL,
  skill_name varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ljps_role`
--

CREATE TABLE ljps_role (
  ljpsr_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  role_title varchar(20) NOT NULL,
  role_desc varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `role_required_skill`
--

CREATE TABLE role_required_skill (
  skill_id int NOT NULL PRIMARY KEY,
  ljpsr_id int NOT NULL PRIMARY KEY,
  constraint role_required_skill_pk primary key (skill_id, ljpsr_id), 
  constraint role_required_skill_fk foreign key(skill_id) references skill(skill_id), 
  constraint role_required_skill_fk2 foreign key(ljpsr_id) references ljps_role(ljpsr_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `learning_journey`
--

CREATE TABLE learning_journey (
  journey_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  role_id int NOT NULL,
  staff_id int NOT NULL,
  status int NOT NULL, -- 1 = complete, 0 = incomplete
  constraint learning_journey_fk1 foreign key(role_id) references role(role_id), 
  constraint learning_journey_fk2 foreign key(staff_id) references staff(staff_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `lj_course`
--

CREATE TABLE lj_course (
  lj_course_id int NOT NULL PRIMARY KEY,
  journey_id int NOT NULL,
  course_id int NOT NULL,
  constraint lj_course_fk foreign key(journey_id) references learning_journey(journey_id), 
  constraint lj_course_fk2 foreign key(course_id) references course(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Insert test values for Staff table
--

insert into staff values
('1', 'staff', 'Jann', 'Chia', 'jann@allinone@gmail.com'),
('2', 'manager', 'Kelvin', 'Yap', 'kelvin@allinone@gmail.com'),
('3', 'hr', 'Dom', 'Teow', 'dom@allinone@gmail.com');

-- --------------------------------------------------------


-- --------------------------------------------------------

--
-- Dumping data for table `staff`
--

-- INSERT INTO `staff` (`id`, `reg_num`, `hourly_rate`) VALUES
-- (1, 'EV1L', 60),
-- (2, 'AN123', 40),
-- (3, 'CW3588', 45);

-- --------------------------------------------------------

-- 
-- Import data for table `staff`

-- show global variables like 'local_infile';
-- set global local_infile=true;

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE staff 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `role`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE role 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `course`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE course 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `registration`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE item 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `skill`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE item 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `ljps_role`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE item 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `learning_journey`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE item 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `roles_required_skill`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE roles_required_skill 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `lj_course`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE lj_course 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 

-- 
-- Import data for table `attached_skill`

-- LOAD DATA INFILE 
-- 'C:/wamp64/tmp/G10T04/Data/item.txt' 
-- INTO TABLE attached_skill 
-- FIELDS TERMINATED BY '\t' 
-- LINES TERMINATED BY '\r\n' 
-- IGNORE 1 LINES; 