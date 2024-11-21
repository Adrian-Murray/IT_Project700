# verify_data.py
import pandas as pd

def verify_csv_files():
    print("Verifying CSV files...\n")
    
    # Check Universities.csv
    try:
        unis_df = pd.read_csv('data/Universities.csv', encoding='utf-8')
        print("Universities.csv:")
        print(f"Columns: {unis_df.columns.tolist()}")
        print(f"Row count: {len(unis_df)}")
        print("\nSample row:")
        print(unis_df.iloc[0])
        print("\n")
    except Exception as e:
        print(f"Error reading Universities.csv: {str(e)}\n")
    
    # Check courses_cleaned.csv
    try:
        courses_df = pd.read_csv('data/courses_cleaned.csv', delimiter=';', encoding='utf-8')
        print("courses_cleaned.csv:")
        print(f"Columns: {courses_df.columns.tolist()}")
        print(f"Row count: {len(courses_df)}")
        print("\nSample row:")
        print(courses_df.iloc[0])
        print("\n")
    except Exception as e:
        print(f"Error reading courses_cleaned.csv: {str(e)}\n")

if __name__ == "__main__":
    verify_csv_files()