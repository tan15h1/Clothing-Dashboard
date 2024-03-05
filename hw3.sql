/***
DS 3500 Spring 2024
filename: hw3.sql
HW 3: Dashboards
Kaydence Lin and Tanishi Datta
***/

-- create database
CREATE DATABASE IF NOT EXISTS clothes;
USE clothes;

-- create table
CREATE TABLE IF NOT EXISTS clothing(
	id INT PRIMARY KEY AUTO_INCREMENT,
    brand TEXT,
    category TEXT,
    color TEXT,
    size TEXT,
    material TEXT,
    price DECIMAL (10,2) );
	
-- select all
SELECT * FROM clothing