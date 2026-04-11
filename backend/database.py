import MySQLdb
import MySQLdb.cursors
import os
from dotenv import load_dotenv, find_dotenv

# 1. find_dotenv() automatically hunts down your .env file
env_path = find_dotenv()

# 2. Print it to the terminal so we can PROVE Windows actually sees it!
print(f"🔧 DEBUG: Loading .env file from: {env_path}")

# 3. Load the variables
load_dotenv(env_path)

def get_db_connection():
    """Helper function to create a new database connection."""
    return MySQLdb.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        passwd=os.getenv('DB_PASSWORD'), 
        db=os.getenv('DB_NAME'),
        cursorclass=MySQLdb.cursors.DictCursor
    )