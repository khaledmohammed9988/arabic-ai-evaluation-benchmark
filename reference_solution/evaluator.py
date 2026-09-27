from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata

DIACRITICS = re.compile(r"[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed]")
SPACE = re.compile(r"\s+")

def normalize(text: str) -> str:
    if not isinstance(text, str): raise TypeError("text must be a string")
    text = unicodedata.normalize("NFC", text)
    text = DIACRITICS.sub("", text).replace("ـ", "")
    text = text.translate(str.maketrans({"أ":"ا","إ":"ا","آ":"ا","ٱ":"ا","ى":"ي"}))
    return SPACE.sub(" ", text).strip()

def token_f1(reference: str, prediction: str) -> float:
    ref, pred = Counter(normalize(reference).split()), Counter(normalize(prediction).split())
    overlap = sum((ref & pred).values())
    precision = overlap / sum(pred.values()) if pred else float(not ref)
    recall = overlap / sum(ref.values()) if ref else float(not pred)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0

def score_case(case: dict, prediction: str) -> dict:
    normalized_prediction = normalize(prediction)
    required = [normalize(item) for item in case["required_concepts"]]
    forbidden = [normalize(item) for item in case["forbidden_claims"]]
    coverage = sum(item in normalized_prediction for item in required) / len(required) if required else 1.0
    violations = [item for item in forbidden if item in normalized_prediction]
    exact = float(normalized_prediction == normalize(case["reference"]))
    f1 = token_f1(case["reference"], prediction)
    score = 0.35 * exact + 0.35 * f1 + 0.30 * coverage
    if violations: score = 0.0
    return {"id":case["id"],"exact_match":exact,"token_f1":round(f1,6),"concept_coverage":round(coverage,6),"forbidden_violations":violations,"score":round(score,6)}

def read_jsonl(path: str | Path) -> list[dict]:
    records=[]
    for line_number,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if line.strip():
            try: records.append(json.loads(line))
            except json.JSONDecodeError as error: raise ValueError(f"invalid JSON on line {line_number}: {error.msg}") from error
    return records

def evaluate(cases: list[dict], predictions: list[dict]) -> dict:
    by_id={row["id"]:row["prediction"] for row in predictions}
    missing=[case["id"] for case in cases if case["id"] not in by_id]
    if missing: raise ValueError(f"missing predictions: {', '.join(missing)}")
    results=[score_case(case,by_id[case["id"]]) for case in cases]
    return {"case_count":len(results),"mean_score":round(sum(row["score"] for row in results)/len(results),6),"cases":results}

def main() -> None:
    if len(sys.argv)!=2: raise SystemExit("usage: python evaluator.py PREDICTIONS.jsonl")
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(evaluate(read_jsonl(root/"benchmark"/"cases.jsonl"),read_jsonl(sys.argv[1])),ensure_ascii=False,indent=2))

if __name__=="__main__": main()
