"""Minimal stateless MCP JSON-RPC dispatch. No SDK, network, or writes."""
import json
from . import discover, registry, intake

TOOLS=[
 {"name":"design_discover","description":"Search compact Headronist design routes.","inputSchema":{"type":"object","properties":{"query":{"type":"string"},"group":{"type":"string"},"limit":{"type":"integer"}},"additionalProperties":False}},
 {"name":"design_inspect","description":"Inspect one design route and required source paths.","inputSchema":{"type":"object","properties":{"route":{"type":"string"}},"required":["route"],"additionalProperties":False}},
 {"name":"design_intake","description":"Route a structured design task without executing it.","inputSchema":{"type":"object","properties":{"version":{"type":"string"},"task":{"type":"string"},"target":{"type":"string"},"intent":{"type":"string"},"content":{"type":"array","items":{"type":"string"}},"constraints":{"type":"object"},"evidence":{"type":"array","items":{"type":"string"}}},"required":["version","task","target"],"additionalProperties":False}}
]
def dispatch(message):
    if not isinstance(message,dict) or message.get("jsonrpc")!="2.0":
        return {"jsonrpc":"2.0","id":message.get("id") if isinstance(message,dict) else None,"error":{"code":-32600,"message":"Invalid Request"}}
    method=message.get("method")
    ident=message.get("id")
    if method=="notifications/initialized": return None
    if "id" not in message: return None
    try:
        if method=="initialize":
            result={"protocolVersion":"2025-03-26","capabilities":{"tools":{"listChanged":False}},"serverInfo":{"name":"headronist-design","version":"0.1.0"}}
        elif method=="ping": result={}
        elif method=="tools/list": result={"tools":TOOLS}
        elif method=="tools/call":
            params=message.get("params",{})
            if not isinstance(params,dict): raise ValueError("Invalid params")
            name=params.get("name")
            args=params.get("arguments",{})
            if not isinstance(args,dict): raise ValueError("Invalid arguments")
            if name=="design_discover":
                if set(args)-{"query","group","limit"}: raise ValueError("Unknown arguments")
                data=discover.discover(args.get("query",""),args.get("group"),args.get("limit",12))
            elif name=="design_inspect":
                if set(args)!={"route"} or not isinstance(args["route"],str): raise ValueError("route required")
                data=registry.inspect(args["route"],registry.load())
            elif name=="design_intake": data=intake.route(args)
            else: raise ValueError("Unknown tool")
            result={"content":[{"type":"text","text":json.dumps(data,sort_keys=True,separators=(",",":"))}],"isError":False}
        else:
            return {"jsonrpc":"2.0","id":ident,"error":{"code":-32601,"message":"Method not found"}}
        return {"jsonrpc":"2.0","id":ident,"result":result}
    except (ValueError,KeyError,TypeError) as exc:
        if method=="tools/call":
            return {"jsonrpc":"2.0","id":ident,"result":{"content":[{"type":"text","text":str(exc)}],"isError":True}}
        return {"jsonrpc":"2.0","id":ident,"error":{"code":-32602,"message":str(exc)}}
