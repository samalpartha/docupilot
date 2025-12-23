import os
import sys
import subprocess
import time

def install_ngrok():
    print("Installing pyngrok...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])

def start_app():
    try:
        from pyngrok import ngrok
    except ImportError:
        install_ngrok()
        from pyngrok import ngrok

    # 1. Kill any existing ngrok processes
    ngrok.kill()

    # 2. Start Streamlit in the background
    print("🚀 Starting Streamlit App...")
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "src/app.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 3. Open Tunnel
    # Check if NGROK_AUTHTOKEN is set, if not warn but try anyway (anonymous tunnels might have limits)
    token = os.getenv("NGROK_AUTHTOKEN")
    if token:
        ngrok.set_auth_token(token)
    else:
        print("⚠️  No NGROK_AUTHTOKEN found. Session might be limited to 2 hours.")

    print("🔗 Creating Public Tunnel...")
    try:
        public_url = ngrok.connect(8501).public_url
        print("\n" + "="*60)
        print(f"  🌟 YOUR APP IS LIVE HERE: {public_url}")
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Failed to create tunnel: {e}")
        return

    # Keep alive
    try:
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("Stopping...")
        ngrok.kill()
        streamlit_process.terminate()

if __name__ == "__main__":
    start_app()
