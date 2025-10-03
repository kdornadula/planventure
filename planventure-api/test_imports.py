try:
    from routes.auth import auth_bp
    print("✅ Auth routes imported successfully")
except Exception as e:
    print(f"❌ Auth import error: {e}")

try:
    from routes.protected_example import protected_bp
    print("✅ Protected routes imported successfully")
except Exception as e:
    print(f"❌ Protected routes import error: {e}")

try:
    from utils.middleware import auth_required
    print("✅ Middleware imported successfully")
except Exception as e:
    print(f"❌ Middleware import error: {e}")
