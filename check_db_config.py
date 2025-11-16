"""
Run this script to check your database configuration
Usage: python check_db_config.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent

print("\n" + "="*70)
print("DATABASE CONFIGURATION CHECKER")
print("="*70)

# Check if .env file exists
env_path = BASE_DIR / '.env'
print(f"\n1. Checking for .env file at: {env_path}")
if env_path.exists():
    print("   ✅ .env file found!")
    with open(env_path, 'r') as f:
        print("\n   Content of .env file:")
        print("   " + "-"*60)
        for line in f:
            if line.strip() and not line.startswith('#'):
                key = line.split('=')[0]
                if 'PASSWORD' in key:
                    print(f"   {key}=***hidden***")
                else:
                    print(f"   {line.strip()}")
        print("   " + "-"*60)
else:
    print("   ❌ .env file NOT found!")
    print(f"   Please create it at: {env_path}")

# Load environment variables
load_dotenv(env_path)

print("\n2. Environment Variables After Loading:")
print("   " + "-"*60)

env_vars = {
    'SUPABASE_DB_HOST': os.getenv('SUPABASE_DB_HOST'),
    'SUPABASE_DB_NAME': os.getenv('SUPABASE_DB_NAME'),
    'SUPABASE_DB_USER': os.getenv('SUPABASE_DB_USER'),
    'SUPABASE_DB_PASSWORD': '***hidden***' if os.getenv('SUPABASE_DB_PASSWORD') else None,
    'SUPABASE_DB_PORT': os.getenv('SUPABASE_DB_PORT'),
}

for key, value in env_vars.items():
    if value:
        print(f"   ✅ {key} = {value}")
    else:
        print(f"   ❌ {key} = NOT SET")

print("   " + "-"*60)

# Test DNS resolution
print("\n3. Testing DNS Resolution:")
if os.getenv('SUPABASE_DB_HOST'):
    import socket
    host = os.getenv('SUPABASE_DB_HOST')
    print(f"   Trying to resolve: {host}")
    try:
        ip = socket.gethostbyname(host)
        print(f"   ✅ DNS resolution successful! IP: {ip}")
    except socket.gaierror as e:
        print(f"   ❌ DNS resolution failed!")
        print(f"   Error: {e}")
        print("\n   Possible issues:")
        print("   - Check if hostname is correct (should be like: db.xxxxx.supabase.co)")
        print("   - Check your internet connection")
        print("   - Try accessing https://app.supabase.com to verify the hostname")
else:
    print("   ⚠️  SUPABASE_DB_HOST not set, skipping DNS test")

# Test PostgreSQL connection
print("\n4. Testing Database Connection:")
if all([os.getenv('SUPABASE_DB_HOST'), os.getenv('SUPABASE_DB_PASSWORD')]):
    try:
        import psycopg2
        print("   ✅ psycopg2 is installed")
        
        print("   Attempting to connect to database...")
        conn = psycopg2.connect(
            host=os.getenv('SUPABASE_DB_HOST'),
            port=os.getenv('SUPABASE_DB_PORT', '5432'),
            database=os.getenv('SUPABASE_DB_NAME', 'postgres'),
            user=os.getenv('SUPABASE_DB_USER', 'postgres'),
            password=os.getenv('SUPABASE_DB_PASSWORD'),
            sslmode='require',
            connect_timeout=10
        )
        print("   ✅ Connection successful!")
        conn.close()
    except ImportError:
        print("   ❌ psycopg2 not installed!")
        print("   Run: pip install psycopg2-binary")
    except Exception as e:
        print(f"   ❌ Connection failed!")
        print(f"   Error: {e}")
else:
    print("   ⚠️  Database credentials not complete, skipping connection test")

print("\n" + "="*70)
print("CONFIGURATION CHECK COMPLETE")
print("="*70 + "\n")