from pyhive import hive
import mysql.connector
import pymongo
import csv
import os
import config

# Get absolute path of the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(BASE_DIR, "student_course_grades.csv")

def create_and_load_hive():
    print(f"Connecting to Hive at {config.HIVE_HOST}:{config.HIVE_PORT}...")
    try:
        conn = hive.Connection(host=config.HIVE_HOST, port=config.HIVE_PORT, username=config.HIVE_USER, database=config.HIVE_DB)
        cursor = conn.cursor()

        # Create a local hive_data directory for the table
        hive_data_dir = os.path.join(BASE_DIR, "hive_data")
        if not os.path.exists(hive_data_dir):
            os.makedirs(hive_data_dir)
            
        # Ensure the directory has proper permissions (if needed)
        os.chmod(hive_data_dir, 0o777)

        print(f"Using local Hive data directory: {hive_data_dir}")
        
        print("Creating Hive table...")
        # Drop table if exists to ensure clean state with new location
        cursor.execute("DROP TABLE IF EXISTS student_grades1")
        
        create_query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS student_grades1 (
            student_id STRING,
            course_id STRING,
            roll_no STRING,
            email_id STRING,
            grade STRING
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\\n'
        STORED AS TEXTFILE
        LOCATION 'file://{hive_data_dir}'
        TBLPROPERTIES ("skip.header.line.count"="1")
        """
        cursor.execute(create_query)

        print(f"Loading data from {CSV_FILE_PATH} into Hive...")
        # Use LOCAL INPATH to load file from local filesystem
        load_query = f"LOAD DATA LOCAL INPATH '{CSV_FILE_PATH}' OVERWRITE INTO TABLE student_grades1"
        cursor.execute(load_query)

        print("Hive: Table created and data loaded successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Hive Error: {e}")

def create_and_load_mysql():
    print(f"Connecting to MySQL at {config.MYSQL_HOST}...")
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            allow_local_infile=True # Enable local infile if needed
        )
        cursor = conn.cursor()

        print("Creating MySQL table...")
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

        print("Truncating MySQL table...")
        cursor.execute("TRUNCATE TABLE student_grades1")

        print(f"Loading data from {CSV_FILE_PATH} into MySQL...")
        with open(CSV_FILE_PATH, 'r') as file:
            next(file)  # Skip header
            reader = csv.reader(file)
            data = [tuple(row) for row in reader]
            
            if data:
                cursor.executemany(
                    "INSERT INTO student_grades1 (student_id, course_id, roll_no, email_id, grade) VALUES (%s, %s, %s, %s, %s)",
                    data
                )

        conn.commit()
        print("MySQL: Table created and data loaded successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"MySQL Error: {e}")

def create_and_load_mongodb():
    print(f"Connecting to MongoDB at {config.MONGO_HOST}:{config.MONGO_PORT}...")
    try:
        client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        db = client[config.MONGO_DB]
        collection = db["student_grades1"]
        
        print("Clearing MongoDB collection...")
        collection.delete_many({})
        
        print(f"Loading data from {CSV_FILE_PATH} into MongoDB...")
        documents = []
        with open(CSV_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                documents.append(row)

        if documents:
            collection.insert_many(documents)

        print("MongoDB: Collection created and data loaded successfully.")
        client.close()
    except Exception as e:
        print(f"MongoDB Error: {e}")

if __name__ == "__main__":
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: CSV file not found at {CSV_FILE_PATH}")
    else:
        create_and_load_hive()
        create_and_load_mysql()
        create_and_load_mongodb()
