/*
File: schema.sql
Author: Erisa Halipaj
Date: 19/01/2025

Description: Defines the database schema for the authentication microservice.
Currently, it includes the 'users' table.
*/
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);