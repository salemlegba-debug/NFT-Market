"""Supervisor for NFT Market Discord Bot.

Ensures dependencies are available and keeps main.py running continuously.
"""
import os
import subprocess
import sys
import time

def ensure_dependencies() -> None:
    try:
        import discord
        import aiohttp
        import nacl
        return
    except ImportError:
        print("[bot_runner] Checking python dependencies from requirements.txt...")
        # Verify if pip is installed
        check_pip = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
        if check_pip.returncode != 0:
            print("[bot_runner] pip not found, bootstrapping pip via get-pip.py...")
            bootstrap = subprocess.run(
                ["curl", "-sS", "https://bootstrap.pypa.io/get-pip.py", "-o", "/tmp/get-pip.py"],
                capture_output=True,
                text=True,
            )
            if bootstrap.returncode == 0:
                subprocess.run(
                    [sys.executable, "/tmp/get-pip.py", "--break-system-packages", "--no-warn-script-location"],
                    capture_output=True,
                    text=True,
                )

        res = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            print(f"[bot_runner] pip install warning/error:\n{res.stderr}", file=sys.stderr)
        else:
            print("[bot_runner] Dependencies successfully verified.")

def run_bot() -> None:
    token = os.getenv("DISCORD_TOKEN", "").strip()
    if not token:
        print("[bot_runner] DISCORD_TOKEN is not configured in environment.", file=sys.stderr)
        return

    ensure_dependencies()

    while True:
        print("[bot_runner] Starting main.py...")
        process = subprocess.Popen([sys.executable, "main.py"])
        try:
            exit_code = process.wait()
            print(f"[bot_runner] main.py exited with code {exit_code}. Restarting in 3 seconds...")
        except KeyboardInterrupt:
            process.terminate()
            break
        time.sleep(3)

if __name__ == "__main__":
    run_bot()
