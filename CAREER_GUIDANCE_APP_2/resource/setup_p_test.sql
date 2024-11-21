-- Insert Personality Test Questions into PersonalityTestQuestions Table

-- Extroversion vs Introversion (E vs I)
INSERT INTO PersonalityTestQuestions (question_text, category, question_type)
VALUES
('In a social gathering, do you feel more energized by interacting with a large group of people or by having one-on-one conversations?', 'E', 'multiple_choice'),
('How do you typically recharge after a busy day?', 'E', 'multiple_choice'),
('When facing a challenge, do you prefer brainstorming ideas with others or working through it independently?', 'E', 'multiple_choice'),
('In your free time, do you find yourself seeking out social events and gatherings or enjoying quieter activities at home?', 'E', 'multiple_choice'),
('How do you feel about small talk?', 'E', 'multiple_choice'),
('When making decisions, do you rely more on your own instincts and feelings or seek input from others?', 'I', 'multiple_choice'),
('How do you handle new and unfamiliar situations?', 'I', 'multiple_choice'),
('In a work or team setting, do you prefer open office spaces and collaboration or individual workspaces?', 'I', 'multiple_choice'),
('How do you typically respond to being the focal point in a group setting?', 'I', 'multiple_choice'),
('When planning a weekend, do you lean towards social plans with friends or quiet time for yourself?', 'I', 'multiple_choice'),
('When meeting new people, are you more likely to initiate conversations and introductions or wait for others to approach you?', 'E', 'multiple_choice');

-- Sensing vs Intuition (S vs N)
INSERT INTO PersonalityTestQuestions (question_text, category, question_type)
VALUES
('When faced with a problem, do you prefer to rely on concrete facts and details or explore possibilities and potential meanings?', 'S', 'multiple_choice'),
('How do you approach new information or learning?', 'N', 'multiple_choice'),
('In a conversation, are you more focused on the present and current details or on future possibilities and patterns?', 'N', 'multiple_choice'),
('When planning a trip, do you prefer to have a detailed itinerary and clear schedule or leave room for spontaneous experiences and changes?', 'S', 'multiple_choice'),
('How do you make decisions?', 'N', 'multiple_choice'),
('When working on a project, do you tend to focus on the specific tasks at hand or the overall vision and goals?', 'S', 'multiple_choice'),
('In a group discussion, do you prefer to stick to the facts and details or contribute ideas and theories?', 'S', 'multiple_choice'),
('How do you handle unexpected changes or disruptions to your plans?', 'N', 'multiple_choice'),
('When recalling a past event, do you focus more on the specific details and occurrences or the overall impressions and meanings?', 'N', 'multiple_choice'),
('When reading a book or watching a movie, do you pay close attention to the plot and events or look for deeper meanings and symbolism?', 'N', 'multiple_choice'),
('How do you prefer to receive information?', 'S', 'multiple_choice'),
('When faced with a decision, do you rely more on your past experiences and proven methods or seek out innovative and creative solutions?', 'S', 'multiple_choice'),
('In a brainstorming session, do you tend to come up with practical, actionable ideas or imaginative, out-of-the-box concepts?', 'N', 'multiple_choice'),
('How do you approach problem-solving?', 'S', 'multiple_choice');

-- Judging vs Perceiving (J vs P)
INSERT INTO PersonalityTestQuestions (question_text, category, question_type)
VALUES
('How do you feel about making plans and sticking to a schedule?', 'J', 'multiple_choice'),
('When starting a project, do you prefer to have a detailed plan in place or do you like to explore possibilities and figure it out as you go?', 'J', 'multiple_choice'),
('How do you approach deadlines?', 'J', 'multiple_choice'),
('In a work setting, do you prefer a clear and organized workspace or are you comfortable with a more flexible and adaptable environment?', 'J', 'multiple_choice'),
('When packing for a trip, do you plan and make a checklist in advance or pack on the fly, throwing in what feels right at the moment?', 'J', 'multiple_choice'),
('What do you do when your plans suddenly change?', 'J', 'multiple_choice'),
('When faced with a new opportunity, do you prefer to consider the advantages and disadvantages prior to making a decision or go with the flow and see where it takes you?', 'J', 'multiple_choice'),
('How do you approach work tasks?', 'J', 'multiple_choice'),
('When organizing your day, do you prefer to have a to-do list with specific tasks and deadlines or keep it open-ended and see where the day takes you?', 'J', 'multiple_choice'),
('How do you feel about routine and predictability?', 'J', 'multiple_choice'),
('In a decision-making process, do you like to reach a conclusion and move on or prefer to keep options open and gather more information?', 'J', 'multiple_choice');

