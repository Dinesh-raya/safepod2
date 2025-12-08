"""
Simple test script to verify imports work correctly
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("Testing imports...")

try:
    from app.config import config
    print("✓ Config imported successfully")
    
    print("Config values:")
    print(f"  SUPABASE_URL: {getattr(config, 'SUPABASE_URL', 'NOT FOUND')}")
    print(f"  SUPABASE_KEY: {getattr(config, 'SUPABASE_KEY', 'NOT FOUND')}")
    print(f"  SUPABASE_SERVICE_KEY: {getattr(config, 'SUPABASE_SERVICE_KEY', 'NOT FOUND')}")
    print(f"  SESSION_SECRET: {getattr(config, 'SESSION_SECRET', 'NOT FOUND')}")
    
    from app.services.auth_service import auth_service
    print("✓ Auth service imported successfully")
    
    from app.services.supabase_client import supabase_client
    print("✓ Supabase client imported successfully")
    
    print("All imports successful!")
    
except Exception as e:
    print(f"✗ Error importing modules: {e}")
    import traceback
    traceback.print_exc()