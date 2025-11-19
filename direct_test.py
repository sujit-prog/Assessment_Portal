# direct_test.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Attempting connection...")
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"User: {os.getenv('DB_USER')}")
    print(f"Database: {os.getenv('DB_NAME')}")
    
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        sslmode='require',
        connect_timeout=10
    )
    
    print("✅ SUCCESS! Connection established!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT current_database(), current_user;")
    result = cursor.fetchone()
    print(f"Connected to database: {result[0]}")
    print(f"Connected as user: {result[1]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ FAILED: {e}")