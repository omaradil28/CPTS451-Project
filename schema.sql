-- WSU Lab Connect: Database Schema

-- WSU Lab Connect: Database Schema

-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS lab_booking;
USE lab_booking;

-- Table: users
-- Stores profile and credentials for researchers and technicians.
CREATE TABLE users (
    user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL,
    CHECK (role IN ('student', 'technician'))
);

-- Table: equipment
-- Tracks lab assets and operational status
CREATE TABLE equipment (
    equipment_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(10) DEFAULT 'available',
    CHECK (status IN ('available', 'repair'))
);

-- Table: reservations
-- Manages the scheduling of equipment
CREATE TABLE reservations (
    reservation_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id INT,
    equipment_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(10) DEFAULT 'active',

    CONSTRAINT chk_time_order CHECK (end_time > start_time),
    CONSTRAINT chk_res_status CHECK (status IN ('active', 'cancelled', 'completed')),

    CONSTRAINT fk_res_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL,

    CONSTRAINT fk_res_equipment
        FOREIGN KEY (equipment_id)
        REFERENCES equipment(equipment_id)
        ON DELETE CASCADE
);

-- Table: usage_logs
-- Keeps users accountable by logging usage and equipment condition.
CREATE TABLE usage_logs (
    log_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    notes VARCHAR(1000) NULL,

    CONSTRAINT fk_log_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES reservations(reservation_id)
        ON DELETE CASCADE
);

-- Table: waitlist
-- Manages users waiting for equipment that is occupied.
CREATE TABLE waitlist (
    waitlist_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_wait_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_wait_equipment
        FOREIGN KEY (equipment_id)
        REFERENCES equipment(equipment_id)
        ON DELETE CASCADE
);

-- Seed Data (to start off)
INSERT INTO equipment (name, status) VALUES 
('Centrifuge', 'available'),
('Mass Spectrometer', 'repair'),
('PCR Machine', 'available'),
('Scanning Electron Microscope', 'available');
