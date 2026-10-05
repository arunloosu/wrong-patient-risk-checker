# Unit Testing and Error Boundaries

## Automated unit tests
The test suite verifies:
1. Exact identifier match produces LOW risk.
2. Patient ID mismatch is a deterministic HIGH-risk hard stop.
3. Wristband mismatch is a deterministic HIGH-risk hard stop.
4. Location mismatch produces MEDIUM risk and human verification.
5. Missing critical data fails closed to HIGH risk.
6. Similar names pass the configured similarity threshold.
7. Invalid input is caught by the error boundary and never becomes LOW risk.
8. Automatic medicine approval remains disabled by configuration.

Run:
`python -m unittest discover -s tests -v`

## Error boundaries
- Configuration loading errors fail closed.
- Missing critical identifiers require human verification.
- API validation errors return safe error responses.
- Unhandled API errors return `fail_closed=true`.
- Core checker exceptions are converted to a HIGH-risk verification result.

The safety principle is: **an uncertain or failed check must never be interpreted as a successful identity match.**
