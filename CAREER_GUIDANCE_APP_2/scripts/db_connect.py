import sqlite3
import os

def connect_to_db(db_path):
    try:
        connection = sqlite3.connect(db_path)
        print(f"Successfully connected to the database: {db_path}")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

if __name__ == "__main__":
    # Specify the path to your database
    db_name = '/workspaces/IT_Project700/CAREER_GUIDANCE_APP_2/resource/users.db'
    connection = connect_to_db(db_name)

    if connection:
        # Keep the connection open and launch sqlite3 shell
        connection.close()  # Close the connection after opening the shell
        os.system(f'sqlite3 {db_name}')  # This will start the SQLite shell with the database
