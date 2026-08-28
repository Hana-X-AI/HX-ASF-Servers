#!/usr/bin/env python3
"""Gordon Gate 7 fixture: minimal OTLP/HTTP capture collector.

Listens on 127.0.0.1:<port>, accepts every POST, appends the raw body to
<outfile> as one length-prefixed record per request, and answers 200 with an
empty JSON body. The telemetry exporter (OTLP/HTTP logs, gzip) must succeed
against it; test rows classify the captured frames (feedback vs session
records) without any cloud collector.

Usage: otlp_capture.py <port> <outfile>  (runs until SIGTERM)
"""
import http.server
import json
import struct
import sys
import threading


class Handler(http.server.BaseHTTPRequestHandler):
    outfile = None

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length)
        with open(self.outfile, "ab") as fh:
            fh.write(struct.pack("<QI", len(body), self.raw_requestline.__len__()))
            fh.write(self.path.encode() + b"\n")
            fh.write(body)
            fh.write(b"\n---\n")
        payload = json.dumps({}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def main():
    port, outfile = int(sys.argv[1]), sys.argv[2]
    Handler.outfile = outfile
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"OTLP-CAPTURE-READY {port}", flush=True)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
