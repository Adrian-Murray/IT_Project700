import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def create_derived_features(df):
    """Create enhanced features from raw data"""
    df['analytical_score'] = df['Dominance'] * 0.3 + df['Formality'] * 0.7
    df['leadership_score'] = df['Dominance'] * 0.6 + df['Extraversion'] * 0.4
    df['team_player_score'] = df['Patience'] * 0.5 + df['Extraversion'] * 0.5
    
    df['age_group'] = pd.cut(
        df['Age'], 
        bins=[0, 22, 25, 30, 35, 100],
        labels=['early_career', 'graduate', 'developing', 'experienced', 'senior']
    )
    
    return df

def calculate_skill_match(user_skills, course_skills):
    """Calculate skill match score"""
    if not user_skills or not course_skills:
        return 0.0
    
    user_skill_list = set(s.strip() for s in user_skills.split(','))
    course_skill_list = set(s.strip() for s in course_skills.split(','))
    
    if not course_skill_list:
        return 0.0
        
    return len(user_skill_list.intersection(course_skill_list)) / len(course_skill_list)