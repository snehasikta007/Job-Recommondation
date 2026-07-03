import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "")
print("Key length:", len(api_key))

try:
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello"
    )
    print("Response:", response.text)
except Exception as e:
    print("Error with genai:", e)

try:
    import google.generativeai as genai_old
    genai_old.configure(api_key=api_key)
    model = genai_old.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print("Old Response:", response.text)
except Exception as e:
    print("Error with generativeai:", e)
