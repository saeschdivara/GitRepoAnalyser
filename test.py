# Unit Tests
import unittest

# Test suites
from gireoan.tests.gireoan.Analyser import TestAnalyserWithSubPath, TestAnalyserWithRootPath



# Variables
test_suites = []
errors = 0
failures = 0

# Test suites
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TestAnalyserWithSubPath) )
test_suites.append( unittest.TestLoader().loadTestsFromTestCase(TestAnalyserWithRootPath) )

for test_suite in test_suites:

    # Tests runner
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)

    errors += len(result.errors)
    failures += len(result.failures)

import sys; sys.exit( errors + failures )