"""MCP stdio adapter for agent runtimes. Stdout is protocol-only."""
import json
import sys
from .mcp import dispatch
MAX_LINE=65536
def main():
    for line in sys.stdin.buffer:
        if len(line)>MAX_LINE:
            continue
        try:
            result=dispatch(json.loads(line))
            if result is not None:
                sys.stdout.write(json.dumps(result,separators=(",",":"))+"\n")
                sys.stdout.flush()
        except (ValueError,UnicodeError):
            continue
if __name__=="__main__":main()
