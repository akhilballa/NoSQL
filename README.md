# NoSQL Distributed Database Project

This project implements a distributed database system that interacts with **MySQL**, **MongoDB**, and **Hive**. It allows for operations like `GET`, `SET`, and `MERGE` across these different database systems using a centralized driver script.

## 🚀 Prerequisites

Before starting, ensure you have the following installed on your machine:

1.  **Python 3.x**
2.  **MySQL Server** (Running on `localhost:3306`)
3.  **MongoDB** (Running on `localhost:27017`)

---

## 🛠️ Step-by-Step Setup Instructions

Follow these steps exactly to set up and run the project from scratch.

### 1. Environment Setup
Create and activate a virtual environment to isolate dependencies.

**Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Install all required Python libraries.
```bash
pip install -r requirements.txt
```

### 3. Configure Database Credentials
Open the `config.py` file and update the credentials to match your local database settings.
- **MySQL**: Update `MYSQL_USER` and `MYSQL_PASSWORD`.
- **MongoDB**: Default settings (`localhost:27017`) usually work fine.
- **Hive**: You can ignore these settings as we are using the mock implementation.

### 4. Create Databases (Fresh Start)
Run this script to ensure the `sample` (MySQL/Mongo) and `db` (Hive) databases exist on your system.
```bash
python create_databases.py
```

### 5. Populate Tables
Run this script to:
- Clear old data from MySQL and MongoDB.
- Load fresh data from `student_course_grades.csv` into MySQL and MongoDB.
- *Note: This script might show a Hive error, which is expected and safe to ignore.*
```bash
python setup_tables.py
```

---

## ▶️ How to Run the Project

Once setup is complete, run the main driver script. This script will:
1.  Initialize the **Mock Hive** database (loading data from CSV if needed).
2.  Read commands from `testcase1.in`.
3.  Execute `GET`, `SET`, and `MERGE` operations across MySQL, MongoDB, and the Mock Hive.
4.  Generate logs in `oplog.sql.txt`, `oplog.mongo.txt`, and `oplog.hive.txt`.

```bash
python driver.py
```

---

## 🔍 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **`ModuleNotFoundError`** | Ensure you activated the virtual environment (`source venv/bin/activate`) and ran `pip install -r requirements.txt`. |
| **`MySQL Error: 1045 (Access Denied)`** | Check your username/password in `config.py`. |
| **`MySQL Error: 1049 (Unknown database)`** | Run `python create_databases.py` first. |
| **`TExecuteStatementResp` (Hive Error)** | Ignore this if running `setup_tables.py`. The execution relies on `mock_hive.db` created by `driver.py`. |
| **`KeyError: 'student_id'`** | Ensure your `student_course_grades.csv` headers match the code. The project expects `student-ID` format as per the provided CSV. |

## 📂 Project Structure

- **`driver.py`**: Main entry point; handles command execution and coordination.
- **`config.py`**: Central configuration for database credentials.
- **`hive_db.py`**: Handles Hive operations (via SQLite mock).
- **`mysql_db.py`**: Handles MySQL operations.
- **`mongo_db.py`**: Handles MongoDB operations.
- **`setup_tables.py`**: Utility to reset and populate tables.
- **`create_databases.py`**: Utility to create initial databases.
- **`student_course_grades.csv`**: Source data file.
