from pyhive import hive
import mysql.connector
import pymongo
import subprocess
import csv

import config

def create_and_load_hive():
    conn = hive.Connection(host=config.HIVE_HOST, port=config.HIVE_PORT, username=config.HIVE_USER, database=config.HIVE_DB)
    cursor = conn.cursor()

    create_query = """
    CREATE TABLE IF NOT EXISTS student_grades1 (
        student_id STRING,
        course_id STRING,
        roll_no STRING,
        email_id STRING,
        grade STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    STORED AS TEXTFILE
    TBLPROPERTIES ("skip.header.line.count"="1")
    """
    cursor.execute(create_query)

    # Upload CSV to HDFS
    local_path = "/home/manish/NoSQL/Project/student_course_grades.csv"
    hdfs_path = "/user/manish/student_course_grades.csv"
    
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", "/user/manish"])
    subprocess.run(["hdfs", "dfs", "-put", "-f", local_path, hdfs_path])

    cursor.execute("TRUNCATE TABLE student_grades1")

    # Load data into Hive table
    load_query = f"LOAD DATA INPATH '{hdfs_path}' INTO TABLE student_grades1"
    cursor.execute(load_query)

    print("Hive: Table created and data loaded successfully.")
    cursor.close()
    conn.close()


def create_and_load_mysql():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS student_grades1 (
        student_id VARCHAR(255),
        course_id VARCHAR(255),
        roll_no VARCHAR(255),
        email_id VARCHAR(255),
        grade VARCHAR(10)
    )
    """
    cursor.execute(create_table_query)

    cursor.execute("TRUNCATE TABLE student_grades1")

    # Load CSV and Insert into MySQL
    csv_file_path = '/home/manish/NoSQL/Project/student_course_grades.csv'
    with open(csv_file_path, 'r') as file:
        next(file)  # Skip header
        reader = csv.reader(file)
        for row in reader:
            cursor.execute(
                "INSERT INTO student_grades1 (student_id, course_id, roll_no, email_id, grade) VALUES (%s, %s, %s, %s, %s)",
                row
            )

    conn.commit()
    print("MySQL: Table created and data loaded successfully.")
    cursor.close()
    conn.close()


def create_and_load_mongodb():
    client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
    db = client[config.MONGO_DB]
    collection = db["student_grades1"]
    collection.delete_many({})
    csv_file_path = '/home/manish/NoSQL/Project/student_course_grades.csv'

    documents = []
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            documents.append(row)

    collection.insert_many(documents)

    print("MongoDB: Collection created and data loaded successfully.")
    client.close()


# Call the function you want
create_and_load_hive()
create_and_load_mysql()
create_and_load_mongodb()
