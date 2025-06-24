CREATE DATABASE sensors;
USE sensors;

CREATE TABLE measurements (
    timestamp DATETIME,
    node_id INT,
    count INT PRIMARY KEY,
    temperature DOUBLE,
    humidity DOUBLE
);