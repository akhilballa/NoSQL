import sqlite3
import os
import csv
import config

# Mock Hive DB using SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mock_hive.db")
CSV_FILE_PATH = os.path.join(BASE_DIR, "student_course_grades.csv")

def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def _init_db():
    """Initialize the SQLite DB and load data from CSV if table is empty"""
    conn = _get_connection()
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_grades1 (
        student_id TEXT,
        course_id TEXT,
        roll_no TEXT,
        email_id TEXT,
        grade TEXT
    )
    """)
    conn.commit()
    
    # Check if empty
    cursor.execute("SELECT COUNT(*) FROM student_grades1")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print(f"[MockHive] Initializing database from {CSV_FILE_PATH}...")
        if os.path.exists(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, 'r') as file:
                reader = csv.DictReader(file)
                to_db = [(i['student-ID'], i['course-id'], i['roll no'], i['email ID'], i['grade']) for i in reader]
                
            cursor.executemany("INSERT INTO student_grades1 (student_id, course_id, roll_no, email_id, grade) VALUES (?, ?, ?, ?, ?)", to_db)
            conn.commit()
            print(f"[MockHive] Loaded {len(to_db)} records.")
        else:
            print(f"[MockHive] Warning: CSV file not found at {CSV_FILE_PATH}")
    
    conn.close()

# Initialize DB on module load
_init_db()

def get_grade(student_id, course_id):
    try:
        conn = _get_connection()
        cursor = conn.cursor()

        query = """
        SELECT grade
        FROM student_grades1
        WHERE student_id = ? AND course_id = ?
        LIMIT 1
        """
        cursor.execute(query, (student_id, course_id))
        result = cursor.fetchone()

        if result:
            print(f"Grade for ({student_id}, {course_id}) is: {result[0]}")
            return True  # Successful retrieval
        else:
            print(f"No record found for ({student_id}, {course_id})")
            return False  # No record found, return False

    except Exception as err:
        print(f"Hive (Mock) Error: {err}")
        return False  # Return False on error
    finally:
        if 'conn' in locals():
            conn.close()


def set_grade(student_id, course_id, grade):
    try:
        conn = _get_connection()
        cursor = conn.cursor()

        # Check if the (student_id, course_id) pair exists
        check_exist_query = """
        SELECT COUNT(1)
        FROM student_grades1
        WHERE student_id = ? AND course_id = ?
        """
        cursor.execute(check_exist_query, (student_id, course_id))
        exists = cursor.fetchone()[0]

        # If the (student_id, course_id) pair doesn't exist, do nothing and return False
        if exists == 0:
            print(f"No matching record found to update.")
            return False  # No matching record found, return False

        # Check if the current grade is already the same as the new one
        check_query = """
        SELECT grade
        FROM student_grades1
        WHERE student_id = ? AND course_id = ?
        """
        cursor.execute(check_query, (student_id, course_id))
        current_grade = cursor.fetchone()

        # If the grade is already the same, skip the update and print no change
        if current_grade and current_grade[0] == grade:
            print(f"No update needed for ({student_id}, {course_id}) as the grade is already '{grade}'")
            return False  # No update needed, return False

        # Update data
        update_query = """
        UPDATE student_grades1
        SET grade = ?
        WHERE student_id = ? AND course_id = ?
        """
        cursor.execute(update_query, (grade, student_id, course_id))
        conn.commit()
        
        print(f"Updated grade for ({student_id}, {course_id}) to '{grade}'")
        return True  # Successful update

    except Exception as err:
        print(f"Hive (Mock) Error: {err}")
        return False  # Return False on error
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    # Test
    get_grade('SID1033', 'CSE016')
    set_grade('SID1033', 'CSE016', 'Z')
    get_grade('SID1033', 'CSE016')
