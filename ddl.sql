-- Create SQL script for PostgreSQL

-- Drop tables if they exist to allow re-running the script cleanly
DROP TABLE IF EXISTS TrainingSessions, Members, Trainers, Rooms, Equipment CASCADE;

-- Table creation for 'Members'
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    HealthInfo TEXT,
    FitnessGoals TEXT
);

-- Table creation for 'Trainers'
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Specialization TEXT,
    AvailableTimes VARCHAR(255)
);

-- Table creation for 'Rooms'
CREATE TABLE Rooms (
    RoomID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Capacity INT CHECK (Capacity > 0)
);

-- Table creation for 'Equipment'
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    MaintenanceSchedule DATE,
    IsAvailable BOOLEAN DEFAULT TRUE
);

-- Table creation for 'TrainingSessions'
CREATE TABLE TrainingSessions (
    SessionID SERIAL PRIMARY KEY,
    MemberID INT NOT NULL,
    TrainerID INT NOT NULL,
    SessionTime TIMESTAMP NOT NULL,
    Duration INTERVAL DEFAULT '1 hour',
    RoomID INT,
    CONSTRAINT FK_MemberID FOREIGN KEY (MemberID) REFERENCES Members (MemberID),
    CONSTRAINT FK_TrainerSessionID FOREIGN KEY (TrainerID) REFERENCES Trainers (TrainerID),
    CONSTRAINT FK_SessionRoomID FOREIGN KEY (RoomID) REFERENCES Rooms (RoomID),
    CONSTRAINT session_time_check CHECK (Duration > '0 hours')
);

-- Optionally, create indexes for frequently accessed fields
CREATE INDEX idx_member_email ON Members (Email);
CREATE INDEX idx_trainer_name ON Trainers (Name);
CREATE INDEX idx_room_name ON Rooms (Name);