from pyhive import hive
from TCLIService.ttypes import TApplicationException
import config

def get_grade(student_id, course_id):
    try:
        conn = hive.Connection(host=config.HIVE_HOST, port=config.HIVE_PORT, username=config.HIVE_USER, database=config.HIVE_DB)
        cursor = conn.cursor()

        query = f"""
        SELECT grade
        FROM student_grades1
        WHERE student_id = '{student_id}' AND course_id = '{course_id}'
        LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            print(f"Grade for ({student_id}, {course_id}) is: {result[0]}")
            return True  # Successful retrieval
        else:
            print(f"No record found for ({student_id}, {course_id})")
            return False  # No record found, return False

    except TApplicationException as err:
        print(f"Hive Error: {err}")
        return False  # Return False on error
    finally:
        cursor.close()
        conn.close()


def set_grade(student_id, course_id, grade):
    try:
        conn = hive.Connection(host=config.HIVE_HOST, port=config.HIVE_PORT, username=config.HIVE_USER, database=config.HIVE_DB)
        cursor = conn.cursor()

        # Check if the (student_id, course_id) pair exists
        check_exist_query = f"""
        SELECT COUNT(1)
        FROM student_grades1
        WHERE student_id = '{student_id}' AND course_id = '{course_id}'
        """
        cursor.execute(check_exist_query)
        exists = cursor.fetchone()[0]

        # If the (student_id, course_id) pair doesn't exist, do nothing and return False
        if exists == 0:
            print(f"No matching record found to update.")
            return False  # No matching record found, return False

        # Check if the current grade is already the same as the new one
        check_query = f"""
        SELECT grade
        FROM student_grades1
        WHERE student_id = '{student_id}' AND course_id = '{course_id}'
        """
        cursor.execute(check_query)
        current_grade = cursor.fetchone()

        # If the grade is already the same, skip the update and print no change
        if current_grade and current_grade[0] == grade:
            print(f"No update needed for ({student_id}, {course_id}) as the grade is already '{grade}'")
            return False  # No update needed, return False

        # Insert data into student_grades1 table with updated grade
        insert_query = f"""
        INSERT OVERWRITE TABLE student_grades1
        SELECT student_id, course_id, roll_no, email_id, 
               CASE WHEN student_id = '{student_id}' AND course_id = '{course_id}' THEN '{grade}' ELSE grade END
        FROM student_grades1
        """
        cursor.execute(insert_query)
        
        print(f"Updated grade for ({student_id}, {course_id}) to '{grade}'")
        return True  # Successful update

    except TApplicationException as err:
        print(f"Hive Error: {err}")
        return False  # Return False on error
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # set_grade('SID9999','CSE020','H1')
    # set_grade('SID1033','CSE016','C1')
    
    set_grade('SID9999','CSE020','C')
    get_grade('SID1033','CSE016')
    
    

# def set_grade(student_id, course_id, grade):
#     try:
#         conn = hive.Connection(host="localhost", port=10000, username="hadoop", database="db")
#         cursor = conn.cursor()

#         # Create a temporary table
#         cursor.execute("CREATE TABLE IF NOT EXISTS grades_temp LIKE student_grades1")

#         # Insert data into temp table with updated grade
#         insert_query = f"""
#         INSERT OVERWRITE TABLE student_grades1
#         SELECT student_id, course_id, roll_no, email_id, 
#                CASE WHEN student_id = '%s' AND course_id = '%s' THEN '%s' ELSE grade END
#         FROM student_grades1
#         """
#         cursor.execute(insert_query)

#         # Overwrite the original student_grades1 table with temp table
#         cursor.execute("TRUNCATE TABLE student_grades1")
#         cursor.execute("INSERT INTO TABLE student_grades1 SELECT * FROM grades_temp")

#         # Optionally drop temp table
#         cursor.execute("DROP TABLE grades_temp")

#         print(f"Updated grade for ({student_id}, {course_id}) to '{grade}'")

#     except TApplicationException as err:
#         print(f"Hive Error: {err}")
#     finally:
#         cursor.close()
#         conn.close()
