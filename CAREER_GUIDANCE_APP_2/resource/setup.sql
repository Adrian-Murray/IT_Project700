-- Create Users Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, -- Ensure passwords are hashed before storing
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    mobile_number TEXT NOT NULL CHECK (mobile_number GLOB '+[0-9]*'),
    date_of_birth TEXT NOT NULL CHECK (date_of_birth < date('now')),
    education_level TEXT NOT NULL
);

-- Create PersonalityTestQuestions Table
CREATE TABLE PersonalityTestQuestions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('E', 'I', 'S', 'N', 'T', 'F', 'J', 'P')), -- E=Extroversion, I=Introversion, etc.
    question_type TEXT NOT NULL CHECK (question_type IN ('yes_no', 'multiple_choice')),
);

-- Create PersonalityTestResults Table
CREATE TABLE PersonalityTestResults (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    question_id INTEGER,
    answer TEXT NOT NULL, -- Store the answer (e.g., 'E' or 'I')
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (question_id) REFERENCES PersonalityTestQuestions(question_id)
);

-- Create PersonalityTestScores Table
CREATE TABLE PersonalityTestScores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category TEXT NOT NULL CHECK (category IN ('E', 'I', 'S', 'N', 'T', 'F', 'J', 'P')),
    score INTEGER NOT NULL DEFAULT 0, -- Track score for each category
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create JobFields Table
CREATE TABLE JobFields (
    job_field_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_field_name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Create Courses Table
CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    description TEXT NOT NULL,
    required_education_level TEXT NOT NULL,
    job_field_id INTEGER,
    FOREIGN KEY (job_field_id) REFERENCES JobFields(job_field_id)
);

-- Create Schools Table
CREATE TABLE Schools (
    school_id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT NOT NULL,
    location TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Create SchoolSubjects Table
CREATE TABLE SchoolSubjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id INTEGER,
    subject_name TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (school_id) REFERENCES Schools(school_id)
);

-- Create JobFieldMatches Table
CREATE TABLE JobFieldMatches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id INTEGER,
    job_field_id INTEGER,
    match_score REAL NOT NULL,
    FOREIGN KEY (result_id) REFERENCES PersonalityTestResults(result_id),
    FOREIGN KEY (job_field_id) REFERENCES JobFields(job_field_id)
);

-- Create ChatbotMessages Table
CREATE TABLE ChatbotMessages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create SupportTickets Table
CREATE TABLE SupportTickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    issue TEXT NOT NULL,
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'closed', 'pending')),
    timestamp TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create CVs Table
