"""
Django Database Connection Test
Save as: django_db_test.py
Usage: python django_db_test.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_app.settings')
django.setup()

from django.db import connection
from django.conf import settings

print("\n" + "="*70)
print("DJANGO DATABASE CONNECTION TEST")
print("="*70)

print("\n1. Django Settings:")
print("   " + "-"*60)
db_settings = settings.DATABASES['default']
print(f"   Engine: {db_settings.get('ENGINE')}")
print(f"   Name: {db_settings.get('NAME')}")
print(f"   User: {db_settings.get('USER')}")
print(f"   Host: {db_settings.get('HOST')}")
print(f"   Port: {db_settings.get('PORT')}")
print(f"   Password: {'***set***' if db_settings.get('PASSWORD') else '❌ NOT SET'}")
print("   " + "-"*60)

print("\n2. Testing Database Connection:")
try:
    # Test connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   ✅ Connected to PostgreSQL!")
        print(f"   ✅ Version: {version[0][:60]}...")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n3. Database Tables Found ({len(tables)}):")
            print("   " + "-"*60)
            for table in tables:
                print(f"   - {table[0]}")
            print("   " + "-"*60)
        else:
            print("\n3. No tables found (database is empty)")
            print("   ⚠️  Run 'python manage.py migrate' to create tables")
        
        print("\n" + "="*70)
        print("✅ DJANGO DATABASE CONNECTION SUCCESSFUL!")
        print("="*70)
        print("\nNext steps:")
        if not tables:
            print("  1. python manage.py migrate")
            print("  2. python manage.py createsuperuser")
            print("  3. python manage.py runserver")
        else:
            print("  python manage.py runserver")
        print("="*70 + "\n")
        
except Exception as e:
    print(f"   ❌ Connection failed!")
    print(f"   Error: {e}")
    print("\n   Troubleshooting:")
    print("   1. Check your .env file exists and has correct values")
    print("   2. Verify DATABASE settings in quiz_app/settings.py")
    print("   3. Make sure python-dotenv is installed: pip install python-dotenv")
    print("   4. Check if load_dotenv() is called in settings.py")
    sys.exit(1)