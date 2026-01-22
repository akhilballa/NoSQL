# NoSQL Project Execution Guide

This project interacts with **MySQL**, **MongoDB**, and **Hive** databases using processing logic defined in `driver.py`.

## Prerequisites

Before running the code, ensure you have the following installed and running:

1.  **Python 3.x**
2.  **MySQL Server** (Running on localhost:3306)
3.  **MongoDB** (Running on localhost:27017)
4.  **Apache Hive** (Running on localhost:10000 with Thrift server)

## Setup

### 1. Create a Virtual Environment (Recommended)

Since newer systems enforce managed environments, it's best to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials

The scripts use hardcoded credentials. You **must** ensure your local database setups match these, or update the python files:

*   **MySQL**: User: `root`, Password: `Manish@123`, Database: `sample`
    *   *File to check*: `mysql_db.py`, `create_databases.py`
*   **Hive**: User: `hadoop`, Port: `10000`, Database: `db`
    *   *File to check*: `hive_db.py`, `create_databases.py`
*   **MongoDB**: Host: `localhost`, Port: `27017`
    *   *File to check*: `mongo_db.py`, `create_databases.py`

### 3. Initialize Databases

Run the initialization script to create the necessary databases if they don't exist:

```bash
python create_databases.py
```

*Note: If this script fails, ensure your database services are running and accessible with the credentials mentioned above.*

## Running the Project

The main entry point is `driver.py`, which processes input files (like `testcase.in`).

```bash
python driver.py
```

By default, `driver.py` is set to process `testcase1.in` (check the `__main__` block at the bottom of `driver.py` to change this).

## Troubleshooting

*   **`ModuleNotFoundError`**: Run `pip install -r requirements.txt` again.
*   **Connection Refused**: Check if the respective database service (MySQL, Mongo, or Hive) is started.
*   **Authentication Error**: Verify the username and password in `mysql_db.py`, `hive_db.py`, and `create_databases.py` match your local setup.
