#!/usr/bin/env python3
"""Add the Theme panel to a live official Confirm UI without modifying ppt-master.

Run the official server first. This loopback presentation proxy forwards native
confirmation requests unchanged. --demo serves a clearly labelled read-only
component preview; it cannot create confirmation receipts.
"""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ASSETS = Path(__file__).resolve().parents[1] / 'confirm_ui'
MAX_BODY = 2 * 1024 * 1024


def request_native(base, path, method='GET', body=None, headers=None):
    forwarded = {k: v for k, v in (headers or {}).items() if k.lower() in ('content-type', 'origin', 'cookie', 'accept')}
    req = Request(base + path, data=body, headers=forwarded, method=method)
    try:
        response = urlopen(req, timeout=15)
    except HTTPError as error:
        response = error
    with response:
        return response.status, dict(response.headers), response.read()


def context(args):
    data = {'schema': 'ppt-master-themes.confirm-context.v1', 'theme': {'name': args.theme_name, 'workspace_root': str(args.theme_root)}, 'stage': 'stage1', 'demo': args.demo, 'applied': False}
    if args.demo:
        stage = 'stage2'
    else:
        status, _, raw = request_native(args.upstream, '/api/health')
        health = json.loads(raw)
        if status != 200 or health.get('service') != 'confirm_ui' or Path(health.get('project','')).resolve() != args.project:
            raise ValueError('native Confirm UI project/service changed')
        stage = 'stage2' if health.get('stage') in (2,'stage2') else 'stage1'
    data['stage'] = stage
    # Stage 1 uses the explicitly supplied label/root only, never theme configuration.
    if stage == 'stage1':
        return data
    file = args.project / 'analysis/theme_context.json'
    if file.exists():
        saved = json.loads(file.read_text(encoding='utf-8'))
        if Path(saved.get('theme',{}).get('workspace_root','')).resolve() != args.theme_root:
            raise ValueError('theme_context.json belongs to a different workspace')
        for key in ('application','source_palette','proposals','assets'):
            if key in saved:
                data[key] = saved[key]
        spec = saved.get('theme',{}).get('style_spec','')
        if spec:
            relative = Path(spec)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('style_spec must be workspace-relative')
            source, installed = args.theme_root / relative, args.project / relative
            if source.is_file() and installed.is_file():
                data['applied'] = hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(installed.read_bytes()).digest()
    return data


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pm', type=Path, required=True)
    p.add_argument('--project', type=Path, required=True)
    p.add_argument('--theme-root', type=Path, required=True)
    p.add_argument('--theme-name', required=True, help='explicit candidate label; no pre-Stage-1 theme inspection')
    p.add_argument('--upstream', default='http://127.0.0.1:5050')
    p.add_argument('--port', type=int, default=5070)
    p.add_argument('--demo', action='store_true')
    args = p.parse_args()
    args.pm, args.project, args.theme_root = (v.expanduser().resolve() for v in (args.pm,args.project,args.theme_root))
    if not args.project.is_dir():
        p.error('project directory is missing')
    check = subprocess.run([sys.executable,str(args.pm/'scripts/attribution_guard.py')])
    if check.returncode:
        return check.returncode
    url = urlsplit(args.upstream)
    if url.scheme != 'http' or url.hostname != '127.0.0.1' or not url.port or url.path not in ('','/') or url.query or url.fragment or url.username:
        p.error('--upstream must be an exact http://127.0.0.1:PORT origin')
    args.upstream = args.upstream.rstrip('/')
    if not 1 <= args.port <= 65535 or args.port == url.port:
        p.error('choose a valid distinct proxy port')
    context(args)  # Fail before binding if the upstream identifies a different project.

    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, raw, content_type='application/json; charset=utf-8', headers=None):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control','no-store')
            for key,value in (headers or {}).items():
                if key.lower() in ('set-cookie','location'):
                    self.send_header(key,value)
            self.end_headers()
            self.wfile.write(raw)

        def handle_request(self):
            parsed = urlsplit(self.path)
            # Keep the same local-only boundary as the official server.
            if self.headers.get('Host','').split(':')[0] not in ('127.0.0.1','localhost') or parsed.scheme or parsed.netloc:
                return self.reply(403,b'{"error":"local requests only"}')
            origin = self.headers.get('Origin')
            if origin and urlsplit(origin).hostname not in ('127.0.0.1','localhost'):
                return self.reply(403,b'{"error":"local origin required"}')
            try:
                if self.command == 'GET' and parsed.path == '/theme-extension/context':
                    return self.reply(200,json.dumps(context(args),ensure_ascii=False).encode())
                if self.command == 'GET' and parsed.path in ('/theme-extension/panel.js','/theme-extension/panel.css'):
                    name = parsed.path.rsplit('/',1)[1]
                    return self.reply(200,(ASSETS/name).read_bytes(),'text/javascript' if name.endswith('.js') else 'text/css')
                if args.demo:
                    if self.command == 'GET' and parsed.path == '/':
                        return self.reply(200,(ASSETS/'demo.html').read_bytes(),'text/html; charset=utf-8')
                    return self.reply(405,b'{"error":"component demo: no confirmation or project writes"}')
                length = int(self.headers.get('Content-Length','0'))
                if length < 0 or length > MAX_BODY:
                    return self.reply(413,b'{"error":"body too large"}')
                body = self.rfile.read(length) if length else None
                status, headers, raw = request_native(args.upstream,self.path,self.command,body,self.headers)
                content_type = headers.get('Content-Type','application/octet-stream')
                if self.command == 'GET' and parsed.path == '/' and status == 200:
                    html = raw.decode('utf-8')
                    if 'id="sections"' not in html or '/static/app.js' not in html:
                        return self.reply(502,b'{"error":"unsupported official UI interface; use its original URL"}')
                    html = html.replace('</head>','<link rel="stylesheet" href="/theme-extension/panel.css"></head>')
                    html = html.replace('</body>','<script src="/theme-extension/panel.js"></script></body>')
                    raw = html.encode('utf-8')
                return self.reply(status,raw,content_type,headers)
            except (ValueError,OSError,URLError) as error:
                return self.reply(502,json.dumps({'error':str(error)}).encode())

        do_GET = handle_request
        do_POST = handle_request

    server = ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'Theme panel: http://127.0.0.1:{args.port} ({"component demo; cannot confirm" if args.demo else "official Confirm UI + theme presentation layer"})',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
