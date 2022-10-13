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
SET FOREIGN_KEY_CHECKS= 0;

--
-- Database: `all_in_one_db`
--

DROP DATABASE IF EXISTS `all_in_one_db`; 
CREATE DATABASE IF NOT EXISTS `all_in_one_db`;
USE `all_in_one_db`;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS role;

CREATE TABLE IF NOT EXISTS role (
  role_id int NOT NULL PRIMARY KEY,
  role_name varchar(20) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS staff; 

CREATE TABLE IF NOT EXISTS staff (
  staff_id int NOT NULL PRIMARY KEY,
  staff_fname varchar(50) NOT NULL,
  staff_lname varchar(50) NOT NULL,
  dept varchar(50) NOT NULL,
  email varchar(255) NOT NULL, 
  role_id int NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS course;

CREATE TABLE IF NOT EXISTS course ( 
  course_id varchar(20) NOT NULL PRIMARY KEY,
  course_name varchar(255) NOT NULL,
  course_desc varchar(65535) DEFAULT NULL,
  course_status varchar(15) DEFAULT NULL,
  course_type varchar(10) DEFAULT NULL,
  course_category varchar(50) DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `attached_skill`
--

DROP TABLE IF EXISTS attached_skill;

CREATE TABLE IF NOT EXISTS attached_skill ( 
  skill_id int NOT NULL,
  course_id varchar(20) NOT NULL,
  constraint attached_skill_pk primary key (skill_id, course_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS registration;

CREATE TABLE IF NOT EXISTS registration ( 
  reg_id int NOT NULL PRIMARY KEY,
  course_id varchar(20) NOT NULL,
  staff_id int NOT NULL,
  reg_status varchar(20) NOT NULL,
  completion_status varchar(20) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `skill`
--

DROP TABLE IF EXISTS skill;

CREATE TABLE IF NOT EXISTS skill (
  skill_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  skill_desc varchar(65535) NOT NULL,
  skill_name varchar(255) NOT NULL,
  active int NOT NULL -- 0 = False, 1 = True 
);

-- --------------------------------------------------------

--
-- Table structure for table `ljps_role`
--

DROP TABLE IF EXISTS ljps_role;

CREATE TABLE IF NOT EXISTS ljps_role ( 
  ljpsr_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  role_title varchar(255) NOT NULL,
  role_desc varchar(65535) NOT NULL, 
  active int NOT NULL -- 0 = False, 1 = True 
);

-- --------------------------------------------------------

--
-- Table structure for table `role_required_skill`
--

DROP TABLE IF EXISTS role_required_skill;

CREATE TABLE IF NOT EXISTS role_required_skill (
  skill_id int NOT NULL,
  ljpsr_id int NOT NULL,
  constraint role_required_skill_pk primary key (skill_id, ljpsr_id)
);

-- --------------------------------------------------------

--
-- Table structure for table `learning_journey` 
--

DROP TABLE IF EXISTS learning_journey;

CREATE TABLE IF NOT EXISTS learning_journey (
  journey_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ljpsr_id int NOT NULL,
  staff_id int NOT NULL,
  status int NOT NULL -- 1 = complete, 0 = incomplete
);

-- --------------------------------------------------------

--
-- Table structure for table `lj_course`
--

DROP TABLE IF EXISTS lj_course;

CREATE TABLE IF NOT EXISTS lj_course (
  journey_id int NOT NULL,
  course_id varchar(20) NOT NULL, 
  constraint lj_course_pk primary key (journey_id, course_id)
);

-- --------------------------------------------------------

--
-- Constraints for table `staff`
--
ALTER TABLE `staff`
  ADD CONSTRAINT `staff_fk` FOREIGN KEY (role_id) REFERENCES role(role_id); 

-- --------------------------------------------------------

--
-- Constraints for table `attached_skill`
--
ALTER TABLE `attached_skill`
  ADD CONSTRAINT `attached_skill_fk` FOREIGN KEY (skill_id) REFERENCES skill(skill_id),
  ADD CONSTRAINT `attached_skill_fk2` FOREIGN KEY (course_id) REFERENCES course(course_id);

-- --------------------------------------------------------

--
-- Constraints for table `registration`
--
ALTER TABLE `registration`
  ADD CONSTRAINT `reg_fk` FOREIGN KEY (course_id) REFERENCES course(course_id),
  ADD CONSTRAINT `reg_fk2` FOREIGN KEY (staff_id) REFERENCES staff(staff_id);

-- --------------------------------------------------------

--
-- Constraints for table `role_required_skill`
--
ALTER TABLE `role_required_skill`
  ADD CONSTRAINT `role_required_skill_fk` FOREIGN KEY (skill_id) REFERENCES skill(skill_id),
  ADD CONSTRAINT `role_required_skill_fk2` FOREIGN KEY (ljpsr_id) REFERENCES ljps_role(ljpsr_id);

-- --------------------------------------------------------

--
-- Constraints for table `learning_journey`
--
ALTER TABLE `learning_journey`
  ADD CONSTRAINT `learning_journey_fk1` FOREIGN KEY (ljpsr_id) REFERENCES ljps_role(ljpsr_id),
  ADD CONSTRAINT `learning_journey_fk2` FOREIGN KEY (staff_id) REFERENCES staff(staff_id);

-- --------------------------------------------------------

--
-- Constraints for table `lj_course`
--
ALTER TABLE `lj_course`
  ADD CONSTRAINT `lj_course_fk` FOREIGN KEY (journey_id) REFERENCES learning_journey(journey_id),
  ADD CONSTRAINT `lj_course_fk2` FOREIGN KEY (course_id) REFERENCES course(course_id);


-- --------------------------------------------------------

-- 

show global variables like 'local_infile';
set global local_infile=true;

LOAD DATA INFILE 
'C:/wamp64/tmp/RawData/courses.csv' 
INTO TABLE course
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/RawData/role.csv' 
INTO TABLE role
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/RawData/staff.csv' 
INTO TABLE staff
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/RawData/registration.csv' 
INTO TABLE registration
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/LjpsData/attached_skill.csv' 
INTO TABLE attached_skill
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/LjpsData/learning_journey.csv' 
INTO TABLE learning_journey
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/LjpsData/lj_course.csv' 
INTO TABLE lj_course
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/LjpsData/ljps_role.csv' 
INTO TABLE ljps_role
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/LjpsData/role_required_skill.csv' 
INTO TABLE role_required_skill
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

-- 

LOAD DATA INFILE 
'C:/wamp64/tmp/LjpsData/skill.csv' 
INTO TABLE skill 
CHARACTER SET latin1 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 ROWS; 

SET FOREIGN_KEY_CHECKS = 1;

