# Risk Register

| ID | Risk | Impact | Mitigation |
|---|---|---|---|
| R1 | Patient ID mismatch | Very High | Deterministic hard stop + human verification |
| R2 | Wristband swap | Very High | Deterministic hard stop + evidence |
| R3 | Similar/typo names | High | Multiple identifiers + fuzzy similarity |
| R4 | Location mismatch after transfer | Medium | Context check + human verification |
| R5 | Missing scan data | High | Fail-closed behavior |
| R6 | False positive / alert fatigue | High | Benchmark + threshold evaluation |
| R7 | Autonomous-decision interpretation | Very High | Explicit safety boundary; no approval output |
| R8 | Synthetic benchmark limitation | Medium | Document limitation; expand validation |
| R9 | Configuration drift | Medium | External config + reproducibility docs |
| R10 | Audit evidence incomplete | High | Structured evidence output |
