-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 2015-09-18 14:47:41
-- 服务器版本： 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `dbfp`
--
CREATE DATABASE IF NOT EXISTS `dbfp` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `dbfp`;

-- --------------------------------------------------------

--
-- 表的结构 `dbfp_av_info`
--

DROP TABLE IF EXISTS `dbfp_av_info`;
CREATE TABLE IF NOT EXISTS `dbfp_av_info` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `av` int(8) NOT NULL,
  `title` char(200) NOT NULL,
  `up_id` int(10) unsigned DEFAULT NULL,
  `create_stamp` timestamp NOT NULL,
  `create_at` datetime NOT NULL,
  `play_times` int(11) NOT NULL,
  `collect_times` int(11) NOT NULL,
  `dan_count` int(11) NOT NULL,
  `review_times` int(11) NOT NULL,
  `coins_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `up_id` (`up_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `dbfp_av_tag`
--

DROP TABLE IF EXISTS `dbfp_av_tag`;
CREATE TABLE IF NOT EXISTS `dbfp_av_tag` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `av_id` int(10) unsigned NOT NULL,
  `tag_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `av_id` (`av_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `dbfp_tag`
--

DROP TABLE IF EXISTS `dbfp_tag`;
CREATE TABLE IF NOT EXISTS `dbfp_tag` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `dbfp_up_info`
--

DROP TABLE IF EXISTS `dbfp_up_info`;
CREATE TABLE IF NOT EXISTS `dbfp_up_info` (
  `uid` int(8) unsigned NOT NULL ,
  `name` varchar(40) NOT NULL,
  `lvl` tinyint(4) NOT NULL,
  `sign` char(200) DEFAULT NULL,
  `birth` date NOT NULL,
  `reg_date` date NOT NULL,
  `article` int(5) NOT NULL,
  `follow_count` int(11) NOT NULL,
  `fans_count` int(11) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- 限制导出的表
--

--
-- 限制表 `dbfp_av_info`
--
ALTER TABLE `dbfp_av_info`
  ADD CONSTRAINT `dbfp_av_info_ibfk_1` FOREIGN KEY (`up_id`) REFERENCES `dbfp_up_info` (`uid`);

--
-- 限制表 `dbfp_av_tag`
--
ALTER TABLE `dbfp_av_tag`
  ADD CONSTRAINT `dbfp_av_tag_ibfk_1` FOREIGN KEY (`av_id`) REFERENCES `dbfp_av_info` (`id`),
  ADD CONSTRAINT `dbfp_av_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `dbfp_tag` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
