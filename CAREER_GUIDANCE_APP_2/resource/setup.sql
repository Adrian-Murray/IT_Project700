-- Table for Personality Test Questions
CREATE TABLE PersonalityTestQuestions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL CHECK (question_type IN ('yes_no', 'multiple_choice'))
);

-- Table for storing the results of personality tests taken by users
CREATE TABLE PersonalityTestResults (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    question_id INTEGER,
    answer TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (question_id) REFERENCES PersonalityTestQuestions(question_id)
);

-- Table for Job Fields
CREATE TABLE JobFields (
    job_field_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_field_name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Table for Courses
CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    description TEXT NOT NULL,
    required_education_level TEXT NOT NULL,
    job_field_id INTEGER,
    FOREIGN KEY (job_field_id) REFERENCES JobFields(job_field_id)
);

-- Table for Schools
CREATE TABLE Schools (
    school_id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT NOT NULL,
    location TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Table for Subjects offered by Schools
CREATE TABLE SchoolSubjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id INTEGER,
    subject_name TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (school_id) REFERENCES Schools(school_id)
);

-- Table to match users' personality test results with job fields
CREATE TABLE JobFieldMatches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id INTEGER,
    job_field_id INTEGER,
    match_score REAL NOT NULL,
    FOREIGN KEY (result_id) REFERENCES PersonalityTestResults(result_id),
    FOREIGN KEY (job_field_id) REFERENCES JobFields(job_field_id)
);

-- Table for storing messages in the chatbot
CREATE TABLE ChatbotMessages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table for user support tickets
CREATE TABLE SupportTickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    issue TEXT NOT NULL,
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'closed', 'pending')),
    timestamp TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table for user CVs
CREATE TABLE CVs (
    cv_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    cv_content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table for user preferences
CREATE TABLE UserPreferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    preference_type TEXT NOT NULL,
    preference_value TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table for course enrollments by users
CREATE TABLE CourseEnrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    course_id INTEGER,
    enrolled_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Table for user feedback
CREATE TABLE UserFeedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    feedback TEXT NOT NULL,
    submitted_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table for notifications sent to users
CREATE TABLE Notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT NOT NULL,
    sent_at TEXT DEFAULT (datetime('now', 'localtime')),
    status TEXT DEFAULT 'unread' CHECK (status IN ('unread', 'read')),
    notification_type TEXT DEFAULT 'general' CHECK (notification_type IN ('general', 'alert', 'reminder')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table for user roles
CREATE TABLE Roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

-- Table linking users to their roles
CREATE TABLE UserRoles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    role_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

-- Table for logging user actions
CREATE TABLE AuditLog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action_type TEXT NOT NULL,
    action_details TEXT NOT NULL,
    action_timestamp TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Index for fast searches in Courses table
CREATE INDEX idx_courses_name ON Courses(course_name);

-- Index for fast searches in JobFieldMatches table
CREATE INDEX idx_jobfieldmatches_userid ON JobFieldMatches(result_id);

-- Table for storing personality test answers
CREATE TABLE PersonalityTestAnswers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer_text TEXT NOT NULL,
    question_id INTEGER,
    answer_value INTEGER,
    category TEXT,
    FOREIGN KEY (question_id) REFERENCES PersonalityTestQuestions(question_id)
);

-- Table for user information
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, -- Ensure passwords are hashed before storing
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    mobile_number TEXT NOT NULL CHECK (
        mobile_number GLOB '+[0-9]*' OR mobile_number GLOB '[0-9]*'
    ),
    date_of_birth TEXT NOT NULL, 
    education_level TEXT NOT NULL
);

-- Table for storing personality test scores for users
CREATE TABLE PersonalityTestScores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    E INTEGER NOT NULL DEFAULT 0,
    I INTEGER NOT NULL DEFAULT 0,
    S INTEGER NOT NULL DEFAULT 0,
    N INTEGER NOT NULL DEFAULT 0,
    T INTEGER NOT NULL DEFAULT 0,
    F INTEGER NOT NULL DEFAULT 0,
    J INTEGER NOT NULL DEFAULT 0,
    P INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Table for storing user personality types
CREATE TABLE user_personality_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, 
    primary_personality_type VARCHAR NOT NULL, 
    alternative_1 VARCHAR, 
    alternative_2 VARCHAR, 
    alternative_3 VARCHAR, 
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);


CREATE TABLE UserSkills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    skill_name TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE UserHobbies (
    hobby_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    hobby_name TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
CREATE TABLE Skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT UNIQUE
);

CREATE TABLE Hobbies (
    hobby_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hobby_name TEXT UNIQUE
);
