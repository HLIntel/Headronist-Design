"""Portable WSGI HTTP adapter for managed cloud deployments; no hosting included."""
import hmac
import json
import os
from .mcp import dispatch

MAX_BODY=65536
def application(environ,start_response):
    def respond(status,payload,headers=None):
        data=json.dumps(payload,separators=(",",":")).encode()
        start_response(status,[("Content-Type","application/json"),("Content-Length",str(len(data))),("Cache-Control","no-store"),("X-Content-Type-Options","nosniff")]+(headers or []))
        return [data]
    path=environ.get("PATH_INFO","")
    method=environ.get("REQUEST_METHOD","")
    if path=="/health" and method=="GET":
        return respond("200 OK",{"ok":True,"service":"headronist","transport":"wsgi"})
    if path!="/mcp" or method!="POST":
        return respond("404 Not Found",{"error":"not found"})
    secret=os.environ.get("HEADRONIST_API_TOKEN","")
    if len(secret)<24:
        return respond("503 Service Unavailable",{"error":"server not configured"})
    auth=environ.get("HTTP_AUTHORIZATION","")
    if not hmac.compare_digest(auth,"Bearer "+secret):
        return respond("401 Unauthorized",{"error":"unauthorized"},[("WWW-Authenticate","Bearer")])
    try:
        length=int(environ.get("CONTENT_LENGTH","0"))
        if not 0<length<=MAX_BODY:
            return respond("413 Payload Too Large",{"error":"invalid body size"})
        payload=json.loads(environ["wsgi.input"].read(length))
        result=dispatch(payload)
        if result is None:
            start_response("202 Accepted",[("Content-Length","0")])
            return [b""]
        return respond("200 OK",result)
    except (ValueError,UnicodeError,KeyError,TypeError):
        return respond("400 Bad Request",{"error":"invalid JSON-RPC request"})
