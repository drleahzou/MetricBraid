#!/usr/bin/env python3
"""Oura API v2 OAuth2 helper — no third-party dependencies.

Oura deprecated Personal Access Tokens in Dec 2025; newly created PATs return
401. OAuth2 is the only path that works for a new setup.

    python3 scripts/oura_auth.py login    # one-time browser authorization
    python3 scripts/oura_auth.py token    # print a valid access token (auto-refreshes)

Typical use, e.g. in your shell profile:

    export OURA_ACCESS_TOKEN="$(python3 /path/to/scripts/oura_auth.py token)"

Requires OURA_CLIENT_ID and OURA_CLIENT_SECRET from an application you
register at https://cloud.ouraring.com/applications with the redirect URI
set to exactly http://localhost:8080/callback
"""

import http.server
import json
import os
import secrets
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

AUTHORIZE_URL = "https://cloud.ouraring.com/oauth/authorize"
TOKEN_URL = "https://api.ouraring.com/oauth/token"
REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "email personal daily heartrate workout tag session spo2"

TOKEN_FILE = Path.home() / ".oura-mcp" / "tokens.json"
# Refresh a little early so a long session doesn't expire mid-flight.
EXPIRY_MARGIN_SECONDS = 120


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def credentials():
    cid = os.environ.get("OURA_CLIENT_ID")
    secret = os.environ.get("OURA_CLIENT_SECRET")
    if not cid or not secret:
        die(
            "set OURA_CLIENT_ID and OURA_CLIENT_SECRET.\n"
            "Register an app at https://cloud.ouraring.com/applications with\n"
            f"redirect URI exactly: {REDIRECT_URI}"
        )
    return cid, secret


def post_token(payload):
    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        die(f"token endpoint returned HTTP {e.code}: {e.read().decode()[:400]}")


def save(tok):
    import time

    # Store an absolute expiry so `token` can decide without a network call.
    tok["expires_at"] = time.time() + int(tok.get("expires_in", 86400))
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tok, indent=2))
    TOKEN_FILE.chmod(0o600)


def login():
    cid, secret = credentials()
    state = secrets.token_urlsafe(16)
    result = {}
    done = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            ok = "code" in result and result.get("state") == state
            self.wfile.write(
                b"<h2>Authorized. You can close this tab.</h2>"
                if ok
                else b"<h2>Authorization failed. Check the terminal.</h2>"
            )
            done.set()

        def log_message(self, *a):  # keep the console quiet
            pass

    server = http.server.HTTPServer(("localhost", 8080), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    url = f"{AUTHORIZE_URL}?" + urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": cid,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
            "state": state,
        }
    )
    print("Opening your browser to authorize...\nIf it doesn't open:\n  " + url)
    webbrowser.open(url)

    if not done.wait(timeout=300):
        die("timed out waiting for the browser redirect")
    server.shutdown()

    if result.get("state") != state:
        die("state mismatch — possible CSRF, aborting")
    if "code" not in result:
        die(f"no authorization code returned: {result}")

    tok = post_token(
        {
            "grant_type": "authorization_code",
            "code": result["code"],
            "redirect_uri": REDIRECT_URI,
            "client_id": cid,
            "client_secret": secret,
        }
    )
    save(tok)
    print(f"\nSaved to {TOKEN_FILE}")
    print("Now run:  export OURA_ACCESS_TOKEN=\"$(python3 scripts/oura_auth.py token)\"")


def token():
    import time

    if not TOKEN_FILE.exists():
        die(f"no saved token at {TOKEN_FILE} — run: python3 {sys.argv[0]} login")
    tok = json.loads(TOKEN_FILE.read_text())

    if time.time() < tok.get("expires_at", 0) - EXPIRY_MARGIN_SECONDS:
        print(tok["access_token"])
        return

    cid, secret = credentials()
    refresh = tok.get("refresh_token")
    if not refresh:
        die("saved token has no refresh_token — run `login` again")
    new = post_token(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh,
            "client_id": cid,
            "client_secret": secret,
        }
    )
    # Oura refresh tokens are SINGLE USE and are invalidated once redeemed.
    # The response carries a fresh one; persist it immediately or the next
    # refresh fails and you have to re-run `login`.
    if "refresh_token" not in new:
        new["refresh_token"] = refresh
    save(new)
    print(new["access_token"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "login":
        login()
    elif cmd == "token":
        token()
    else:
        print(__doc__)
        sys.exit(1)
