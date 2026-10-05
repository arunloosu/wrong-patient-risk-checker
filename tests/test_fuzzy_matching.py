import os,sys,unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))
from checker import name_similarity, levenshtein_ratio, soundex
class FuzzyMatchingTests(unittest.TestCase):
    def test_ten_synthetic_name_pairs(self):
        pairs=[('John A. Miller','Jon A. Miller'),('Maria Garcia','Maria E Garcia'),('Robert Chen','Robet Chen'),('Anita Joseph','Anita Josph'),('Arun Kumar','Arun Kumer'),('David Wilson','David Wilsn'),('Meena Ravi','Mena Ravi'),('Suresh Raj','Suresh Rj'),('Latha Devi','Latha Dvi'),('Michael Brown','Micheal Brown')]
        self.assertEqual(sum(name_similarity(a,b)>=0.70 for a,b in pairs),10)
    def test_levenshtein(self): self.assertGreater(levenshtein_ratio('john','jon'),0.7)
    def test_soundex(self): self.assertEqual(soundex('Robert'),soundex('Rupert'))
if __name__=='__main__': unittest.main(verbosity=2)
