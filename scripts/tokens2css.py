#!/usr/bin/env python3
"""tokens.json du design system abdoul.dev -> tokens.css (variables CSS sur :root). Usage : python3 tokens2css.py tokens.json tokens.css"""
import json, sys
t = json.load(open(sys.argv[1])); out = [":root{"]
def val(v): return v.get("video", next(iter(v.values()))) if isinstance(v, dict) else v
for fam in ("color", "spacing", "radius", "shadow", "border", "size"):
    for tok in t.get(fam, {}).get("tokens", []):
        out.append(f"  --{tok['name']}:{val(tok['value'])};")
for k, v in t.get("type", {}).get("families", {}).items():
    out.append(f"  --font-{k}:{v};")
out.append("}")
open(sys.argv[2], "w").write("\n".join(out) + "\n")
print(f"{len(out)-2} variables")
