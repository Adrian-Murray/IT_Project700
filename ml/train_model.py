import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
from feature_engineering import create_derived_features

def train_model():
    df = pd.read_csv('../data/career_recommendation_with_courses.csv')
    
    df = create_derived_features(df)
    
    categorical_features = ['Course', 'Universities_ID', 'Faculty/Department', 'age_group']
    numerical_features = [
        'Duration', 'analytical_score', 'leadership_score', 'team_player_score',
        'Dominance', 'Extraversion', 'Patience', 'Formality'
    ]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=42
        ))
    ])
    
    X = df[categorical_features + numerical_features]
    y = df['Recommended Career']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    pipeline.fit(X_train, y_train)
    
    train_score = pipeline.score(X_train, y_train)
    test_score = pipeline.score(X_test, y_test)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
    
    print("\nModel Performance:")
    print(f"Train Score: {train_score:.4f}")
    print(f"Test Score: {test_score:.4f}")
    print(f"CV Scores Mean: {cv_scores.mean():.4f}")
    
    joblib.dump(pipeline, '../models/career_recommendation_model.pkl')
   
    feature_importance = pipeline.named_steps['classifier'].feature_importances_

    categorical_features_encoded = pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    all_features = list(categorical_features_encoded) + numerical_features
    
    print("\nFeature Importance:")
    for feature, importance in sorted(zip(all_features, feature_importance), 
                                    key=lambda x: x[1], reverse=True)[:10]:
        print(f"{feature}: {importance:.4f}")
    
if __name__ == "__main__":
    train_model()