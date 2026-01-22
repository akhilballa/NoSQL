from pyhive import hive
from pymongo import MongoClient
import mysql.connector
import config

def create_hive_database(database_name="db", host="localhost", port=10000):
    """Create a Hive database if it does not exist."""
    try:
        # Use config if defaults are passed
        host = config.HIVE_HOST if host == "localhost" else host
        port = config.HIVE_PORT if port == 10000 else port
        db_name = config.HIVE_DB # Use config db name
        
        conn = hive.Connection(host=host, port=port, username=config.HIVE_USER) 
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Hive database '{db_name}' created successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to create Hive database: {e}")

def create_mongodb_database(database_name="sample", host="localhost", port=27017):
    """Create a MongoDB database by inserting into a dummy collection."""
    try:
        host = config.MONGO_HOST if host == "localhost" else host
        port = config.MONGO_PORT if port == 27017 else port
        db_name = config.MONGO_DB
        
        client = MongoClient(host, port)
        db = client[db_name]
        print(f"MongoDB database '{db_name}' created successfully.")
        client.close()
    except Exception as e:
        print(f"Failed to create MongoDB database: {e}")

def create_mysql_database(database_name="sample", host="localhost", user="root", password="yourpassword"):
    """Create a MySQL database if it does not exist."""
    try:
        host = config.MYSQL_HOST if host == "localhost" else host
        user = config.MYSQL_USER if user == "root" else user
        password = config.MYSQL_PASSWORD
        db_name = config.MYSQL_DB
        
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"MySQL database '{db_name}' created successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to create MySQL database: {e}")

if __name__ == "__main__":
    create_hive_database()
    create_mongodb_database()
    create_mysql_database() 