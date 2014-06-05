# Regex
import re

# Git
from dulwich.repo import Repo
from dulwich.objects import Blob




def get_file_ending(file_path):
    """
    """

    return file_path.split('.')[-1]


class Analyser(object):

    CHANGE_TYPES = (
        'add',
        'modify',
        'delete',
    )

    def __init__(self,
                 repo_name,
                 searching_paths, allowed_endings,
                 exclude_patters, exclude_paths,
                 ):
        """
        """

        # Repository
        self.repo_name = repo_name
        self.repo = Repo(repo_name)

        # File infos
        self.file_endings = {}
        self.file_paths = {}

        # Commits
        self.authors = {}
        self.commits = 0

        # Searched
        self.SEARCHING_PATHS = searching_paths
        self.ALLOWED_ENDINGS = allowed_endings

        # Excludes
        self.EXCLUDE_PATTERNS = exclude_patters
        self.EXCLUDE_PATHS = exclude_paths



    def do_analyse(self):
        """
        """


        for change_tree in self.repo.get_walker():
            author_name = change_tree.commit.author

            if author_name in self.authors:
                author_count = self.authors[author_name]
                author_count += 1
                self.authors[author_name] = author_count
            else:
                self.authors[author_name] = 1

            for tree_change in change_tree.changes():
                # Save tree data
                self.save_tree_data(
                    tree_change=tree_change,
                )




    def is_matching_exclude_pattern(self, path):
        """
        """

        for pattern in self.EXCLUDE_PATTERNS:

            p = re.compile(pattern)

            if p.match(path) is not None:
                return True

        return False


    def in_exclude_path(self, path):
        """
        """

        for exclude_path in self.EXCLUDE_PATHS:

            if path.startswith(exclude_path):
                return True

        return False


    def is_allowed_path(self, path):
        """
        """

        try:
            file_ending = get_file_ending(path)

            for search_path in self.SEARCHING_PATHS:

                if self.in_exclude_path(path):
                    return False

                if self.is_matching_exclude_pattern(path):
                    return False

                if not path.startswith(search_path):
                    return False

            if file_ending not in self.ALLOWED_ENDINGS or path in self.file_paths:
                return False

            self.file_paths[path] = True

        except Exception as err:
            print(err)

        return True


    def save_tree_data(self, tree_change):

        # Check if is list
        if type(tree_change) is list:

            for change in tree_change:
                self.parse_change_tree(tree_change=change)

        else:
            self.parse_change_tree(tree_change=tree_change)


    def parse_change_tree(self, tree_change):

        change_type = ''

        change_type = tree_change.type
        new_tree_sha = tree_change.new.sha

        if new_tree_sha is None:
            return

        new_tree_value = self.repo[new_tree_sha]
        new_tree_data = new_tree_value.data

        file_path = tree_change.new.path
        file_ending = get_file_ending(file_path)

        if not self.is_allowed_path(path=file_path):
            return

        if change_type is 'delete':
            return


        if file_ending in self.file_endings:
            self.file_endings[file_ending] += new_tree_data.count('\n')
        else:
            self.file_endings[file_ending] = new_tree_data.count('\n')


    def report_file_endings(self):
        """
        """

        for ending in self.file_endings:
            print("%s: %s" % (ending, self.file_endings[ending]))



    def report_authors_commits(self):
        """
        """

        for author_name in self.authors:
            author_commit_count = self.authors[author_name]
            print("%s has %s commits" % (author_name, author_commit_count))



