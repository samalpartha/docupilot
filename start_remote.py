import os
import sys
import subprocess
import time
import re

def start_app():
    # 1. Start Streamlit in the background with Native Port 8000
    print(f"🚀 Starting Streamlit App via {sys.executable} on Port 8000...")
    
    # NOVITA NATIVE PORT IS 8000
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "src/app.py", "--server.port", "8000", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for Streamlit to boot
    time.sleep(2)

    print("\n" + "="*60)
    print("  ✅ APP FULLY STARTED ON PORT 8000")
    print("  👉 GO TO NOVITA DASHBOARD (Web Browser)")
    print("  👉 Click the button: 'Connect to HTTP Service [Port 8000]'")
    print("="*60 + "\n")

    print("🔗 Creating Backup Public Tunnel (via Serveo)...")
    # 2. Open SSH Tunnel to Serveo (Forwarding localhost:8000)
    tunnel_process = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8000", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"  # Text mode
    )

    print("  (Waiting for backup tunnel URL...)")
    # Serveo prints the URL to stdout
    public_url = None
    while True:
        line = tunnel_process.stdout.readline()
        if not line:
            break
        
        # Check for URL in output
        if "Forwarding HTTP traffic" in line:
            # Match .serveo.net OR .serveousercontent.com
            match = re.search(r'(https?://[a-zA-Z0-9.-]+(?:\.serveo\.net|\.serveousercontent\.com))', line)
            if match:
                public_url = match.group(1)
                print("\n" + "-"*60)
                print(f"  Backup URL: {public_url}")
                print("-"*60 + "\n")
                break
    
    if not public_url:
        print("❌ Could not get Backup URL from Serveo. Please use the Novita Dashboard button.")

    # Keep alive
    try:
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("Stopping...")
        tunnel_process.terminate()
        streamlit_process.terminate()

if __name__ == "__main__":
    start_app()
