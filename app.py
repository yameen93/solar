from flask import Flask, redirect
import requests

app = Flask(__name__)

# GitHub RAW url of url.txt
URL_TXT_RAW = "https://raw.githubusercontent.com/yameen93/solar/main/url.txt"

@app.route("/")
def home():
    try:
        r = requests.get(URL_TXT_RAW, timeout=5)
        url = r.text.strip()

        if url.startswith("http"):
            return redirect(url, code=302)
        else:
            return "Tunnel URL not available", 503

    except Exception as e:
        return f"Error: {e}", 500


@app.route("/health")
def health():
    return "OK", 200
