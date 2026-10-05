"""Core wrong-patient risk checking logic.

Safety boundary: this module checks identity/workflow consistency only.
It never approves, rejects, prescribes, doses, administers, or changes treatment.
"""
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from typing import Any, Dict, List
import json
import os


class CheckerValidationError(ValueError):
    """Raised when required verification input is missing or malformed."""


class CheckerDataError(RuntimeError):
    """Raised when reference data cannot safely support a check."""


def normalize(value: Any) -> str:
    """Normalize an identifier/name for safe comparison without changing source data."""
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())



def levenshtein_ratio(a: Any, b: Any) -> float:
    """Return normalized Levenshtein similarity in the range 0..1."""
    a, b = normalize(a), normalize(b)
    if not a and not b: return 1.0
    if not a or not b: return 0.0
    prev=list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        cur=[i]
        for j, cb in enumerate(b, 1):
            cur.append(min(cur[-1]+1, prev[j]+1, prev[j-1]+(ca!=cb)))
        prev=cur
    return 1.0 - prev[-1]/max(len(a),len(b))

def soundex(value: Any) -> str:
    """Return a compact English phonetic code for name comparison."""
    s=''.join(ch for ch in normalize(value).upper() if ch.isalpha())
    if not s: return ''
    codes=dict.fromkeys('BFPV','1') | dict.fromkeys('CGJKQSXZ','2') | dict.fromkeys('DT','3') | {'L':'4','MN':'5','R':'6'}
    first=s[0]; out=first; last=''
    mapping={'B':'1','F':'1','P':'1','V':'1','C':'2','G':'2','J':'2','K':'2','Q':'2','S':'2','X':'2','Z':'2','D':'3','T':'3','L':'4','M':'5','N':'5','R':'6'}
    for ch in s[1:]:
        code=mapping.get(ch,'')
        if code and code!=last: out+=code
        last=code
    return (out+'000')[:4]

def name_similarity(a: Any, b: Any) -> float:
    """Return a deterministic 0..1 similarity score for names."""
    a, b = normalize(a), normalize(b)
    if not a or not b:
        return 0.0
    jw = SequenceMatcher(None, a, b).ratio()
    lev = levenshtein_ratio(a, b)
    phonetic = 1.0 if soundex(a) == soundex(b) else 0.0
    return max(jw, (jw + lev + phonetic) / 3.0)


@dataclass
class CheckResult:
    risk_level: str
    score: int
    human_verification_required: bool
    discrepancies: List[str]
    evidence: List[str]
    check_status: str = "OK"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_config(path: str = "config.json") -> Dict[str, Any]:
    """Load configurable weights and thresholds; fail closed if config is invalid."""
    if not os.path.exists(path):
        raise CheckerDataError(f"Configuration file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        required = {"weights", "thresholds"}
        if not required.issubset(cfg):
            raise CheckerDataError("Configuration missing weights or thresholds")
        return cfg
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckerDataError(f"Unable to load configuration safely: {exc}") from exc


def check_patient(order: Dict[str, Any], scan: Dict[str, Any], config: Dict[str, Any]) -> CheckResult:
    """Compare intended and scanned patient identifiers.

    Critical ID/wristband mismatches are hard stops. Missing critical identifiers
    also require human verification. All other scoring is configurable.
    """
    required = ["patient_id", "wristband_id", "dob", "name", "location"]
    missing = [k for k in required if not normalize(order.get(k)) or not normalize(scan.get(k))]
    if missing:
        return CheckResult(
            risk_level="HIGH", score=0, human_verification_required=True,
            discrepancies=[f"MISSING_IDENTIFIER:{k.upper()}" for k in missing],
            evidence=["Critical verification data is missing; fail closed and require human verification."]
        )

    discrepancies: List[str] = []
    evidence: List[str] = []
    weights = config["weights"]
    score = 0

    pairs = [
        ("patient_id", "PATIENT_ID_MISMATCH"),
        ("wristband_id", "WRISTBAND_MISMATCH"),
        ("dob", "DOB_MISMATCH"),
        ("name", "NAME_MISMATCH"),
        ("location", "LOCATION_MISMATCH"),
    ]

    # Critical identifiers are deterministic safety gates, not fuzzy matches.
    if normalize(order["patient_id"]) != normalize(scan["patient_id"]):
        discrepancies.append("PATIENT_ID_MISMATCH")
    else:
        score += int(weights["patient_id"])

    if normalize(order["wristband_id"]) != normalize(scan["wristband_id"]):
        discrepancies.append("WRISTBAND_MISMATCH")
    else:
        score += int(weights["wristband_id"])

    if normalize(order["dob"]) == normalize(scan["dob"]):
        score += int(weights["dob"])
    else:
        discrepancies.append("DOB_MISMATCH")

    sim = name_similarity(order["name"], scan["name"])
    if sim >= float(config["thresholds"].get("name_similarity", 0.88)):
        score += int(weights["name"])
    else:
        discrepancies.append("NAME_MISMATCH")
        evidence.append(f"Name similarity={sim:.3f}, below configured threshold.")

    if normalize(order["location"]) == normalize(scan["location"]):
        score += int(weights["location"])
    else:
        discrepancies.append("LOCATION_MISMATCH")

    # A critical mismatch always overrides weighted scoring.
    if "PATIENT_ID_MISMATCH" in discrepancies or "WRISTBAND_MISMATCH" in discrepancies:
        risk = "HIGH"
        human = True
        score = 0
    elif not discrepancies:
        risk = "LOW"
        human = False
    else:
        risk = "MEDIUM"
        human = True

    evidence.insert(0, f"Risk={risk}; verification_score={score}/100; human verification required={human}.")
    evidence.append("Final verification remains with an authorized human; no automatic medicine approval is permitted.")
    return CheckResult(risk, score, human, discrepancies, evidence)


def safe_check(order: Dict[str, Any], scan: Dict[str, Any], config: Dict[str, Any]) -> CheckResult:
    """Error boundary for UI/API callers; never convert an exception into a LOW-risk result."""
    try:
        if not isinstance(order, dict) or not isinstance(scan, dict):
            raise TypeError("order and scan must be objects")
        return check_patient(order, scan, config)
    except (KeyError, TypeError, ValueError) as exc:
        return CheckResult("HIGH", 0, True, ["VALIDATION_ERROR"], [f"Verification could not be completed safely: {exc}"], "ERROR")
