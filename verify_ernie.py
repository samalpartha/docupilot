import os
import erniebot
from dotenv import load_dotenv

load_dotenv()

def verify_ernie():
    token = os.getenv('ERNIE_ACCESS_TOKEN')
    print(f"Testing ERNIE with token: {token[:10]}...")
    
    erniebot.api_type = 'aistudio'
    erniebot.access_token = token
    
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=[{'role': 'user', 'content': 'Hello, are you working?'}],
            temperature=0.1
        )
        print("✅ ERNIE (Baidu) Response:", response.get_result())
    except Exception as e:
        print(f"❌ ERNIE (Baidu) Failed: {e}")

if __name__ == "__main__":
    verify_ernie()
