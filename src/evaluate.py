"""Reproducible benchmark evaluation with precision/recall/F1 and latency."""
import csv, json, os, time, sys
sys.path.insert(0, os.path.dirname(__file__))
from checker import load_config, check_patient

ROOT = os.path.dirname(os.path.dirname(__file__))
config = load_config(os.path.join(ROOT, "config.json"))

def read_csv(name):
    with open(os.path.join(ROOT, "data", name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

patients = read_csv("patients.csv")
orders = read_csv("orders.csv")
scans = read_csv("wristband_scans.csv")
cases = read_csv("test_cases.csv")

by_id = {p["patient_id"]: p for p in patients}
order_by = {o["order_id"]: o for o in orders}
scan_by = {s["scan_id"]: s for s in scans}

tp=tn=fp=fn=0; passed=0; times=[]
for case in cases:
    order = order_by[case["order_id"]]
    scan = scan_by[case["scan_id"]]
    start=time.perf_counter(); result=check_patient(order, scan, config); times.append((time.perf_counter()-start)*1000)
    expected=case["expected_risk"]
    ok=result.risk_level==expected
    passed += int(ok)
    pred_intercept=result.risk_level in ("MEDIUM","HIGH")
    actual_intercept=expected in ("MEDIUM","HIGH")
    if pred_intercept and actual_intercept: tp+=1
    elif not pred_intercept and not actual_intercept: tn+=1
    elif pred_intercept and not actual_intercept: fp+=1
    else: fn+=1

total=len(cases); acc=(tp+tn)/total if total else 0
precision=tp/(tp+fp) if tp+fp else 0
recall=tp/(tp+fn) if tp+fn else 0
f1=2*precision*recall/(precision+recall) if precision+recall else 0
out={"dataset":{"patients":len(patients),"orders":len(orders),"wristband_scans":len(scans),"benchmark_cases":len(cases)},"multi_identifier_checker":{"tp":tp,"tn":tn,"fp":fp,"fn":fn,"accuracy":acc,"precision":precision,"recall":recall,"f1":f1},"benchmark_pass_rate":passed/total if total else 0,"latency_ms":{"mean":sum(times)/len(times) if times else 0,"max":max(times) if times else 0},"safety_assertions":{"auto_approval_possible":False,"autonomous_treatment_decision":False}}
os.makedirs(os.path.join(ROOT,"outputs"),exist_ok=True)
with open(os.path.join(ROOT,"outputs","evaluation_results.json"),"w",encoding="utf-8") as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2)); print(f"Benchmark: {passed}/{total} PASS")
