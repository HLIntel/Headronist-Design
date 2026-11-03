"""Native deterministic token compiler, no third-party runtime."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def compile_tokens(spec):
    if set(spec)!={'schemaVersion','id','colors','spacing','radii','type'} or spec['schemaVersion']!='1.0.0':raise ValueError('Invalid contract')
    colors=spec['colors']
    if not {'ground','light','band','mark','soft','deep'}<=set(colors):raise ValueError('Missing colors')
    if not all(isinstance(v,str) and re.fullmatch(r'#[0-9a-fA-F]{6}',v) for v in colors.values()):raise ValueError('Invalid color')
    for key in ('spacing','radii'):
        if not isinstance(spec[key],dict) or not all(type(v) in (int,float) and 0<=v<=256 for v in spec[key].values()):raise ValueError('Invalid '+key)
    css='@layer headronist.tokens {\n:root {\n'+''.join(f'  --hd-color-{k}: {v};\n' for k,v in sorted(colors.items()))+'}\n}\n'
    swift='// Generated Headronist tokens\nimport Foundation\nenum HeadronistTokens {\n'+''.join(f'  static let {k} = "{v}"\n' for k,v in sorted(colors.items()))+'}\n'
    kotlin='// Generated Headronist tokens\nobject HeadronistTokens {\n'+''.join(f'  const val {k} = "{v}"\n' for k,v in sorted(colors.items()))+'}\n'
    return {'tokens.css':css,'Tokens.swift':swift,'Tokens.kt':kotlin,'agent.tokens.json':json.dumps(spec,sort_keys=True,separators=(',',':'))+'\n'}
def write(spec,out):
    target=Path(out);target.mkdir(parents=True,exist_ok=True)
    for name,content in compile_tokens(spec).items():(target/name).write_text(content)
