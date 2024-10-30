-- Creating PersonalityTestAnswers Table
CREATE TABLE PersonalityTestAnswers (
    answer_id INT PRIMARY KEY AUTO_INCREMENT,
    answer_text VARCHAR(255) NOT NULL,
    question_id INT,
    FOREIGN KEY (question_id) REFERENCES PersonalityTestQuestions(question_id)
);