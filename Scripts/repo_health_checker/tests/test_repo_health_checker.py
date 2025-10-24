import unittest
import tempfile
from pathlib import Path
import shutil
import sys

# Import the module (adjust import path if necessary)
sys.path.append(str(Path(__file__).resolve().parents[2]))
from repo_health_checker import check_repo  # type: ignore

class BasicTest(unittest.TestCase):
    def test_check_empty_dir(self):
        d = Path(tempfile.mkdtemp())
        try:
            findings = check_repo(d)
            # basic expectations
            self.assertIn("README", findings)
            self.assertFalse(findings["README"]["found"])
            self.assertFalse(findings["PYTHON_FILES"]["found"])
        finally:
            shutil.rmtree(d)

if __name__ == "__main__":
    unittest.main()