CREATE TABLE CVs (
    cv_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    cv_content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create UserPreferences Table
CREATE TABLE UserPreferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    preference_type TEXT NOT NULL,
    preference_value TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create CourseEnrollments Table
CREATE TABLE CourseEnrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    course_id INTEGER,
    enrolled_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Create UserFeedback Table
CREATE TABLE UserFeedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    feedback TEXT NOT NULL,
    submitted_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Notifications Table
CREATE TABLE Notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT NOT NULL,
    sent_at TEXT DEFAULT (datetime('now', 'localtime')),
    status TEXT DEFAULT 'unread' CHECK (status IN ('unread', 'read')),
    notification_type TEXT DEFAULT 'general' CHECK (notification_type IN ('general', 'alert', 'reminder')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Roles Table
CREATE TABLE Roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

-- Create UserRoles Table
CREATE TABLE UserRoles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    role_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

-- Insert predefined roles
INSERT INTO Roles (role_name) VALUES 
('Database Admin'), 
('Course Uploader'), 
('Support'), 
('Linux Admin'), 
('User');

-- Create Audit Log Table
CREATE TABLE AuditLog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action_type TEXT NOT NULL,
    action_details TEXT NOT NULL,
    action_timestamp TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Indexing for performance optimization
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_courses_name ON Courses(course_name);
CREATE INDEX idx_personality_results_userid ON PersonalityTestResults(user_id);
CREATE INDEX idx_jobfieldmatches_userid ON JobFieldMatches(result_id);

-- Triggers and Functions

-- Trigger Function to create personality test results
CREATE TRIGGER after_user_insert
AFTER INSERT ON Users
FOR EACH ROW
BEGIN
    -- Create empty test results
    INSERT INTO PersonalityTestResults (user_id, question_id, answer)
    SELECT NEW.user_id, question_id, ''
    FROM PersonalityTestQuestions;

    -- Initialize user's test scores for each category
    INSERT INTO PersonalityTestScores (user_id, category)
    VALUES 
    (NEW.user_id, 'E'), (NEW.user_id, 'I'),
    (NEW.user_id, 'S'), (NEW.user_id, 'N'),
    (NEW.user_id, 'T'), (NEW.user_id, 'F'),
    (NEW.user_id, 'J'), (NEW.user_id, 'P');
END;

-- Trigger Function to create CV automatically
CREATE TRIGGER after_user_insert_cv
AFTER INSERT ON Users
FOR EACH ROW
BEGIN
    INSERT INTO CVs (user_id, cv_content)
    VALUES (NEW.user_id, 
            'Name: ' || NEW.name || ' ' || NEW.surname || '\n' ||
            'Email: ' || NEW.email || '\n' ||
            'Mobile: ' || NEW.mobile_number || '\n' ||
            'Date of Birth: ' || NEW.date_of_birth || '\n' ||
            'Education Level: ' || NEW.education_level);
END;

-- Trigger Function to log user updates
CREATE TRIGGER trg_log_user_update
AFTER UPDATE ON Users
FOR EACH ROW
BEGIN
    INSERT INTO AuditLog (user_id, action_type, action_details)
    VALUES (NEW.user_id, 'UPDATE', 'User details updated');
END;


CREATE TABLE IF NOT EXISTS TempPersonalityTestResults (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    answer TEXT NOT NULL CHECK (answer IN ('E', 'I', 'S', 'N', 'T', 'F', 'J', 'P')),  -- Ensure valid answer types
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Record when the answer is submitted
    UNIQUE (user_id, question_id),  -- Ensure each user answers each question only once
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES PersonalityTestQuestions(question_id) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS cleanup_temp_results
AFTER INSERT ON PersonalityTestScores
FOR EACH ROW
BEGIN
    -- Delete all temporary results for the user
    DELETE FROM TempPersonalityTestResults WHERE user_id = NEW.user_id;
END;

CREATE TRIGGER IF NOT EXISTS log_temp_submission
AFTER INSERT ON TempPersonalityTestResults
FOR EACH ROW
BEGIN
    -- Insert a log entry for each answer submitted
    INSERT INTO AuditLog (user_id, action_type, action_details, action_timestamp)
    VALUES (NEW.user_id, 'SUBMIT_ANSWER', 'Question ' || NEW.question_id || ' answered with ' || NEW.answer, CURRENT_TIMESTAMP);
END;


CREATE TRIGGER IF NOT EXISTS complete_personality_test
AFTER INSERT ON TempPersonalityTestResults
FOR EACH ROW
WHEN (SELECT COUNT(*) FROM TempPersonalityTestResults WHERE user_id = NEW.user_id) = (SELECT COUNT(*) FROM PersonalityTestQuestions)
BEGIN
    -- Calculate and store the results in PersonalityTestScores
    INSERT INTO PersonalityTestScores (user_id, category, score)
    SELECT user_id, answer AS category, COUNT(answer) AS score
    FROM TempPersonalityTestResults
    WHERE user_id = NEW.user_id
    GROUP BY answer;

    -- Clean up the temporary results for the user
    DELETE FROM TempPersonalityTestResults WHERE user_id = NEW.user_id;
END;

CREATE TABLE IF NOT EXISTS PersonalityTestAnswers (
    answer_id INTEGER PRIMARY KEY,
    answer_text TEXT NOT NULL,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES PersonalityTestQuestions(id) ON DELETE CASCADE,
    CHECK (answer_id > 0),
    CHECK (question_id > 0)
);

CREATE INDEX idx_temp_results_user_id ON TempPersonalityTestResults(user_id);
CREATE INDEX idx_temp_results_question_id ON TempPersonalityTestResults(question_id);
