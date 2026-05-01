from dotenv import find_dotenv, load_dotenv
import os

# 1. Look for the file
env_path = find_dotenv()
print(f"\n1. 🔍 find_dotenv() located file at: '{env_path}'")

# 2. Try to load it
load_dotenv(env_path)

# 3. Print the variables (we will obscure the password for safety)
print("2. 🗄️ Checking Variables:")
print(f"   DB_HOST: {os.getenv('DB_HOST')}")
print(f"   DB_USER: {os.getenv('DB_USER')}")
print(f"   DB_PASSWORD: {'FOUND' if os.getenv('DB_PASSWORD') else 'NONE'}")
print(f"   DB_NAME: {os.getenv('DB_NAME')}\n")