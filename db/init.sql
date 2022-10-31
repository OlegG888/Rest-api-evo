CREATE DATABASE csvdata;
use csvdata;



CREATE TABLE `finance` (
  `TransactionId` int(10) NOT NULL,
  `RequestId` int(10) NOT NULL,
  `TerminalId` int(10) NOT NULL,
  `PartnerObjectId` int(10) NOT NULL,
  `AmountTotal` int(10) NOT NULL,
  `AmountOriginal` int(10) NOT NULL,
  `CommissionPS` float NOT NULL,
  `CommissionClient` float NOT NULL,
  `CommissionProvider` float NOT NULL,
  `DateInput` date NOT NULL,
  `DatePost` date NOT NULL,
  `Status` varchar(100) NOT NULL,
  `PaymentType` varchar(100) NOT NULL,
  `PaymentNumber` varchar(100) NOT NULL,
  `ServiceId` int(20) NOT NULL,
  `Service` varchar(100) NOT NULL,
  `PayeeId` int(20) NOT NULL,
  `PayeeName` varchar(100) NOT NULL,
  `PayeeBankMfo` int(20) NOT NULL,
  `PayeeBankAccount` varchar(100) NOT NULL,
  `PaymentNarrative` varchar(250) NOT NULL,
   PRIMARY KEY (`TransactionId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert  into `finance`(`TransactionId`,`RequestId`,`TerminalId`,`PartnerObjectId`,`AmountTotal`) values
(1,'20020', '3506', '1111', '1.00', '1.00', '0.00', '0.00', '0.00', '2022-08-12 11:25:27', '2022-08-12 14:25:27', 'accepted', 'cash', 'PS16698205', '13980', 'Поповнення карток', '14232155', 'pumb', '254751', 'UA713451373919523', 'Перерахування коштів згідно договору про надання послуг А11/27122 від 19.11.2020 р.' ),