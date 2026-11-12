"""Minimal stateless MCP JSON-RPC dispatch. No SDK, network, or writes."""
import json
from pathlib import Path
from . import discover, registry, intake, assets, visuals, composition

INTAKE_SCHEMA = json.loads(
    (Path(__file__).resolve().parent.parent / "contracts/intake.v1.schema.json").read_text(encoding="utf-8")
)

TOOLS = [
    {
        "name": "design_discover",
        "description": "Search compact Headronist design routes.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "group": {"type": "string"}, "limit": {"type": "integer"}},
            "additionalProperties": False,
        },
    },
    {
        "name": "design_inspect",
        "description": "Inspect one design route and required source paths.",
        "inputSchema": {
            "type": "object",
            "properties": {"route": {"type": "string"}},
            "required": ["route"],
            "additionalProperties": False,
        },
    },
    {
        "name": "design_intake",
        "description": "Route a structured design task without executing it.",
        "inputSchema": INTAKE_SCHEMA,
    },
    {
        "name": "design_recommend_assets",
        "description": "Recommend local and curated visual assets for a given design intent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "intent": {"type": "string"},
                "kind": {"type": "string"},
                "offline": {"type": "boolean"},
            },
            "required": ["intent"],
            "additionalProperties": False,
        },
    },
    {
        "name": "design_visual_prompt",
        "description": "Build a structured prompt brief for image generation or visual design.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string"},
                "intent": {"type": "string"},
                "audience": {"type": "string"},
                "palette": {"type": "string"},
                "aspect_ratio": {"type": "string"},
                "style": {"type": "string"},
                "text": {"type": "array", "maxItems": 8, "items": {"type": "string", "maxLength": 120}},
                "references": {"type": "array", "maxItems": 5, "items": {"type": "string", "maxLength": 300}},
                "constraints": {"type": "array", "maxItems": 12, "items": {"type": "string", "maxLength": 300}},
            },
            "required": ["kind", "intent"],
            "additionalProperties": False,
        },
    },
    {
        "name": "design_graph_guidance",
        "description": "Recommend chart and data graphic encodings based on data shape and analytical purpose.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_shape": {"type": "string", "enum": list(visuals.DATA_SHAPES)},
                "purpose": {"type": "string"},
                "audience": {"type": "string", "enum": list(visuals.AUDIENCES)},
            },
            "required": ["data_shape"],
            "additionalProperties": False,
        },
    },
    {
        "name": "design_composition_check",
        "description": "Advisory HTML composition analysis against anti-patterns (card walls, badge clutter, run-on headings).",
        "inputSchema": {
            "type": "object",
            "properties": {"html": {"type": "string"}},
            "required": ["html"],
            "additionalProperties": False,
        },
    },
]

TOOL_SCHEMAS = {tool["name"]: tool["inputSchema"] for tool in TOOLS}


def _validate(value, schema, path="arguments"):
    """Validate the JSON Schema keywords used by the published tool inputs."""
    kind = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool, "integer": int}
    if kind and (not isinstance(value, types[kind]) or (kind == "integer" and isinstance(value, bool))):
        raise ValueError(f"{path} must be {kind}")
    if "const" in schema and value != schema["const"]:
        raise ValueError(f"{path} has unsupported value")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path} has unsupported value")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and value.keys() - properties.keys():
            raise ValueError(f"{path} contains unknown fields")
        if set(schema.get("required", [])) - value.keys():
            raise ValueError(f"{path} is missing required fields")
        for key, item in value.items():
            if key in properties:
                _validate(item, properties[key], f"{path}.{key}")
    if isinstance(value, (str, list)):
        low = schema.get("minLength" if isinstance(value, str) else "minItems", 0)
        high = schema.get("maxLength" if isinstance(value, str) else "maxItems")
        if len(value) < low or (high is not None and len(value) > high):
            raise ValueError(f"{path} has invalid length")
    if isinstance(value, list) and "items" in schema:
        for item in value:
            _validate(item, schema["items"], path + "[]")


def dispatch(message):
    if not isinstance(message, dict) or message.get("jsonrpc") != "2.0":
        return {
            "jsonrpc": "2.0",
            "id": message.get("id") if isinstance(message, dict) else None,
            "error": {"code": -32600, "message": "Invalid Request"},
        }
    method = message.get("method")
    ident = message.get("id")
    if method == "notifications/initialized":
        return None
    if "id" not in message:
        return None
    try:
        if method == "initialize":
            result = {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "headronist-design", "version": "0.1.0"},
            }
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = message.get("params", {})
            if not isinstance(params, dict):
                raise ValueError("Invalid params")
            name = params.get("name")
            args = params.get("arguments", {})
            if not isinstance(args, dict):
                raise ValueError("Invalid arguments")
            if not isinstance(name, str) or name not in TOOL_SCHEMAS:
                raise ValueError("Unknown tool")
            _validate(args, TOOL_SCHEMAS[name])
            if name == "design_discover":
                if set(args) - {"query", "group", "limit"}:
                    raise ValueError("Unknown arguments")
                data = discover.discover(args.get("query", ""), args.get("group"), args.get("limit", 12))
            elif name == "design_inspect":
                if set(args) != {"route"} or not isinstance(args["route"], str):
                    raise ValueError("route required")
                data = registry.inspect(args["route"], registry.load())
            elif name == "design_intake":
                data = intake.route(args)
            elif name == "design_recommend_assets":
                if not isinstance(args.get("intent"), str):
                    raise ValueError("intent required")
                data = assets.recommend(
                    args["intent"],
                    kind=args.get("kind", "auto"),
                    offline=args.get("offline", True),
                )
            elif name == "design_visual_prompt":
                if not isinstance(args.get("kind"), str) or not isinstance(args.get("intent"), str):
                    raise ValueError("kind and intent required")
                data = visuals.build_prompt(
                    kind=args["kind"],
                    intent=args["intent"],
                    audience=args.get("audience", "general"),
                    palette=args.get("palette", "brand"),
                    aspect_ratio=args.get("aspect_ratio", "16:9"),
                    style=args.get("style", "premium restrained"),
                    text=args.get("text"),
                    references=args.get("references"),
                    constraints=args.get("constraints"),
                )
            elif name == "design_graph_guidance":
                if not isinstance(args.get("data_shape"), str):
                    raise ValueError("data_shape required")
                data = visuals.recommend_graph(
                    data_shape=args["data_shape"],
                    purpose=args.get("purpose", "comparison"),
                    audience=args.get("audience", "general"),
                )
            elif name == "design_composition_check":
                if not isinstance(args.get("html"), str):
                    raise ValueError("html required")
                data = composition.analyze(args["html"])
            else:
                raise ValueError("Unknown tool")
            result = {"content": [{"type": "text", "text": json.dumps(data, sort_keys=True, separators=(",", ":"))}], "isError": False}
        else:
            return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": "Method not found"}}
        return {"jsonrpc": "2.0", "id": ident, "result": result}
    except (ValueError, KeyError, TypeError) as exc:
        if method == "tools/call":
            return {"jsonrpc": "2.0", "id": ident, "result": {"content": [{"type": "text", "text": str(exc)}], "isError": True}}
        return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32602, "message": str(exc)}}
