import sqlite3

def run_sql_file(filename):
    # Connect to the SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect('users.db')  # Ensure this is the correct path for your SQLite DB
    cursor = conn.cursor()

    # Read the SQL file
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script
    try:
        cursor.executescript(sql_script)
        print("Database edited successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Since you're already in the resource directory, adjust the path
    run_sql_file('edit_db.sql')
