#!/usr/bin/env python3
"""
Screen Sharer Client
Run this on the machine whose screen you want to share.
It captures the screen and uploads frames to the server.

Usage:
    python sharer.py --server http://SERVER-IP:6100
"""

import argparse
import base64
import io
import sys
import time
import json

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    sys.exit(1)

if sys.platform in ["win32", "darwin"]:
    from PIL import ImageGrab as ig
else:
    import pyscreenshot as ig

FPS = 10


def capture_and_upload(server_url):
    upload_url = server_url.rstrip('/') + '/upload'

    print(f"Sharing screen to: {upload_url}")
    print(f"FPS: {FPS}")
    print("Press Ctrl+C to stop sharing.\n")

    while True:
        try:
            # Capture screen
            if sys.platform in ["win32", "darwin"]:
                im = ig.grab()
            else:
                im = ig.grab(childprocess=False)

            # Convert to JPEG base64
            buf = io.BytesIO()
            im.convert("RGB").save(buf, format="jpeg", quality=75, progressive=True)
            frame_b64 = base64.b64encode(buf.getvalue()).decode()

            # Upload to server
            resp = requests.post(
                upload_url,
                json={"frame": frame_b64},
                timeout=5
            )

            if resp.status_code != 200:
                print(f"Upload error: {resp.status_code}")

        except requests.exceptions.ConnectionError:
            print("Cannot connect to server. Retrying...")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1.0 / FPS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Share your screen to the server")
    parser.add_argument("-s", "--server", required=True, help="Server URL, e.g. http://SERVER-IP:6100")
    parser.add_argument("-f", "--fps", type=int, default=10, help="Frames per second (default: 10)")

    args = parser.parse_args()
    FPS = args.fps

    capture_and_upload(args.server)
