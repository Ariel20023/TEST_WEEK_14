CREATE DATABASE IF NOT EXISTS weapon;

USE weapon;

CREATE TABLE IF NOT EXISTS weapon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    weapon_id VARCHAR(20) NOT NULL,
    weapon_name VARCHAR(50) NOT NULL,
    weapon_type VARCHAR(50) NOT NULL,
    range_km  INT NOT NULL,
    weight_kg FLOAT NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    origin_country VARCHAR(50) NOT NULL,
    storage_location VARCHAR(50) NOT NULL,
    year_estimated INT NOT NULL,
    risk_level VARCHAR(50) NOT NULL
);


