"""Assemble worker/dist from the headronist package and its contracts.

dist/ is derived and gitignored; run this before `wrangler deploy`.
"""
import pathlib
import shutil

WORKER = pathlib.Path(__file__).resolve().parent
ROOT = WORKER.parent
DIST = WORKER / "dist"


def build(dist=DIST):
    shutil.rmtree(dist, ignore_errors=True)
    (dist / "headronist").mkdir(parents=True)
    (dist / "contracts").mkdir()
    shutil.copy2(WORKER / "entry.py", dist / "entry.py")
    for source in sorted((ROOT / "headronist").glob("*.py")):
        shutil.copy2(source, dist / "headronist" / source.name)
    for source in sorted((ROOT / "contracts").glob("*.json")):
        shutil.copy2(source, dist / "contracts" / source.name)
    return dist


if __name__ == "__main__":
    print(build())
