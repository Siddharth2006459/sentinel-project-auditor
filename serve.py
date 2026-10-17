#!/usr/bin/env python3
"""SENTINEL's dependency-free, loopback-only development server."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import functools
import sys
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent / 'dist'
FILES = {'/', '/index.html', '/style.css', '/app.mjs', '/engine.mjs'}

class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.mjs': 'text/javascript'}
    def do_GET(self):
        if unquote(urlsplit(self.path).path) not in FILES:
            self.send_error(404, 'Not found')
            return
        super().do_GET()
    def do_HEAD(self):
        if unquote(urlsplit(self.path).path) not in FILES:
            self.send_error(404, 'Not found')
            return
        super().do_HEAD()
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Frame-Options', 'DENY')
        super().end_headers()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--open', action='store_true')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('Port must be between 1024 and 65535.')
    url = f'http://127.0.0.1:{args.port}/'
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), functools.partial(Handler, directory=str(ROOT)))
    except OSError as exc:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                existing = response.read(10000).decode('utf-8', errors='replace')
            if '<title>SENTINEL' in existing:
                print(f'SENTINEL is already running: {url}', flush=True)
                if args.open:
                    webbrowser.open(url)
                return
        except Exception:
            pass
        print(f'Could not start at {url}: {exc}. Try --port 4174.', file=sys.stderr)
        sys.exit(1)
    print(f'SENTINEL is running: {url}\nKeep this terminal open. Press Ctrl+C to stop.', flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
