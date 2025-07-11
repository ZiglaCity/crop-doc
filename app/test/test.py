import requests
from supabase import create_client
from uuid import uuid4
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

API_URL = "http://localhost:8000/scan"

def scan(
        headers,
        image_url = "https://content.peat-cloud.com/w800/cassava-mosaic-disease-manioc-1561129470.jpg"
    ):
    # image_url = "https://content.peat-cloud.com/w800/cassava-mosaic-disease-manioc-1561129470.jpg"

    img_response = requests.get(image_url)
    img_bytes = img_response.content

    files = {
        "file": ("cassava.jpg", img_bytes, "image/jpeg")
    }

    if headers:
        response = requests.post(API_URL, headers=headers, files=files)
    else:
        response = requests.post(API_URL, files=files)
        

    print("Status Code:", response.status_code)
    print("Prediction Result:", response.json())
    return response



def test_signup_signin_and_request():
    email = f"test_{uuid4().hex[:8]}@example.com"
    password = "StrongTestPassword123!"

    create_result = supabase.auth.admin.create_user({
        "email": email,
        "password": password,
        "email_confirm": True
    })

    if not create_result.user:
        raise Exception("User creation failed")

    print("User created:", create_result.user.email)

    signin_result = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if not signin_result.session or not signin_result.session.access_token:
        raise Exception("Sign-in failed")

    jwt_token = signin_result.session.access_token
    print("JWT:", jwt_token)

    # Step 3: Send request with JWT in Authorization header
    headers = {
        "Authorization": f"Bearer {jwt_token} "
    }

    response = scan(headers=headers)

    print("Response status:", response.status_code)
    print("Response body:", response.text)


test_signup_signin_and_request()