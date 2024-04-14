-- Insert sample data into the Members table
INSERT INTO Members (Username, Email, Password, HealthInfo, FitnessGoals)
VALUES
('john_doe', 'john.doe@example.com', 'password123', 'No known allergies.', 'Increase muscle mass.'),
('jane_smith', 'jane.smith@example.com', 'password456', 'Asthmatic. Uses inhaler.', 'Lose weight and improve stamina.');

-- Insert sample data into the Trainers table
INSERT INTO Trainers (Name, Specialization, AvailableTimes)
VALUES
('Alice Johnson', 'Yoga, Pilates', 'Weekdays: 8 AM - 4 PM'),
('Bob Richards', 'Weightlifting, Cardio', 'Weekdays: 12 PM - 8 PM');

-- Insert sample data into the Rooms table
INSERT INTO Rooms (Name, Capacity)
VALUES
('Yoga Studio', 15),
('Weight Room', 10);

-- Insert sample data into the Equipment table
INSERT INTO Equipment (Name, MaintenanceSchedule, IsAvailable)
VALUES
('Treadmill', '2023-12-15', TRUE),
('Yoga Mats', NULL, TRUE);

-- Insert sample data into the TrainingSessions table
INSERT INTO TrainingSessions (MemberID, TrainerID, SessionTime, Duration, RoomID)
VALUES
(1, 1, '2023-04-01 09:00:00', '1 hour', 1),
(2, 2, '2023-04-01 10:00:00', '2 hours', 2);

-- Optionally, update indexes after insertion for better performance
REINDEX TABLE Members;
REINDEX TABLE Trainers;
REINDEX TABLE Rooms;