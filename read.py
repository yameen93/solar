
import subprocess
import time
import re
import os

# ================= CONFIG =================
PORT = "80"                      # Apache = 80, PHP = 8000
CHECK_INTERVAL = 20              # seconds
REPO_PATH = "/home/yameen/solar"
URL_FILE = "url.txt"

GITHUB_TOKEN = ""
GITHUB_REPO = "yameen93/solar"
# =========================================


cloudflared_process = None
current_url = ""


def start_tunnel():
    global cloudflared_process

    print("🚀 Starting Cloudflare Tunnel...")
    cloudflared_process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in cloudflared_process.stdout:
        print(line.strip())
        match = re.search(r"https://.*?\.trycloudflare\.com", line)
        if match:
            return match.group(0)

    return None


def tunnel_alive():
    if cloudflared_process is None:
        return False
    return cloudflared_process.poll() is None


def update_github(url):
    print("📤 Updating GitHub URL...")
    os.chdir(REPO_PATH)

    with open(URL_FILE, "w") as f:
        f.write(url)

    subprocess.run(["git", "add", URL_FILE])
    subprocess.run(["git", "commit", "-m", "Update Cloudflare tunnel URL"])

    #push_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    #subprocess.run(["git", "push", push_url, "main"])
    subprocess.run(["git", "push", "origin", "main"])


# ================= MAIN LOOP =================
while True:
    if not tunnel_alive():
        url = start_tunnel()

        if url:
            if url != current_url:
                current_url = url
                print(f"🌐 New URL: {url}")
                update_github(url)
        else:
            print("❌ Tunnel start failed")

    time.sleep(CHECK_INTERVAL)
