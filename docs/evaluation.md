# Evaluation protocol

Use the same 120 hand-labelled questions for both systems. Freeze the train/test or prompt configuration before comparing runs. For each question, record expected source IDs, retrieved source IDs, answer groundedness (pass/fail), escalation correctness and latency.

Report grounded answer accuracy as grounded passes divided by total questions. Report median latency from monotonic wall-clock measurements after separating cold-start and warm runs. Keep model deployment, prompt version, chunk size, top-k and threshold in the run metadata. The 61% baseline and 83% result in the project brief should only be claimed when reproduced from the original labelled set.
