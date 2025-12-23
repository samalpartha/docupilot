import os
import sys
import subprocess
import time
import re

def start_app():
    # 1. Start Streamlit in the background
    print("🚀 Starting Streamlit App...")
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "src/app.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for Streamlit to boot
    time.sleep(2)

    print("🔗 Creating Public Tunnel (via Serveo/SSH)...")
    # 2. Open SSH Tunnel to Serveo
    # ssh -R 80:localhost:8501 serveo.net
    tunnel_process = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8501", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"  # Text mode
    )

    print("\n" + "="*60)
    print("  WAITING FOR PUBLIC URL...")
    print("="*60 + "\n")

    # Serveo prints the URL to stdout
    public_url = None
    while True:
        line = tunnel_process.stdout.readline()
        if not line:
            break
        print(f"Tunnel Log: {line.strip()}")
        if "serveo.net" in line:
            # Extract URL
            # Example output: "Forwarding HTTP traffic from https://somename.serveo.net"
            match = re.search(r'(https?://[a-zA-Z0-9.-]+\.serveo\.net)', line)
            if match:
                public_url = match.group(1)
                print("\n" + "="*60)
                print(f"  🌟 YOUR APP IS LIVE HERE: {public_url}")
                print("="*60 + "\n")
                break
    
    if not public_url:
        print("❌ Could not get URL from Serveo. Trying backup (stdout check)...")

    # Keep alive
    try:
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("Stopping...")
        tunnel_process.terminate()
        streamlit_process.terminate()

if __name__ == "__main__":
    start_app()
