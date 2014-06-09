import unittest
from gireoan.tests.gireoan.Analyser import TestAnalyser

analyser_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAnalyser)
result = unittest.TextTestRunner(verbosity=2).run(analyser_test_suite)

errors = len(result.errors)
failures = len(result.failures)

import sys; sys.exit( errors + failures )