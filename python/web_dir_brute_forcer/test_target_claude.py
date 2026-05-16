#!/usr/bin/env python3
"""
Fake Target Server for Directory Brute Forcing Practice
Runs on localhost:8000

Simulates a realistic web server with:
- Common paths that return 200 OK
- Forbidden paths (403)
- Redirects (301/302)
- Realistic 404 responses
- Rate limiting simulation
- Basic auth on some paths
- Random response delays
"""

import http.server
import json
import time
import random
import base64
from urllib.parse import urlparse

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

HOST = "localhost"
PORT = 8000

# Paths that return 200 OK with content
FOUND_PATHS = {
    "/": "text/html",
    "/index.html": "text/html",
    "/index.php": "text/html",
    "/about": "text/html",
    "/about.html": "text/html",
    "/contact": "text/html",
    "/login": "text/html",
    "/login.php": "text/html",
    "/register": "text/html",
    "/dashboard": "text/html",
    "/admin": "text/html",          # juicy!
    "/admin/": "text/html",
    "/admin/index.php": "text/html",
    "/admin/login.php": "text/html",
    "/api": "application/json",
    "/api/v1": "application/json",
    "/api/v1/users": "application/json",
    "/api/v1/status": "application/json",
    "/backup": "text/html",         # very juicy!
    "/backup.zip": "application/zip",
    "/config": "text/html",
    "/robots.txt": "text/plain",
    "/sitemap.xml": "application/xml",
    "/.env": "text/plain",          # super juicy!
    "/wp-admin": "text/html",
    "/wp-login.php": "text/html",
    "/phpmyadmin": "text/html",
    "/phpmyadmin/": "text/html",
    "/server-status": "text/html",
    "/uploads": "text/html",
    "/uploads/": "text/html",
    "/static": "text/html",
    "/static/": "text/html",
    "/css": "text/html",
    "/js": "text/html",
    "/images": "text/html",
    "/files": "text/html",
    "/download": "text/html",
    "/docs": "text/html",
    "/swagger": "text/html",
    "/swagger-ui.html": "text/html",
    "/graphql": "application/json",
    "/health": "application/json",
    "/metrics": "text/plain",
    "/debug": "text/html",
    "/test": "text/html",
    "/old": "text/html",
    "/dev": "text/html",
    "/secret": "text/html",
    "/private": "text/html",
    "/hidden": "text/html",
}

# Paths that return 403 Forbidden
FORBIDDEN_PATHS = {
    "/.git",
    "/.git/",
    "/.git/config",
    "/.git/HEAD",
    "/.htaccess",
    "/.htpasswd",
    "/etc/passwd",
    "/proc/self/environ",
    "/admin/config",
    "/admin/users",
    "/private/keys",
    "/internal",
    "/internal/",
}

# Paths that redirect
REDIRECT_PATHS = {
    "/home": "/",
    "/admin/dashboard": "/admin",
    "/api/docs": "/swagger",
    "/wp-content/uploads": "/uploads",
    "/panel": "/admin",
}

# Paths requiring basic auth (username: admin, password: secret)
AUTH_PATHS = {
    "/admin/settings",
    "/admin/panel",
    "/server-info",
    "/phpinfo.php",
}

# Simulate rate limiting: requests per second threshold
RATE_LIMIT_THRESHOLD = 50  # requests per second before triggering 429
request_timestamps = []

# ──────────────────────────────────────────────
# HTML Templates
# ──────────────────────────────────────────────

