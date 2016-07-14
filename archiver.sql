-- MySQL Script generated by MySQL Workbench
-- Thu 14 Jul 2016 04:11:40 PM CEST
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema chan
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema chan
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `chan` DEFAULT CHARACTER SET utf8 ;
USE `chan` ;

-- -----------------------------------------------------
-- Table `chan`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`category` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `nsfw` TINYINT(1) UNSIGNED NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`board`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`board` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `keywords` VARCHAR(255) NULL,
  `description` VARCHAR(255) NULL,
  `url` VARCHAR(12) NOT NULL,
  `category_ID` INT(11) UNSIGNED NOT NULL,
  `posts_shown` TINYINT(1) UNSIGNED NOT NULL,
  `posting_enabled` TINYINT(1) NULL DEFAULT 0,
  PRIMARY KEY (`ID`),
  INDEX `fk_board_category_idx` (`category_ID` ASC),
  UNIQUE INDEX `category_ID_UNIQUE` (`category_ID` ASC),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC),
  CONSTRAINT `fk_board_category`
    FOREIGN KEY (`category_ID`)
    REFERENCES `chan`.`category` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`thread`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`thread` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `board_ID` INT(11) UNSIGNED NOT NULL,
  `sticky` TINYINT(1) UNSIGNED NULL,
  `closed` TINYINT(1) UNSIGNED NULL,
  `archived` TINYINT(1) UNSIGNED NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_thread_board1_idx` (`board_ID` ASC),
  CONSTRAINT `fk_thread_board1`
    FOREIGN KEY (`board_ID`)
    REFERENCES `chan`.`board` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`image` (
  `ID` INT(13) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` TEXT NOT NULL,
  `name_original` TEXT NOT NULL,
  `extension` VARCHAR(5) NOT NULL,
  `size` INT(8) NOT NULL,
  `md5` VARCHAR(32) NOT NULL,
  `width` INT(5) NOT NULL,
  `height` INT(5) NOT NULL,
  `thumbnail_width` INT(3) NOT NULL,
  `thumbnail_height` INT(3) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`rank`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`rank` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `capcode` VARCHAR(12) NOT NULL,
  `display_name` VARCHAR(12) NULL,
  `rank` INT(4) UNSIGNED NOT NULL DEFAULT 1000,
  `colour` VARCHAR(45) NULL,
  `image` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`post` (
  `ID` INT(13) UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` INT(13) UNSIGNED NOT NULL,
  `poster_id` TEXT NULL,
  `rank_ID` INT(11) UNSIGNED NULL,
  `name` TEXT NOT NULL,
  `tripcode` TEXT NULL,
  `subject` TEXT NULL,
  `html_comment` TEXT NOT NULL,
  `text_comment` TEXT NOT NULL,
  `timestamp` INT(10) UNSIGNED NOT NULL,
  `image_ID` INT(13) UNSIGNED NULL,
  `file_deleted` TINYINT(1) NULL,
  `spoiler` TINYINT(1) NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_post_image1_idx` (`image_ID` ASC),
  INDEX `fk_post_rank1_idx` (`rank_ID` ASC),
  CONSTRAINT `fk_post_image1`
    FOREIGN KEY (`image_ID`)
    REFERENCES `chan`.`image` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_rank1`
    FOREIGN KEY (`rank_ID`)
    REFERENCES `chan`.`rank` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`thread_post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`thread_post` (
  `ID` INT(13) UNSIGNED NOT NULL AUTO_INCREMENT,
  `thread_ID` INT(11) UNSIGNED NOT NULL,
  `post_ID` INT(13) UNSIGNED NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_thread_post_thread1_idx` (`thread_ID` ASC),
  INDEX `fk_thread_post_post1_idx` (`post_ID` ASC),
  CONSTRAINT `fk_thread_post_thread1`
    FOREIGN KEY (`thread_ID`)
    REFERENCES `chan`.`thread` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_thread_post_post1`
    FOREIGN KEY (`post_ID`)
    REFERENCES `chan`.`post` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`que`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`que` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `thread_post_ID` INT(13) UNSIGNED NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_que_thread_post1_idx` (`thread_post_ID` ASC),
  CONSTRAINT `fk_que_thread_post1`
    FOREIGN KEY (`thread_post_ID`)
    REFERENCES `chan`.`thread_post` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`tag` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`image_tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`image_tag` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `image_ID` INT(13) UNSIGNED NOT NULL,
  `tag_ID` INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_image_tag_image1_idx` (`image_ID` ASC),
  INDEX `fk_image_tag_tag1_idx` (`tag_ID` ASC),
  CONSTRAINT `fk_image_tag_image1`
    FOREIGN KEY (`image_ID`)
    REFERENCES `chan`.`image` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_image_tag_tag1`
    FOREIGN KEY (`tag_ID`)
    REFERENCES `chan`.`tag` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chan`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chan`.`user` (
  `ID` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(64) NULL,
  `salt` VARCHAR(64) NOT NULL,
  `rank_ID` INT(11) NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  INDEX `fk_user_rank1_idx` (`rank_ID` ASC),
  CONSTRAINT `fk_user_rank1`
    FOREIGN KEY (`rank_ID`)
    REFERENCES `chan`.`rank` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
