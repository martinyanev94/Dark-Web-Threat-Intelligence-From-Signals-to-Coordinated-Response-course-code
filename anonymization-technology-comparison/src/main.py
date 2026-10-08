import json
from pathlib import Path
from comparison import TechnologyClaim, generate_brief

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "data" / "flawed_brief.json").read_text())
claims = [TechnologyClaim(**item) for item in source]
result = generate_brief(claims)
print(json.dumps(result, indent=2))
if result["issues"]:
    raise SystemExit("brief review failed")