def html_page(title, body, status_code=200):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - FakeCorpApp</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }} a {{ color: #0066cc; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #e0f0ff; color: #0055aa; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        {body}
        <hr>
        <small>FakeCorpApp v2.4.1 | Apache/2.4.51 (Ubuntu)</small>
    </div>
</body>
</html>"""

PAGE_CONTENT = {
    "/": html_page("Welcome", "<p>Welcome to FakeCorpApp. <a href='/login'>Login</a> | <a href='/about'>About</a></p><p>Employee portal: <a href='/dashboard'>Dashboard</a></p>"),
    "/login": html_page("Login", "<form><input type='text' placeholder='Username'><br><input type='password' placeholder='Password'><br><button>Login</button></form>"),
    "/admin": html_page("Admin Panel", "<p>Administration area. Restricted access.</p><ul><li><a href='/admin/users'>Users</a></li><li><a href='/admin/settings'>Settings</a></li></ul>"),
    "/robots.txt": "User-agent: *\nDisallow: /admin\nDisallow: /backup\nDisallow: /.env\nDisallow: /private\nDisallow: /config\n",
    "/.env": "APP_ENV=production\nDB_HOST=localhost\nDB_USER=root\nDB_PASS=Sup3rS3cret!\nSECRET_KEY=a1b2c3d4e5f6g7h8\nAWS_KEY=AKIA0000FAKE0000XXXX\nAWS_SECRET=fakeAWSsecretKeyForTestingOnly\n",
    "/api/v1/status": json.dumps({"status": "ok", "version": "1.4.2", "uptime": 99823, "db": "connected"}),
    "/api/v1/users": json.dumps({"users": [{"id": 1, "name": "admin", "role": "superadmin"}, {"id": 2, "name": "jdoe", "role": "user"}]}),
    "/health": json.dumps({"healthy": True, "checks": {"db": "ok", "cache": "ok", "queue": "ok"}}),
    "/metrics": "# HELP http_requests_total Total HTTP requests\nhttp_requests_total{method=\"GET\"} 14892\nhttp_requests_total{method=\"POST\"} 3471\n",
    "/sitemap.xml": '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>http://localhost:8000/</loc></url><url><loc>http://localhost:8000/about</loc></url></urlset>',
}

# ──────────────────────────────────────────────
# Request Handler
# ──────────────────────────────────────────────

class FakeTargetHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        path = self.path
        code = args[1] if len(args) > 1 else "???"
        color = {
            "200": "\033[92m",  # green
            "301": "\033[94m",  # blue
            "302": "\033[94m",
            "401": "\033[93m",  # yellow
            "403": "\033[91m",  # red
            "404": "\033[90m",  # gray
            "429": "\033[95m",  # magenta
        }.get(str(code), "\033[0m")
        reset = "\033[0m"
        print(f"  {color}[{code}]{reset} {self.address_string()} → {path}")

    def check_rate_limit(self):
        now = time.time()
        request_timestamps.append(now)
        # Keep only timestamps from last second
        cutoff = now - 1.0
        while request_timestamps and request_timestamps[0] < cutoff:
            request_timestamps.pop(0)
        return len(request_timestamps) > RATE_LIMIT_THRESHOLD

    def check_basic_auth(self):
        auth_header = self.headers.get("Authorization", "")
        if not auth_header.startswith("Basic "):
            return False
        try:
            decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
            return decoded == "admin:secret"
        except Exception:
            return False

    def send_404(self):
        body = html_page("404 Not Found", "<p>The page you requested could not be found.</p>")
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(body.encode()))
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        # Simulate realistic variable response time
        time.sleep(random.uniform(0.01, 0.08))

        path = urlparse(self.path).path

        # Rate limiting
        if self.check_rate_limit():
            body = json.dumps({"error": "Too many requests. Slow down."})
            self.send_response(429)
            self.send_header("Content-Type", "application/json")
            self.send_header("Retry-After", "1")
            self.send_header("Content-Length", len(body.encode()))
            self.end_headers()
            self.wfile.write(body.encode())
            return

        # Auth-required paths
        if path in AUTH_PATHS:
            if not self.check_basic_auth():
                self.send_response(401)
                self.send_header("WWW-Authenticate", 'Basic realm="Restricted Area"')
                self.send_header("Content-Type", "text/html")
                body = html_page("401 Unauthorized", "<p>Authentication required.</p>")
                self.send_header("Content-Length", len(body.encode()))
                self.end_headers()
                self.wfile.write(body.encode())
                return
            # Authenticated — fall through to found path logic

        # Forbidden paths
        if path in FORBIDDEN_PATHS:
            body = html_page("403 Forbidden", "<p>You don't have permission to access this resource.</p>")
            self.send_response(403)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(body.encode()))
            self.end_headers()
            self.wfile.write(body.encode())
            return

        # Redirect paths
        if path in REDIRECT_PATHS:
            target = REDIRECT_PATHS[path]
            self.send_response(301)
            self.send_header("Location", target)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        # Found paths
        if path in FOUND_PATHS:
            content_type = FOUND_PATHS[path]
            body = PAGE_CONTENT.get(path)
            if body is None:
                # Generate generic page
                body = html_page(path.strip("/").capitalize() or "Home",
                                 f"<p>Resource: <code>{path}</code></p><p class='badge'>200 OK</p>")
            if isinstance(body, str):
                body = body.encode()

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(body))
            self.send_header("Server", "Apache/2.4.51 (Ubuntu)")
            self.send_header("X-Powered-By", "PHP/8.1.2")
            self.end_headers()
            self.wfile.write(body)
            return

        # Default: 404
        self.send_404()

    def do_POST(self):
        path = urlparse(self.path).path
        if path in ("/login", "/login.php", "/api/v1/users"):
            body = json.dumps({"error": "Invalid credentials"})
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(body.encode()))
            self.end_headers()
            self.wfile.write(body.encode())
        elif path in FOUND_PATHS:
            body = json.dumps({"status": "ok"})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(body.encode()))
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_404()

# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    server = http.server.HTTPServer((HOST, PORT), FakeTargetHandler)

    print(f"""
\033[1m╔══════════════════════════════════════════╗
║     Fake Target Server — Ready to Fuzz   ║
╚══════════════════════════════════════════╝\033[0m

  \033[94mListening on:\033[0m  http://{HOST}:{PORT}

  \033[92m[200 OK]\033[0m      {len(FOUND_PATHS)} discoverable paths
  \033[91m[403]\033[0m         {len(FORBIDDEN_PATHS)} forbidden paths
  \033[94m[301]\033[0m         {len(REDIRECT_PATHS)} redirects
  \033[93m[401]\033[0m         {len(AUTH_PATHS)} auth-protected paths  (admin:secret)
  \033[95m[429]\033[0m         Rate limit at >{RATE_LIMIT_THRESHOLD} req/s

  Press Ctrl+C to stop.
──────────────────────────────────────────────
""")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[93mServer stopped.\033[0m")