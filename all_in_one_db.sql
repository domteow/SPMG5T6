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
-- Database: `all_in_one_db`
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
  email varchar(50) NOT NULL
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
  course_id varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `registration`
--

CREATE TABLE registration ( 
  reg_id int NOT NULL PRIMARY KEY,
  course_id varchar(20) NOT NULL,
  staff_id int NOT NULL,
  reg_status varchar(20) NOT NULL,
  completion_status varchar(20) NOT NULL
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
  skill_id int NOT NULL,
  ljpsr_id int NOT NULL,
  constraint role_required_skill_pk primary key (skill_id, ljpsr_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `learning_journey` 
--

CREATE TABLE learning_journey (
  journey_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ljpsr_id int NOT NULL,
  staff_id int NOT NULL,
  status int NOT NULL -- 1 = complete, 0 = incomplete
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `lj_course`
--

CREATE TABLE lj_course (
  lj_course_id int NOT NULL PRIMARY KEY,
  journey_id int NOT NULL,
  course_id varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
-- Dumping data for table `staff`
--

insert into staff (staff_id, role_id, staff_fname, staff_lname, dept, email) values
(1, 'staff', 'Jann', 'Chia', 'Business Intelligence', 'jann@allinone.com'),
(2, 'staff', 'Kelvin', 'Yap', 'Business Intelligence', 'kelvin@allinone.com'),
(3, 'staff', 'Dom', 'Teow', 'Business Intelligence', 'dom@allinone.com');

-- --------------------------------------------------------

--
-- Dumping data for table `role`
--

insert into role (role_id, role_name) values
(1, 'staff'),
(2, 'manager'),
(3, 'hr');

-- --------------------------------------------------------

--
-- Dumping data for table `course`
--

insert into course (course_id, course_name, course_desc, course_status, course_type, course_category) values
('COURSE1', 'Business Strategy', 'you learn business strategy', 'Active', 'Internal', 'Business'),
('COURSE2', 'Foundations of Project Management', 'discover foundational project management terminology', 'Active', 'Internal', 'Business');

-- --------------------------------------------------------

--
-- Dumping data for table `attached_skill`
--

insert into attached_skill (attached_skill_id, skill_id, course_id) values
(1, 1, 'COURSE1'), -- skill: strat analysis, course: biz strat
(2, 2, 'COURSE1'), -- skill: cap analysis, course: biz strat
(3, 2, 'COURSE2'); -- skill: cap analysis, course: foundations of pm

-- --------------------------------------------------------

--
-- Dumping data for table `skill`
--

insert into skill (skill_id, skill_desc, skill_name) values
(1, 'Researching an organization and its working environment to formulate a strategy', 'Strategic Analysis'),
(2, 'A set of tools and calculations used in determining whether a system meets certain specification requirements', 'Capabilities Analysis'),
(3, 'Project management is the process of leading the work of a team to achieve all project goals within the given constraints', 'Project Management');

-- --------------------------------------------------------

--
-- Dumping data for table 'registration'
--

insert into registration (reg_id, course_id, staff_id, reg_status, completion_status) values
(1, 'COURSE1', 2, 'Registered', 'In-Progress'), -- business strategy, kelvin, in prog
(2, 'COURSE2', 1, 'Registered', 'In-Progress'), -- foundations of pm, jann, in prog
(3, 'COURSE1', 1, 'Registered', 'Completed'); -- business strategy, jann, completed

-- --------------------------------------------------------

--
-- Dumping data for table 'ljps_role'
--

insert into ljps_role (ljpsr_id, role_title, role_desc) values
(1, 'Accountant', 'Accountants are responsible for financial audits, reconciling bank statements, and ensuring financial records are accurate throughout the year.'), 
(2, 'Project Manager', 'Project managers are accountable for planning and allocating resources, preparing budgets, monitoring progress, and keeping stakeholders informed throughout the project lifecycle'),
(3, 'Business Intelligence Analysts', 'Business Intelligence Analysts capitalise on data and translate it into insights for the company in order to make informed decisions.');

-- --------------------------------------------------------

--
-- Dumping data for table `role_required_skill`
--

insert into role_required_skill (skill_id, ljpsr_id) values
(1, 1), -- strat analysis, accountant
(2, 1), -- cap analysis, accountant
(3, 2); -- project management, project manager

-- --------------------------------------------------------

--
-- Dumping data for table `learning_journey`
--

insert into learning_journey (journey_id, ljpsr_id, staff_id, status) values
(1, 1, 2, 0), -- accountant, kelvin, incomplete
(2, 2, 1, 0), -- project manager, jann, incomplete
(3, 1, 1, 0); -- accountant, jann, incomplete

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