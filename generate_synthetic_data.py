import pandas as pd
import numpy as np
import random

# Define the desired number of samples
num_samples = 500

# Define courses, career mappings, and career skills mappings as before
courses = [
    "Bachelor of Computer Science", "BCOM Law", "BCOM Accounting", 
    "BCOM Logistics", "BEng Civil Engineering", "Bachelor of Nursing", 
    "Fitting and Turning", "Boiler Making", "BSc in Agriculture in Animal Science", 
    "Bed Degree in Foundation Phase Teaching", "Diploma in Information Technology", 
    "LLB", "MBBCH Medicine and Surgery", "Diploma in Crop Production", 
    "BEngTech Industrial Engineering", "BEng Industrial Engineering", 
    "BCOM Finance", "BCOM Economics", "BSc Geology and Geography"
]

# Mapping from courses to careers
course_career_map = {
    "Bachelor of Computer Science": "Software Engineer",
    "BCOM Law": "Corporate Lawyer",
    "BCOM Accounting": "Accountant",
    "BCOM Logistics": "Logistics Manager",
    "BEng Civil Engineering": "Civil Engineer",
    "Bachelor of Nursing": "Registered Nurse",
    "Fitting and Turning": "Mechanical Technician",
    "Boiler Making": "Welding Technician",
    "BSc in Agriculture in Animal Science": "Agronomist",
    "Bed Degree in Foundation Phase Teaching": "Primary School Teacher",
    "Diploma in Information Technology": "IT Support Specialist",
    "LLB": "Public Defender",
    "MBBCH Medicine and Surgery": "General Practitioner",
    "Diploma in Crop Production": "Agronomist",
    "BEngTech Industrial Engineering": "Industrial Engineer",
    "BEng Industrial Engineering": "Operations Manager",
    "BCOM Finance": "Financial Analyst",
    "BCOM Economics": "Economist",
    "BSc Geology and Geography": "Geologist"
}

# Initialize data dictionary with random values
data = {
    "Age": np.random.randint(20, 35, size=num_samples),
    "Course": np.random.choice(courses, num_samples),
    "Universities_ID": np.random.randint(1, 10, size=num_samples),
    "Faculty/Department": np.random.choice(["SCIENCE", "LAW", "ENGINEERING", "HEALTH", "ECONOMICS"], num_samples),
    "Duration": np.random.choice([1, 2, 3, 4], num_samples),
    "Key Skills": np.random.choice(["Programming,Data Structures", "Legal Research,Negotiation", "Financial Analysis,Excel"], num_samples),
    "Dominance": np.random.randint(1, 10, size=num_samples),
    "Extraversion": np.random.randint(1, 10, size=num_samples),
    "Patience": np.random.randint(1, 10, size=num_samples),
    "Formality": np.random.randint(1, 10, size=num_samples),
}

# Generate Recommended Career based on Course
recommended_careers = []
for course in data["Course"]:
    recommended_career = course_career_map.get(course, "Generalist")
    recommended_careers.append(recommended_career)

data["Recommended Career"] = recommended_careers

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV for use in training
df.to_csv("career_recommendation_with_courses.csv", index=False)
print(f"Synthetic dataset with {len(df)} samples created and saved as career_recommendation_with_courses.csv")
