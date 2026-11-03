"""Build original structured image briefs, no hosted model dependency."""
def build_prompt(spec):
    required={"kind","intent","aspectRatio","palette","text"}
    if not required.issubset(spec): raise ValueError("Missing image fields")
    if spec["aspectRatio"] not in ("1:1","4:5","9:16","16:9","3:2","21:9"):raise ValueError("Invalid aspect ratio")
    if len(spec["text"])>5:raise ValueError("Too much text")
    safe=spec.get("safeArea",.1)
    if not .03<=safe<=.3:raise ValueError("Unsafe margin")
    return "\n".join([
        f"Original {spec['kind']} design. {spec['intent']}",
        f"Aspect ratio {spec['aspectRatio']}; palette {spec['palette']}; safe margins {safe:.0%} on all edges.",
        "Clean geometry, intentional negative space, crisp edges, readable contrast, no unintended cropping.",
        "Text (exact spelling): "+(" | ".join(spec["text"]) if spec["text"] else "none"),
        "No fake interface elements, illegible microtext, watermark, logos of other brands or unlicensed imagery.",
        "Avoid: "+", ".join(spec.get("negative",[]))
    ])