-- Thinking vs Feeling (T vs F)
INSERT INTO PersonalityTestQuestions (question_text, category, question_type)
VALUES
('When making decisions, do you prioritize logical analysis and objective criteria or consider the impact on people and relationships?', 'T', 'multiple_choice'),
('How do you handle criticism or feedback?', 'T', 'multiple_choice'),
('When faced with a problem, do you rely more on your head and reason or your heart and empathy?', 'T', 'multiple_choice'),
('How do you prioritize tasks and responsibilities?', 'T', 'multiple_choice'),
('In a group decision-making process, do you tend to advocate for the most logical and rational choice or the one that aligns with personal values and harmony?', 'T', 'multiple_choice'),
('When giving feedback, do you focus on providing objective analysis or consider the individuals feelings and emotional response?', 'T', 'multiple_choice'),
('How do you express your opinions in a debate or discussion?', 'T', 'multiple_choice'),
('When solving a problem, do you prioritize efficiency and effectiveness, even if it means being blunt, or do you consider the feelings of those involved?', 'T', 'multiple_choice'),
('In a work environment, do you value objective performance metrics and results or prioritize a positive and supportive team culture?', 'T', 'multiple_choice'),
('How do you approach conflict resolution?', 'T', 'multiple_choice'),
('When planning an event or project, do you prioritize the logical steps and timeline or consider the emotional atmosphere and team dynamics?', 'T', 'multiple_choice'),
('How do you cope with stress or pressure?', 'T', 'multiple_choice'),
('When making decisions, what holds more weight for you?', 'T', 'multiple_choice'),
('When providing feedback, do you prioritize offering constructive criticism and improvement suggestions or highlighting positive aspects and encouraging the individual?', 'T', 'multiple_choice');




