# Regex
import re

# Git
from dulwich.repo import Repo
from dulwich.objects import Blob

# Gireoan
from gireoan.repo.File import File



################################################################
# REPO ANALYSER CLASS
################################################################
class Analyser(object):

    #########################
    ## STATIC CLASS MEMBER ##
    #########################

    CHANGE_TYPES = (
        'add',
        'modify',
        'delete',
    )


    ####################
    ## PUBLIC METHODS ##
    ####################

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
        self.deleted_paths = {}

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
                self._save_tree_data(tree_change=tree_change)


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


    #####################
    ## PRIVATE METHODS ##
    #####################

    def _is_matching_exclude_pattern(self, path):
        """
        """

        for pattern in self.EXCLUDE_PATTERNS:

            p = re.compile(pattern)

            if p.match(path) is not None:
                return True

        return False


    def _in_exclude_path(self, path):
        """
        """

        for exclude_path in self.EXCLUDE_PATHS:

            if path.startswith(exclude_path):
                return True

        return False


    def _is_allowed_path(self, path):
        """
        """

        try:
            file_ending = File.get_ending(file_path=path)

            for search_path in self.SEARCHING_PATHS:

                # Looks if path in exclude path
                if self._in_exclude_path(path):
                    return False

                # Looks if path matches the excluding pattern
                if self._is_matching_exclude_pattern(path):
                    return False

                # TODO: Check out if this is logical
                # Looks if path starts not in a searching path
                if not path.startswith(search_path):
                    return False

            if file_ending not in self.ALLOWED_ENDINGS or self._has_repo_file(file_path=path):
                return False

            self._create_repo_file(file_path=path)

        except Exception as err:
            print(err)

        return True


    def _save_tree_data(self, tree_change):

        # Check if is list
        if type(tree_change) is list:

            for change in tree_change:
                self._parse_change_tree(tree_change=change)

        else:
            self._parse_change_tree(tree_change=tree_change)


    def _parse_change_tree(self, tree_change):

        change_type = tree_change.type

        if change_type is 'add' or change_type is 'modify':

            new_tree_sha = tree_change.new.sha
            new_tree_value = self.repo[new_tree_sha]
            new_tree_data = new_tree_value.data
            file_path = tree_change.new.path

            # Check if the file has not been later being deleted
            if file_path in self.deleted_paths:
                return

            file_ending = File.get_ending(file_path=file_path)

            # Check if file is in allowed path
            if not self._is_allowed_path(path=file_path):
                return

            counted_lines = new_tree_data.count('\n')

            repo_file = self._get_repo_file(file_path=file_path)
            repo_file.code_lines = counted_lines

            # Check if file ending is already registered
            if file_ending in self.file_endings:

                self.file_endings[file_ending] += counted_lines
            else:
                self.file_endings[file_ending] = counted_lines


        elif change_type is 'delete':
            file_path = tree_change.old.path

            self.deleted_paths[file_path] = True


    def _create_repo_file(self, file_path):
        """
        """

        if not self._has_repo_file(file_path=file_path):

            file = File(path=file_path)
            self.file_paths[file_path] = file


    def _get_repo_file(self, file_path):
        """
        """

        file = self.file_paths[file_path]
        return file


    def _has_repo_file(self, file_path):
        """
        """

        if file_path in self.file_paths:
            return True
        else:
            return False