"""Cloudflare Python Worker serving the Headronist MCP dispatcher.

Reached only through a service binding from headron.tech/mcp; no public route.
The dispatcher is the same headronist.mcp module the stdio server uses, copied
into dist/ by build.py so there is one implementation.
"""
import json

from workers import Response, WorkerEntrypoint

JSON = {"content-type": "application/json"}


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Imported lazily: a module-level import of the package failed to
        # register the fetch handler in the spike.
        from headronist import mcp

        if request.method == "GET":
            return Response(json.dumps({"ok": True, "tools": len(mcp.TOOLS)}), headers=JSON)
        if request.method != "POST":
            return Response("", status=405, headers={"allow": "GET, POST"})
        try:
            message = json.loads(await request.text())
        except ValueError:
            error = {"code": -32700, "message": "Parse error"}
            return Response(json.dumps({"jsonrpc": "2.0", "id": None, "error": error}), status=400, headers=JSON)
        try:
            reply = mcp.dispatch(message)
        except Exception:
            error = {"code": -32603, "message": "Internal error"}
            reply = {"jsonrpc": "2.0", "id": message.get("id") if isinstance(message, dict) else None, "error": error}
        if reply is None:
            return Response("", status=202)
        return Response(json.dumps(reply), headers=JSON)
