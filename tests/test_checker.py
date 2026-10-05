import os, sys, json, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from checker import check_patient, safe_check, name_similarity

CFG=json.load(open(os.path.join(os.path.dirname(__file__),'..','config.json'),encoding='utf-8'))
BASE={'patient_id':'PAT-1001','wristband_id':'WB-1001','dob':'1965-03-12','name':'John A. Miller','location':'Ward-3A Bed-01'}

class SafetyTests(unittest.TestCase):
    def test_exact_match_is_low(self):
        r=check_patient(BASE.copy(),BASE.copy(),CFG); self.assertEqual(r.risk_level,'LOW'); self.assertFalse(r.human_verification_required)
    def test_patient_id_hard_stop(self):
        s=BASE.copy(); s['patient_id']='PAT-1002'; r=check_patient(BASE,s,CFG); self.assertEqual(r.risk_level,'HIGH'); self.assertIn('PATIENT_ID_MISMATCH',r.discrepancies)
    def test_wristband_hard_stop(self):
        s=BASE.copy(); s['wristband_id']='WB-1002'; r=check_patient(BASE,s,CFG); self.assertEqual(r.risk_level,'HIGH')
    def test_location_mismatch_is_medium(self):
        s=BASE.copy(); s['location']='Ward-9Z Bed-99'; r=check_patient(BASE,s,CFG); self.assertEqual(r.risk_level,'MEDIUM'); self.assertTrue(r.human_verification_required)
    def test_missing_critical_identifier_fails_closed(self):
        s=BASE.copy(); s['wristband_id']=''; r=check_patient(BASE,s,CFG); self.assertEqual(r.risk_level,'HIGH'); self.assertTrue(r.human_verification_required)
    def test_name_typo_similarity(self):
        self.assertGreaterEqual(name_similarity('John A. Miller','Jon A. Miller'),0.88)
    def test_bad_input_error_boundary(self):
        r=safe_check(None,BASE,CFG); self.assertEqual(r.risk_level,'HIGH'); self.assertEqual(r.check_status,'ERROR')
    def test_no_autonomous_approval(self):
        self.assertFalse(CFG['safety_rules']['automatic_medicine_approval'])

if __name__=='__main__': unittest.main(verbosity=2)
