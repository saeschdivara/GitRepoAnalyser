import unittest
from gireoan.tests.gireoan.Analyser import TestAnalyser

analyser_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAnalyser)
unittest.TextTestRunner(verbosity=2).run(analyser_test_suite)