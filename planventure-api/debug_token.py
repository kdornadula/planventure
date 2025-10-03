import os
from dotenv import load_dotenv
import jwt as pyjwt

load_dotenv()

# Your token from Bruno environment (copy the actual token value)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1OTQ4OTYzNCwianRpIjoiMjExNTc4NjMtMGRhZi00NWViLTg0MjItMDM5NWIxYTkyNWY3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NiwibmJmIjoxNzU5NDg5NjM0LCJleHAiOjE3NTk0OTMyMzQsInVzZXJfaWQiOjYsImVtYWlsIjoiZ2F5YUBleGFtcGxlLmNvbSIsImlzX2FjdGl2ZSI6dHJ1ZX0.YpKelPYe_Opfr0dsOqiVZRAEVdRXbnk3f39CleljPs8"

try:
    # Decode the token
    payload = pyjwt.decode(
        token,
        os.getenv('JWT_SECRET_KEY'),
        algorithms=['HS256']
    )
    
    print("✅ Token decoded successfully!")
    print(f"🔍 Payload: {payload}")
    print(f"🔍 Subject (user_id): {payload.get('sub')} (type: {type(payload.get('sub'))})")
    print(f"🔍 User ID field: {payload.get('user_id')} (type: {type(payload.get('user_id'))})")
    
except Exception as e:
    print(f"❌ Token decode error: {e}")
