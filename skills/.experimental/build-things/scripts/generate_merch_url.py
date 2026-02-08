#!/usr/bin/env python3
"""Generate a Super Bowl merch redemption URL.

Prints only the final URL; no browser/open calls.
"""

import base64
import hashlib
import hmac
import sys
import time
import urllib.parse

SECRET_KEY = "dfc92bc5e95825103283f01c2aa6ca7fe7f6ffc31778ea82c354785c73b0858c"
BASE_URL = "https://www.openai.com/codex/youcanjustbuildthings"


def _urlsafe_b64(data: bytes) -> str:
    # URL-safe, no padding, ASCII-only.
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def generate_token(ts: int, email: str) -> str:
    msg = f"{ts}:{email}".encode("ascii")
    key = SECRET_KEY.encode("ascii")
    sig = hmac.new(key, msg, hashlib.sha256).digest()
    return f"{ts}.{_urlsafe_b64(sig)}"


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: missing email. Usage: generate_merch_url.py <email>", file=sys.stderr)
        raise SystemExit(2)
    ts = int(time.time())
    email = sys.argv[1].strip().lower()
    token = generate_token(ts, email)
    encoded_email = urllib.parse.quote(email, safe="")
    print(f"{BASE_URL}?t={token}&e={encoded_email}")


if __name__ == "__main__":
    main()
