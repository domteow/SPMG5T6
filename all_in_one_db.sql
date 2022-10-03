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
  dept varchar(50) NOT NULL, 
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
  skill_id int NOT NULL,
  course_id varchar(20) NOT NULL,
  constraint attached_skill_pk primary key (skill_id, course_id)
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
  journey_id int NOT NULL,
  course_id varchar(20) NOT NULL, 
  constraint lj_course_pk primary key (journey_id, course_id)
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
-- Dumping data for table `role`
--

-- insert into role (role_id, role_name) values
-- (1, 'staff'),
-- (2, 'manager'),
-- (3, 'hr');

-- --------------------------------------------------------

--
-- Dumping data for table `staff`
--

-- insert into staff (staff_id, role_id, staff_fname, staff_lname, dept, email) values
-- (1, 1, 'Jann', 'Chia', 'Business Intelligence','jann@allinone.com'),
-- (2, 1, 'Kelvin', 'Yap', 'Business Intelligence', 'kelvin@allinone.com'),
-- (3, 1, 'Dom', 'Teow', 'Business Intelligence', 'dom@allinone.com');


-- --------------------------------------------------------

--
-- Dumping data for table `course`
--

-- insert into course (course_id, course_name, course_desc, course_status, course_type, course_category) values
-- ('COURSE1', 'Business Strategy', 'you learn business strategy', 'Active', 'Internal', 'Business'),
-- ('COURSE2', 'Foundations of Project Management', 'discover foundational project management terminology', 'Active', 'Internal', 'Business'),
-- ('COURSE3',	'Accounting Fundamentals',	'financial statements and more!',	'Active', 'Internal',	'Finance'),
-- ('COURSE4', 'Writing & Reasoning',	'be better at writing emails',	'Active',	'Internal',	'Business'),
-- ('COURSE5',	'User Interface & User Experience',	'prototypes, wireframes, user design stuff',	'Active',	'Internal',	'Design'),
-- ('COURSE6',	'Business Value with User Experience',	'how nice app make good money',	'Active',	'External', 'Design');
-- --------------------------------------------------------

--
-- Dumping data for table `skill`
--

insert into skill (skill_id, skill_desc, skill_name) values
(1, 'Researching an organization and its working environment to formulate a strategy', 'Strategic Analysis'),
(2, 'A set of tools and calculations used in determining whether a system meets certain specification requirements', 'Capabilities Analysis'),
(3, 'Project management is the process of leading the work of a team to achieve all project goals within the given constraints', 'Project Management'),
(4,	'design for usability', 'User-Centric Design'),
(5,	'how to bring value to business',	'Value Proposition'),
(6,	'beginner level accounting things', 'Accounting (Basics)'), 
(7,	'how to talk like businessman and woman',	'Business Communication');

-- --------------------------------------------------------

--
-- Dumping data for table `attached_skill`
--

insert into attached_skill (skill_id, course_id) values
(1, 'COURSE1'), -- skill: strat analysis, course: biz strat
(2, 'COURSE1'), -- skill: cap analysis, course: biz strat
(2, 'COURSE2'), -- skill: cap analysis, course: foundations of pm
(3, 'COURSE2'), -- skill: project mgt, course: foundations of pm
(6, 'COURSE3'), -- skill: accounting (basics), course: accounting fundamentals
(7, 'COURSE4'), -- skill: biz comm, course: writing & reasoning
(4, 'COURSE5'), -- skill: user-centric design, course: user interface & user exp 
(5, 'COURSE6'); -- skill: value prop, course: business value with ux 

-- --------------------------------------------------------

--
-- Dumping data for table 'registration'
--

-- insert into registration (reg_id, course_id, staff_id, reg_status, completion_status) values
-- (1, 'COURSE1', 2, 'Registered', 'In-Progress'), -- business strategy, kelvin, in prog
-- (2, 'COURSE2', 1, 'Registered', 'In-Progress'), -- foundations of pm, jann, in prog
-- (3, 'COURSE1', 1, 'Registered', 'Completed'), -- business strategy, jann, completed
-- (4,	'COURSE5', 3,	'Registered',	'In-Progress'), -- uiux, dom, in prog 
-- (5,	'COURSE2', 2,	'Registered',	'In-Progress'), -- foundations of pm, kelvin, completed
-- (6,	'COURSE3',	2, 'Registered',	'Completed'), -- accounting fundamentals, kelvin, completed
-- (7, 'COURSE6',	3,	'Registered',	'In-Progress'), -- business value with ui, dom, inprog
-- (8,	'COURSE1',	1,	'Registered',	'In-Progress'), -- business strat, jann, in prog
-- (9,	'COURSE3',	1,	'Registered',	'In-Progress'); -- accounting fundamentals, jann, in prog 

