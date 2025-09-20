#!/usr/bin/env python3
"""
Debug script to help identify token issues in the browser
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.auth import AuthService
import jwt

async def debug_token_issue():
    """
    This script helps debug token issues that users might experience
    """
    print("🐛 Token Debugging Helper")
    print("=" * 40)
    
    # Check if there's a test user we can use
    test_national_id = input("Enter your national_id (or press Enter for test user): ").strip()
    if not test_national_id:
        test_national_id = "debug_user_123"
        test_password = "debug_password_123"
        
        # Create test user
        print(f"\n📝 Creating test user: {test_national_id}")
        from app.supabase_client import supabase_client as supabase
        try:
            supabase.table('users').delete().eq('national_id', test_national_id).execute()
        except:
            pass
        
        success = await AuthService.create_user(test_national_id, test_password)
        if not success:
            print("❌ Failed to create test user")
            return
        print("✅ Test user created")
    else:
        test_password = input("Enter your password: ").strip()
    
    # Authenticate and get token
    print(f"\n🔐 Authenticating user: {test_national_id}")
    user_info = await AuthService.authenticate_user(test_national_id, test_password)
    
    if not user_info:
        print("❌ Authentication failed - check your credentials")
        return
    
    token = user_info['access_token']
    print("✅ Authentication successful!")
    print(f"🎟️  Token: {token}")
    
    # Decode token to check contents
    print("\n🔍 Token Analysis:")
    try:
        # Decode without verification to see contents
        decoded = jwt.decode(token, options={"verify_signature": False})
        print(f"   Subject (user_id): {decoded.get('sub')}")
        print(f"   National ID: {decoded.get('national_id')}")
        print(f"   Expiration: {decoded.get('exp')}")
        
        import datetime
        if decoded.get('exp'):
            exp_time = datetime.datetime.fromtimestamp(decoded['exp'])
            now = datetime.datetime.now()
            if exp_time > now:
                print(f"   Token expires: {exp_time} (✅ Valid)")
            else:
                print(f"   Token expires: {exp_time} (❌ EXPIRED)")
    except Exception as e:
        print(f"   ❌ Token decode error: {e}")
    
    # Test token validation
    print("\n🧪 Testing Token Validation:")
    try:
        auth_header = f"Bearer {token}"
        current_user = await AuthService.get_current_user(auth_header)
        print(f"   ✅ Token validation successful")
        print(f"   Validated user: {current_user.get('national_id')}")
    except Exception as e:
        print(f"   ❌ Token validation failed: {e}")
    
    # Provide browser debugging info
    print("\n💻 Browser localStorage Fix:")
    print("=" * 40)
    print("If you get 'Could not validate credentials' error:")
    print("Open browser console (F12) and run these commands:")
    print()
    print("1. Clear corrupted token:")
    print("   localStorage.removeItem('authToken');")
    print()
    print("2. Set correct token (copy this exactly):")
    import json
    localStorage_cmd = f"localStorage.setItem('authToken', '{json.dumps(user_info)}');"
    print(f"   {localStorage_cmd}")
    print()
    print("3. Verify it worked:")
    print("   console.log(JSON.parse(localStorage.getItem('authToken')));")
    print()
    print("4. Refresh the page and try analyzing a mole again.")
    print()
    print("💡 Alternative: Simply log out and log back in!")
    print("=" * 40)
    
    # Clean up test user if created
    if test_national_id == "debug_user_123":
        try:
            from app.supabase_client import supabase_client as supabase
            supabase.table('users').delete().eq('national_id', test_national_id).execute()
            print("\n✅ Test user cleaned up")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(debug_token_issue())
