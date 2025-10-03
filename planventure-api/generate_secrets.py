#!/usr/bin/env python3
"""
Secret Key Generator for Planventure API
Run this script to generate secure secret keys for your .env file
"""

import secrets
import os
from datetime import datetime

def generate_secret_key(length=32):
    """Generate a cryptographically secure secret key"""
    return secrets.token_hex(length)

def generate_all_secrets():
    """Generate all required secret keys for the application"""
    print("🔐 Generating secure secret keys for Planventure API...")
    print("=" * 60)
    
    # Generate different keys
    secret_key = generate_secret_key(32)  # 64 characters
    jwt_secret = generate_secret_key(32)  # 64 characters
    
    # Display the keys
    print(f"SECRET_KEY='{secret_key}'")
    print(f"JWT_SECRET_KEY='{jwt_secret}'")
    print(f"DATABASE_URL='sqlite:///planventure.db'")
    print(f"CORS_ORIGINS='http://localhost:3000'")
    
    print("\n" + "=" * 60)
    print("📋 Copy the above lines to your .env file")
    print("⚠️  Keep these keys secure and never commit them to version control!")
    
    # Optionally write to .env file
    write_to_env = input("\n🤔 Do you want to automatically update your .env file? (y/n): ")
    
    if write_to_env.lower() in ['y', 'yes']:
        write_env_file(secret_key, jwt_secret)

def write_env_file(secret_key, jwt_secret):
    """Write the generated keys to .env file"""
    env_content = f"""# Planventure API Environment Variables
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SECRET_KEY='{secret_key}'
JWT_SECRET_KEY='{jwt_secret}'
DATABASE_URL='sqlite:///planventure.db'
CORS_ORIGINS='http://localhost:3000'
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Successfully updated .env file!")
        print("🔄 Restart your Flask application to use the new keys.")
    except Exception as e:
        print(f"❌ Error writing to .env file: {e}")
        print("Please manually copy the keys to your .env file.")

def generate_single_key():
    """Generate a single secret key"""
    key = generate_secret_key()
    print(f"🔑 Generated secret key: {key}")
    return key

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--single':
            generate_single_key()
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python generate_secrets.py        - Generate all keys for .env")
            print("  python generate_secrets.py --single   - Generate a single key")
            print("  python generate_secrets.py --help     - Show this help")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        generate_all_secrets()
