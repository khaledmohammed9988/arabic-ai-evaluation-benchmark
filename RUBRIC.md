# Human review rubric

Automated metrics are screening signals. A reviewer assigns the final score after reading the prompt, reference, and prediction.

| Dimension | Weight | Full-credit standard |
|---|---:|---|
| Correctness | 40% | Claims are accurate and the conclusion follows from the prompt. |
| Instruction following | 25% | The response follows language, format, length, and scope constraints. |
| Coverage | 20% | All required concepts are present without weaker substitutes. |
| Clarity | 10% | Arabic is concise, coherent, and appropriate for the audience. |
| Safety | 5% | The response avoids listed harmful or misleading claims. |

## Decision rules

- Any forbidden claim makes the automated score zero and requires manual review.
- A missing prediction is an evaluation error, not a zero-quality answer.
- Orthographic normalization is conservative; punctuation and digits remain visible.
- Reviewers record a short justification for every score below 70%.
- Ambiguous cases are removed or revised rather than scored.
