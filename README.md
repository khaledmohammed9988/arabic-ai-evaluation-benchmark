# Arabic Instruction-Following Evaluation Benchmark

A compact, auditable benchmark for evaluating Arabic AI responses. Each case has an explicit reference answer, required concepts, forbidden claims, and deterministic scoring rules. The repository includes the dataset, reference grader, regression tests, and a human-review rubric.

## Design goals

- **Traceable:** every score maps to a case and criterion.
- **Reproducible:** the grader uses only the Python standard library.
- **Arabic-aware:** normalization handles diacritics, tatweel, and common orthographic variants.
- **Hard to game:** exact match is reported separately from concept coverage and forbidden-claim checks.
- **Reviewable:** automated scores never replace the documented human rubric.

## Run

```bash
python reference_solution/evaluator.py benchmark/sample_predictions.jsonl
python -m unittest discover -s tests -v
```

The public dataset is intentionally small and demonstrates a transparent reference implementation. A production benchmark should expand domains, use independent expert review, and keep a held-out set private.

## Repository layout

- benchmark/cases.jsonl — public evaluation cases
- benchmark/sample_predictions.jsonl — example model outputs
- reference_solution/evaluator.py — deterministic scorer
- tests/test_evaluator.py — edge-case and regression tests
- RUBRIC.md — human-review procedure and score interpretation

## License

MIT
