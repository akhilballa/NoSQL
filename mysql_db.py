import mysql.connector
import config

def get_grade(student_id, course_id):
    try:
        connection = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        cursor = connection.cursor()

        query = """
            SELECT grade FROM student_grades1
            WHERE student_id = %s AND course_id = %s
        """
        cursor.execute(query, (student_id, course_id))
        print("Done mysql get grade,...")
        result = cursor.fetchone()

        if result:
            print(f" Grade for ({student_id}, {course_id}) is: {result[0]}")
            return True  # Successfully retrieved grade
        else:
            print(f"No record found for ({student_id}, {course_id})")
            return False  # No record found

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
        return False  # MySQL error occurred
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()


def set_grade(student_id, course_id, grade):
    try:
        connection = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        cursor = connection.cursor()

        query = """
            UPDATE student_grades1
            SET grade = %s
            WHERE student_id = %s AND course_id = %s
        """
        cursor.execute(query, (grade, student_id, course_id))
        connection.commit()

        if cursor.rowcount:
            print(f"Updated grade for ({student_id}, {course_id}) to '{grade}'")
            return True  # Successfully updated grade
        else:
            print(f"No matching record found to update.")
            return False  # No record found to update

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False  # MySQL error occurred
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    set_grade('SID9999','CSE020','H')
    set_grade('SID1033','CSE016','C')
    


