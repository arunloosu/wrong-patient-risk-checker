# Error Boundary Design

1. **Input boundary:** API validates that order and scan are objects.
2. **Required-field boundary:** missing critical identifiers fail closed.
3. **Configuration boundary:** invalid/missing configuration raises a controlled data error.
4. **Core logic boundary:** `safe_check()` converts validation/runtime input errors into HIGH-risk human verification.
5. **API boundary:** 404/500 responses expose no stack traces and never imply approval.
6. **UI boundary:** users see risk/evidence and human-verification guidance, not treatment recommendations.

This design prevents an application error from being interpreted as a safe patient match.
