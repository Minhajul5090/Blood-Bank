#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for Django deployment
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure secret key for Django"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("🔑 Generating secure SECRET_KEY for Railway...")
    print()
    
    # Generate the secret key
    secret_key = generate_secret_key()
    
    print("✅ Generated SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")
    print()
    
    print("📋 Copy this to your Railway environment variables:")
    print("Key: SECRET_KEY")
    print(f"Value: {secret_key}")
    print()
    
    print("⚠️  Important:")
    print("- Copy the entire key (no extra spaces)")
    print("- Don't include quotes around the value")
    print("- Add it manually in Railway dashboard")
    print("- Keep this key secure and don't share it") 