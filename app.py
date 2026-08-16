"""
URL Shortener & Analytics Engine (FastAPI / Python)
"""

import hashlib
import time

class URLShortenerService:
    def __init__(self):
        self.db = {} # code -> { original_url, clicks, created_at }

    def shorten_url(self, original_url: str, custom_alias: str = None) -> dict:
        if not original_url or not (original_url.startswith('http://') or original_url.startswith('https://')):
            raise ValueError("Invalid URL format. Must start with http:// or https://")

        if custom_alias:
            alias = custom_alias.strip()
            if alias in self.db:
                raise ValueError("Custom alias already in use")
            code = alias
        else:
            code = hashlib.md5(f"{original_url}{time.time()}".encode('utf-8')).hexdigest()[:6]
        
        entry = {
            "code": code,
            "original_url": original_url,
            "short_url": f"http://short.ly/{code}",
            "clicks": 0,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.db[code] = entry
        return entry

    def redirect_code(self, code: str) -> str:
        if code in self.db:
            self.db[code]["clicks"] += 1
            return self.db[code]["original_url"]
        return None

    def get_analytics(self, code: str) -> dict:
        if code in self.db:
            return self.db[code]
        return None
