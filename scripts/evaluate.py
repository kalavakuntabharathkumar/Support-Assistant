import argparse, json
from app.graph import support_graph

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/eval_questions.jsonl")
    args = parser.parse_args()
    rows = [json.loads(line) for line in open(args.input, encoding="utf-8") if line.strip()]
    passed = 0
    for row in rows:
        result = support_graph.invoke({"question": row["question"]})
        ids = {x["article_id"] for x in result.get("sources", [])}
        ok = row["expected_source"] in ids
        passed += int(ok)
        print(f"{'PASS' if ok else 'FAIL'} | {row['question']} | retrieved={sorted(ids)}")
    print(f"Source-hit rate: {passed}/{len(rows)} = {passed / max(1, len(rows)):.1%}")

if __name__ == "__main__":
    main()