-- Inserting Personality Test Answers
INSERT INTO PersonalityTestAnswers (answer_id, answer_text, question_id) VALUES
(1, 'Large group interactions', 1),
(2, 'One-on-one conversations', 1),
(3, 'Spending time with friends or engaging in social activities', 2),
(4, 'Having some alone time to relax and unwind', 2),
(5, 'Brainstorming with others', 3),
(6, 'Working through it independently', 3),
(7, 'Social events and gatherings', 4),
(8, 'Quieter activities at home', 4),
(9, 'Enjoy it and find it easy to engage in', 5),
(10, 'Find it somewhat awkward or draining', 5),
(11, 'Rely on own instincts and feelings', 6),
(12, 'Seek input from others', 6),
(13, 'Embrace them with enthusiasm', 7),
(14, 'Approach them with caution', 7),
(15, 'Open office spaces and collaboration', 8),
(16, 'Individual workspaces', 8),
(17, 'Embrace it and feel at ease', 9),
(18, 'Prefer to avoid being the center of attention', 9),
(19, 'Social plans with friends', 10),
(20, 'Quiet time for yourself', 10),
(21, 'Initiate conversations and introductions', 11),
(22, 'Wait for others to approach you', 11),
(23, 'Rely on concrete facts and details', 12),
(24, 'Explore possibilities and potential meanings', 12),
(25, 'Prefer practical, hands-on experiences', 13),
(26, 'Enjoy exploring theories and concepts', 13),
(27, 'Present and current details', 14),
(28, 'Future possibilities and patterns', 14),
(29, 'Detailed itinerary and clear schedule', 15),
(30, 'Leave room for spontaneous experiences and changes', 15),
(31, 'Based on practical considerations and real-world implications', 16),
(32, 'Consider potential outcomes and future possibilities', 16),
(33, 'Specific tasks at hand', 17),
(34, 'Overall vision and goals', 17),
(35, 'Stick to facts and details', 18),
(36, 'Contribute ideas and theories', 18),
(37, 'Prefer stability and may find changes challenging', 19),
(38, 'Adapt well to changes and enjoy the flexibility', 19),
(39, 'Specific details and occurrences', 20),
(40, 'Overall impressions and meanings', 20),
(41, 'Plot and events', 21),
(42, 'Deeper meanings and symbolism', 21),
(43, 'Clear and straightforward explanations', 22),
(44, 'Rich with possibilities and potential connections', 22),
(45, 'Past experiences and proven methods', 23),
(46, 'Innovative and creative solutions', 23),
(47, 'Practical, actionable ideas', 24),
(48, 'Imaginative, out-of-the-box concepts', 24),
(49, 'Logical analysis and objective criteria', 25),
(50, 'Consider the impact on people and relationships', 25),
(51, 'Focus on the facts and seek constructive solutions', 26),
(52, 'Consider the emotional aspects and how it affects others', 26),
(53, 'Prioritize efficiency and effectiveness', 27),
(54, 'Consider the feelings of those involved', 27),
(55, 'Organized and systematic approach', 28),
(56, 'Flexible and adaptable, responding to the moment', 28),
(57, 'Advocate for logical and rational choices', 29),
(58, 'Align with personal values and harmony', 29),
(59, 'Objective analysis and constructive feedback', 30),
(60, 'Highlight positive aspects and encourage the individual', 30),
(61, 'Structured and methodical', 31),
(62, 'Flexible and spontaneous', 31),
(63, 'Clear, organized workspace', 32),
(64, 'Flexible and adaptable environment', 32),
(65, 'Detailed plan with checklists', 33),
(66, 'Pack on the fly and trust your instincts', 33),
(67, 'Feel frustrated or anxious', 34),
(68, 'Adapt quickly and seek new opportunities', 34),
(69, 'Consider advantages and disadvantages', 35),
(70, 'Go with the flow and see where it takes you', 35),
(71, 'Step-by-step, following the process', 36),
(72, 'Big picture, looking for creative angles', 36),
(73, 'To-do list with specific tasks', 37),
(74, 'Open-ended and flexible', 37),
(75, 'Enjoy routine and find comfort in predictability', 38),
(76, 'Prefer spontaneity and flexibility', 38),
(77, 'Reaching a conclusion and moving on', 39),
(78, 'Keep options open and gather more information', 39),
(79, 'I am very detail-oriented', 40),
(80, 'I prefer a more flexible and adaptable approach', 40),
(81, 'I like to research thoroughly before making a decision', 41),
(82, 'I tend to trust my instincts and go with the flow', 41),
(83, 'I am comfortable with ambiguity', 42),
(84, 'I prefer clear guidelines and structures', 42),
(85, 'I believe in taking calculated risks', 43),
(86, 'I tend to play it safe', 43),
(87, 'I enjoy challenging myself to think differently', 44),
(88, 'I prefer proven methods', 44),
(89, 'I thrive in fast-paced environments', 45),
(90, 'I prefer steady and predictable environments', 45),
(91, 'I enjoy brainstorming sessions with my team', 46),
(92, 'I prefer working alone on my projects', 46),
(93, 'I find comfort in established routines', 47),
(94, 'I enjoy breaking away from routines', 47),
(95, 'I prefer to be proactive in my decisions', 48),
(96, 'I often respond to situations as they arise', 48),
(97, 'I focus on long-term goals', 49),
(98, 'I am more concerned with immediate outcomes', 49),
(99, 'I prefer a structured approach to problem-solving', 50),
(100, 'I am open to exploring new ideas and solutions', 50);




-- Extroversion vs Introversion (E vs I)
UPDATE PersonalityTestAnswers SET answer_value = 'I' WHERE answer_id IN (2, 4, 6, 8, 10, 11, 14, 16, 18, 20, 22);

-- Sensing vs InUPDATE PersonalityTestAnswers SET answer_value = 'E' WHERE answer_id IN (1, 3, 5, 7, 9, 13, 15, 17, 19, 21);
tuition (S vs N)
UPDATE PersonalityTestAnswers SET answer_value = 'S' WHERE answer_id IN (23, 25, 27, 29, 31, 33, 35, 37, 39, 43, 45, 47, 49);
UPDATE PersonalityTestAnswers SET answer_value = 'N' WHERE answer_id IN (24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48);

-- Thinking vs Feeling (T vs F)
UPDATE PersonalityTestAnswers SET answer_value = 'T' WHERE answer_id IN (49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75);
UPDATE PersonalityTestAnswers SET answer_value = 'F' WHERE answer_id IN (50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76);

-- Judging vs Perceiving (J vs P)
UPDATE PersonalityTestAnswers SET answer_value = 'J' WHERE answer_id IN (77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99);
UPDATE PersonalityTestAnswers SET answer_value = 'P' WHERE answer_id IN (78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100);
