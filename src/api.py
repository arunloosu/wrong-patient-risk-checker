"""Small Flask API exposing the same safety-bounded checker used by the UI."""
from flask import Flask, jsonify, request
from checker import load_config, safe_check

app = Flask(__name__)
CONFIG = load_config()

@app.get("/api/health")
def health():
    """Health endpoint: reports service availability, not clinical readiness."""
    return jsonify({"status": "ok", "service": "wrong-patient-risk-checker"})

@app.post("/api/check")
def check():
    """Run an identity consistency check; never return an approval decision."""
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload.get("order"), dict) or not isinstance(payload.get("scan"), dict):
        return jsonify({"error": "order and scan objects are required", "fail_closed": True}), 400
    result = safe_check(payload["order"], payload["scan"], CONFIG)
    return jsonify(result.to_dict()), (200 if result.check_status == "OK" else 422)

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "endpoint_not_found", "fail_closed": True}), 404

@app.errorhandler(500)
def server_error(_):
    # Do not expose stack traces or silently imply a safe match after server errors.
    return jsonify({"error": "internal_error", "fail_closed": True, "human_verification_required": True}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
