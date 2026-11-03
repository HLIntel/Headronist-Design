"""Opt-in localhost read-only API. No remote binding, no file serving."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import parse_qs, urlsplit
from . import discover, registry

MAX_QUERY=512
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url=urlsplit(self.path)
        if len(self.path)>MAX_QUERY:
            return self.reply(414,{"error":"query too long"})
        try:
            args=parse_qs(url.query,keep_blank_values=True)
            if url.path=="/health" and not args:
                data={"ok":True,"service":"headronist","mode":"read-only"}
            elif url.path=="/v1/routes":
                if set(args)-{"q","group","limit"}: return self.reply(400,{"error":"unknown query parameter"})
                q=args.get("q",[""])[0]
                group=args.get("group",[None])[0]
                limit=int(args.get("limit",["12"])[0])
                data=discover.discover(q,group,limit)
            elif url.path=="/v1/route":
                if set(args)!={"id"} or len(args["id"])!=1:
                    return self.reply(400,{"error":"id required"})
                data=registry.inspect(args["id"][0],registry.load())
            else:
                return self.reply(404,{"error":"not found"})
            return self.reply(200,data)
        except (ValueError,TypeError) as exc:
            return self.reply(400,{"error":str(exc)})
    def do_POST(self):
        self.reply(405,{"error":"read only"})
    def reply(self,status,data):
        raw=json.dumps(data,sort_keys=True,separators=(",",":")).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(raw)))
        self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.end_headers()
        self.wfile.write(raw)
    def log_message(self,format,*args):
        pass

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--port",type=int,default=8765)
    args=parser.parse_args()
    if not 1024<=args.port<=65535: parser.error("port must be 1024-65535")
    server=ThreadingHTTPServer(("127.0.0.1",args.port),Handler)
    print("Headronist read-only API on http://127.0.0.1:%d"%args.port,flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__=="__main__":
    main()
