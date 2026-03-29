"""
Corrected Database Connection Test Script
Save as: test_connection.py
Usage: python test_connection.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent

print("\n" + "="*70)
print("DATABASE CONNECTION TEST")
print("="*70)

# Check if .env file exists
env_path = BASE_DIR / '.env'
print(f"\n1. Checking for .env file at: {env_path}")
if env_path.exists():
    print("   ✅ .env file found!")
else:
    print("   ❌ .env file NOT found!")
    print(f"   Please create it at: {env_path}")
    exit(1)

# Load environment variables
load_dotenv(env_path)

print("\n2. Environment Variables:")
print("   " + "-"*60)

env_vars = {
    'DB_HOST': os.getenv('DB_HOST'),
    'DB_NAME': os.getenv('DB_NAME'),
    'DB_USER': os.getenv('DB_USER'),
    'DB_PASSWORD': '***hidden***' if os.getenv('DB_PASSWORD') else None,
    'DB_PORT': os.getenv('DB_PORT'),
}

all_set = True
for key, value in env_vars.items():
    if value:
        print(f"   ✅ {key} = {value}")
    else:
        print(f"   ❌ {key} = NOT SET")
        all_set = False

print("   " + "-"*60)

if not all_set:
    print("\n❌ Some environment variables are missing!")
    print("Please check your .env file.")
    exit(1)

# Test DNS resolution
print("\n3. Testing DNS Resolution:")
host = os.getenv('DB_HOST')
print(f"   Trying to resolve: {host}")
try:
    import socket
    ip = socket.gethostbyname(host)
    print(f"   ✅ DNS resolution successful! IP: {ip}")
except socket.gaierror as e:
    print(f"   ❌ DNS resolution failed!")
    print(f"   Error: {e}")
    exit(1)

# Test PostgreSQL connection
print("\n4. Testing Database Connection:")
try:
    import psycopg2
    print("   ✅ psycopg2 is installed")
    
    print("   Attempting to connect to database...")
    print(f"   Host: {os.getenv('DB_HOST')}")
    print(f"   Port: {os.getenv('DB_PORT')}")
    print(f"   Database: {os.getenv('DB_NAME')}")
    print(f"   User: {os.getenv('DB_USER')}")
    
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        sslmode='require',
        connect_timeout=10
    )
    
    print("   ✅ Connection successful!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"   ✅ PostgreSQL version: {version[0][:50]}...")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - Your database is configured correctly!")
    print("="*70)
    print("\nYou can now run:")
    print("  python manage.py migrate")
    print("  python manage.py runserver")
    print("="*70 + "\n")
    
except ImportError:
    print("   ❌ psycopg2 not installed!")
    print("\n   Please install it:")
    print("   pip install psycopg2-binary")
    exit(1)
except psycopg2.OperationalError as e:
    print(f"   ❌ Connection failed!")
    print(f"   Error: {e}")
    print("\n   Common issues:")
    print("   1. Wrong password - Check DB_PASSWORD in .env")
    print("   2. Wrong host/port - Verify from Supabase dashboard")
    print("   3. Firewall blocking connection")
    print("   4. Database paused - Check Supabase project status")
    exit(1)
except Exception as e:
    print(f"   ❌ Unexpected error!")
    print(f"   Error: {e}")
    exit(1)