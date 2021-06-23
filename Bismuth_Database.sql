-- BEGIN TABLE User
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `userID` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `jobType` varchar(255) NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `Un_User` (`userID`,`email`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE User



-- BEGIN TABLE Leader
DROP TABLE IF EXISTS Leader;
CREATE TABLE `Leader` (
  `leaderID` int unsigned NOT NULL,
  PRIMARY KEY (`leaderID`),
  UNIQUE KEY `Un_leaderID` (`leaderID`),
  CONSTRAINT `leaderID` FOREIGN KEY (`leaderID`) REFERENCES `User` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE Leader

-- BEGIN TABLE FieldGeologist
DROP TABLE IF EXISTS FieldGeologist;
CREATE TABLE `FieldGeologist` (
  `fieldGeologistID` int unsigned NOT NULL,
  `availability` varchar(255) NOT NULL DEFAULT 'True',
  PRIMARY KEY (`fieldGeologistID`),
  UNIQUE KEY `Un_FieldGeologist` (`fieldGeologistID`),
  CONSTRAINT `fieldgeologist` FOREIGN KEY (`fieldGeologistID`) REFERENCES `User` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE FieldGeologist


-- BEGIN TABLE Project_details
DROP TABLE IF EXISTS Project_details;
CREATE TABLE `Project_details` (
  `projectName` varchar(255) NOT NULL DEFAULT '',
  `programName` varchar(255) NOT NULL DEFAULT '',
  `departmentName` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`projectName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE Project_details


-- BEGIN TABLE Task
DROP TABLE IF EXISTS Task;
CREATE TABLE `Task` (
  `taskID` int unsigned NOT NULL AUTO_INCREMENT,
  `taskName` varchar(255) NOT NULL,
  `objectives` varchar(255) DEFAULT '',
  `summary` varchar(255) DEFAULT '',
  `report_path` varchar(255) DEFAULT '',
  `status` varchar(10) NOT NULL DEFAULT 'Upcoming',
  `leaderID` int unsigned NOT NULL,
  `internalSupport` varchar(255) NOT NULL DEFAULT '',
  `externalSupport` varchar(255) NOT NULL DEFAULT '',
  `deliverables` varchar(255) NOT NULL DEFAULT '',
  `projectName` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`taskID`),
  UNIQUE KEY `Un_taskID` (`taskID`),
  KEY `LeaderFK` (`leaderID`),
  KEY `projectNameFK` (`projectName`),
  CONSTRAINT `LeaderFK` FOREIGN KEY (`leaderID`) REFERENCES `Leader` (`leaderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `projectNameFK` FOREIGN KEY (`projectName`) REFERENCES `Project_details` (`projectName`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE Task





-- BEGIN TABLE FieldGeologist_Task
DROP TABLE IF EXISTS FieldGeologist_Task;
CREATE TABLE `FieldGeologist_Task` (
  `fieldGeologistID` int unsigned NOT NULL,
  `taskID` int unsigned NOT NULL,
  PRIMARY KEY (`fieldGeologistID`,`taskID`),
  CONSTRAINT `FGid` FOREIGN KEY (`fieldGeologistID`) REFERENCES `FieldGeologist` (`fieldGeologistID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE FieldGeologist_Task



-- BEGIN TABLE Record
DROP TABLE IF EXISTS Record;
CREATE TABLE `Record` (
  `recordID` int unsigned NOT NULL AUTO_INCREMENT,
  `siteName` varchar(255) NOT NULL DEFAULT '',
  `stream` varchar(255) NOT NULL DEFAULT '',
  `city` varchar(255) NOT NULL DEFAULT '',
  `date` varchar(255) DEFAULT NULL,
  `remark` varchar(255) NOT NULL DEFAULT '',
  `EC` double DEFAULT NULL,
  `temp` double DEFAULT NULL,
  `pH` double DEFAULT NULL,
  `EH` double DEFAULT NULL,
  `taskID` int unsigned DEFAULT NULL,
  `fieldGeologistID` int unsigned DEFAULT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  PRIMARY KEY (`recordID`),
  KEY `TaskID_FK` (`taskID`),
  KEY `fieldGeologist_FK` (`fieldGeologistID`),
  CONSTRAINT `fieldGeologist_FK` FOREIGN KEY (`fieldGeologistID`) REFERENCES `FieldGeologist` (`fieldGeologistID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `TaskID_FK` FOREIGN KEY (`taskID`) REFERENCES `Task` (`taskID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE Record



-- BEGIN TABLE Image
DROP TABLE IF EXISTS Image;
CREATE TABLE `Image` (
  `imageID` int unsigned NOT NULL AUTO_INCREMENT,
  `imageType` varchar(255) NOT NULL,
  `imagePath` varchar(255) NOT NULL DEFAULT '',
  `recordID` int unsigned NOT NULL,
  PRIMARY KEY (`imageID`),
  KEY `recordID_FK` (`recordID`),
  CONSTRAINT `recordID_FK` FOREIGN KEY (`recordID`) REFERENCES `Record` (`recordID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- END TABLE Image