-- --------------------------------------------------------

--
-- Dumping data for table 'ljps_role'
--

insert into ljps_role (ljpsr_id, role_title, role_desc) values
(1, 'Accountant', 'Accountants are responsible for financial audits, reconciling bank statements, and ensuring financial records are accurate throughout the year.'), 
(2, 'Project Manager', 'Project managers are accountable for planning and allocating resources, preparing budgets, monitoring progress, and keeping stakeholders informed throughout the project lifecycle'),
(3,	'UI/UX Designer',	'design allinone application and all its features'), 
(4,	'Business Development',	'help to develop the business'); 

-- --------------------------------------------------------

--
-- Dumping data for table `role_required_skill`
--

insert into role_required_skill (skill_id, ljpsr_id) values
(1,	1), -- strat analysis, accountant
(2,	1), -- cap analysis, accountant
(6,	1), -- value prop, accountant
(3,	2), -- project mgt, project manager
(7,	2), -- business comm, proj manager
(4,	3), -- user-centric design, ui/ux designer
(5,	3), -- value prop, ui/ux designer
(1,	4), -- strat analysis, biz dev
(2,	4), -- cap analysis, biz dev
(7,	4); -- biz comm, biz dev
-- --------------------------------------------------------

--
-- Dumping data for table `learning_journey`
--

insert into learning_journey (journey_id, ljpsr_id, staff_id, status) values
(1, 1, 2, 0), -- accountant, kelvin, incomplete
(2, 2, 1, 0), -- project manager, jann, incomplete
(3, 1, 1, 0), -- accountant, jann, incomplete
(4, 3, 3, 0); -- uiux designer, dom, incomplete

-- --------------------------------------------------------

--
-- Dumping data for table `lj_course`
--

insert into lj_course (journey_id, course_id) values
(1,	'COURSE1'),  -- lj #1 (accountant, kelvin, incomplete), business strat
(1,	'COURSE2'),  -- lj #1 (accountant, kelvin, incomplete), foundations of pm 
(1,	'COURSE3'),  -- lj #1 (accountant, kelvin, incomplete), accounting fundamentals
(2,	'COURSE2'),  -- lj #2 (PM, jann, incomplete), foundations of pm
(2,	'COURSE4'),  -- lj #2 (PM, jann, incomplete), wr
(3,	'COURSE1'),  -- lj #3 (accountant, jann, incomplete), business strat
(3,	'COURSE3'),  -- lj #3 (accountant, jann, incomplete), foundations of pm 
(4,	'COURSE5'),  -- lj #4 (uiux, dom, incomplete), uiux
(4,	'COURSE6');  -- lj #4 (uiux, dom, incomplete), biz value w ux 

-- --------------------------------------------------------

-- 

Import data for table `courses`

show global variables like 'local_infile';
set global local_infile=true;

LOAD DATA INFILE 
'C:/wamp64/www/SPMG5T6/RawData/courses.csv' 
INTO TABLE course
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES; 

-- 

Import data for table `role`

show global variables like 'local_infile';
set global local_infile=true;

LOAD DATA INFILE 
'C:/wamp64/www/SPMG5T6/RawData/role.csv' 
INTO TABLE role
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES; 

-- 

Import data for table `registration`

show global variables like 'local_infile';
set global local_infile=true;

LOAD DATA INFILE 
'C:/wamp64/www/SPMG5T6/RawData/registration.csv' 
INTO TABLE role
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES; 

-- 

Import data for table `staff`

show global variables like 'local_infile';
set global local_infile=true;

LOAD DATA INFILE 
'C:/wamp64/www/SPMG5T6/RawData/staff.csv' 
INTO TABLE staff
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES; 

-- 