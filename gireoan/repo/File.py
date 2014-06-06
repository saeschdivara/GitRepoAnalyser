

class File(object):

    @classmethod
    def get_ending(cls, file_path):
        """
        """

        return file_path.split('.')[-1]


    def __init__(self, path):
        """
        """
        
        self.path = path

        self.ending = ''

        self.commits = 0
        self.code_lines = 0