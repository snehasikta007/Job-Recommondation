import os
import django
import sys
import json

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_recommender.settings")
sys.path.insert(0, r"d:\Job- Recomendation System")
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()

def test_login_json():
    print("Testing Login (JSON)...")
    payload = {'email': 'test@gmail.com', 'password': 'password123'}
    # Ensure user exists for test
    User.objects.filter(email='test@gmail.com').delete()
    User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='password123')
    
    response = client.post('/login/', data=json.dumps(payload), content_type='application/json')
    print(f"Status: {response.status_code}")
    print(f"Content: {response.content.decode()}")
    assert response.status_code == 200
    assert 'success' in response.content.decode()

def test_login_form():
    print("Testing Login (Form)...")
    payload = {'email': 'test@gmail.com', 'password': 'password123'}
    response = client.post('/login/', data=payload)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.content.decode()}")
    assert response.status_code == 200
    assert 'success' in response.content.decode()

def test_register_json():
    print("Testing Register (JSON)...")
    User.objects.filter(email='newuser@gmail.com').delete()
    User.objects.filter(username='newuser@gmail.com').delete()
    payload = {
        'full_name': 'New User',
        'email': 'newuser@gmail.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'phone': '1234567890'
    }
    response = client.post('/register/', data=json.dumps(payload), content_type='application/json')
    print(f"Status: {response.status_code}")
    print(f"Content: {response.content.decode()}")
    assert response.status_code == 200
    assert 'success' in response.content.decode()

if __name__ == "__main__":
    try:
        test_login_json()
        print("-" * 20)
        test_login_form()
        print("-" * 20)
        test_register_json()
        print("ALL TESTS PASSED!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"TEST FAILED: {str(e)}")
        sys.exit(1)
