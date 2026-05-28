"""
Day 5: Promptfoo — Быстрый старт Guide (companion script)
========================================================
This script shows how to run promptfoo programmatically from Python
and how to integrate it into your workflow.

SETUP:
  npm install -g promptfoo
  OR
  npx promptfoo@latest eval -c week1-llm-basics/day5_promptfoo.yaml

VIEW RESULTS:
  npx promptfoo view

ЗАДАЧИ:
1. Run the YAML config and review the web UI
2. Modify a prompt (v1 vs v2) and see which test cases break
3. Add a new provider (e.g., openai:gpt-4o) to compare models
4. Export results: npx promptfoo eval --output results.json
"""

import subprocess
import json
import os


def run_promptfoo_eval(config_path: str = "week1-llm-basics/day5_promptfoo.yaml"):
    """Run promptfoo evaluation and return results."""
    output_path = "week1-llm-basics/outputs/day5_promptfoo_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cmd = [
        "npx", "promptfoo", "eval",
        "-c", config_path,
        "--output", output_path,
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None

    print(result.stdout)
    if os.path.exists(output_path):
        with open(output_path) as f:
            return json.load(f)
    return None


def analyze_results(results: dict):
    """Analyze promptfoo results and highlight failures."""
    if not results:
        print("No results to analyze.")
        return

    print("\n=== PROMPTFOO RESULTS ANALYSIS ===")
    total = 0
    passed = 0
    failed_cases = []

    for result in results.get("results", {}).get("results", []):
        total += 1
        if result.get("success"):
            passed += 1
        else:
            failed_cases.append({
                "prompt": result.get("vars", {}).get("question", "?")[:50],
                "failures": [a.get("reason", "unknown") for a in result.get("assertionResults", []) if not a.get("pass")],
            })

    print(f"Total: {total} | Passed: {passed} | Failed: {total - passed}")
    if failed_cases:
        print("\nFailed cases:")
        for fc in failed_cases:
            print(f"  - {fc['prompt']}")
            for reason in fc["failures"]:
                print(f"    ! {reason[:80]}")


if __name__ == "__main__":
    print("=== Day 5: Promptfoo Evaluation ===")
    print("\nTo run the evaluation:")
    print("  npx promptfoo eval -c week1-llm-basics/day5_promptfoo.yaml")
    print("\nTo view results in browser:")
    print("  npx promptfoo view")
    print("\nTo run programmatically (requires npx in PATH):")

    results = run_promptfoo_eval()
    if results:
        analyze_results(results)
