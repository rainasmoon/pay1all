drop database if exists online_db;

CREATE DATABASE IF NOT EXISTS online_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON online_db.* TO pc@localhost IDENTIFIED BY 'pc';