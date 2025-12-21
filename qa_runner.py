
import unittest
import sys
import os

# Add current directory to path just in case
sys.path.append(os.getcwd())

from tests.qa_uat_intelligence import TestIntelligenceLayer

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntelligenceLayer)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
