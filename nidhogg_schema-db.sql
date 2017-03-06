-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema Nidhogg
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Nidhogg
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Nidhogg` ;
USE `Nidhogg` ;

-- -----------------------------------------------------
-- Table `Nidhogg`.`Client`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Nidhogg`.`Client` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(6) NOT NULL,
  `name` VARCHAR(128) NOT NULL DEFAULT '',
  `install` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `code_UNIQUE` (`code` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Nidhogg`.`NicConfig`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Nidhogg`.`NicConfig` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Client_id` INT NOT NULL,
  `date` TIMESTAMP NOT NULL,
  `mac` VARCHAR(17) NOT NULL,
  `ip` VARCHAR(15) NULL,
  `subnet` VARCHAR(15) NULL,
  `gateway` VARCHAR(15) NULL,
  `dns` VARCHAR(15) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_NicConfig_Client1`
    FOREIGN KEY (`Client_id`)
    REFERENCES `Nidhogg`.`Client` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Nidhogg`.`Qinfo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Nidhogg`.`Qinfo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Client_id` INT NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cpu` INT NULL,
  `ram` INT NULL,
  `hdd` INT NULL,
  UNIQUE INDEX `date_UNIQUE` (`date` ASC),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_Qinfo_Client`
    FOREIGN KEY (`Client_id`)
    REFERENCES `Nidhogg`.`Client` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Nidhogg`.`table1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Nidhogg`.`table1` (
  `id` INT NOT NULL,
  `date` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
