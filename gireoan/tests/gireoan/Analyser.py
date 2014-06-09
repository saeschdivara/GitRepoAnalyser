import unittest
from gireoan import Analyser


class TestAnalyser(unittest.TestCase):

    def setUp(self):
        repository_path = ''

        searching_paths = ( '/example/', )

        allowed_endings = ( 'py', )

        exclude_patters = ( '.gitignore', )

        exclude_paths = ( '/env/', )

        self.analyer_obj = Analyser.Analyser(
            repo_name=repository_path,
            searching_paths=searching_paths,
            allowed_endings=allowed_endings,
            exclude_patters=exclude_patters,
            exclude_paths=exclude_paths
        )


    def tearDown(self):
        pass


    def test_is_allowed_path(self):

        test_path = '/example/test.py'

        is_allowed_path = self.analyer_obj._is_allowed_path(path=test_path)

        self.assertTrue(is_allowed_path)


    def test_double_ending_not_allowed(self):
        """
        """

        test_path = '/example/test.py.tpl'

        is_allowed_path = self.analyer_obj._is_allowed_path(path=test_path)

        self.assertFalse(is_allowed_path)