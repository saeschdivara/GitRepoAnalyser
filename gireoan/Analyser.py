# Time
import time
# Regex
import re

# Git
from dulwich.repo import Repo
from dulwich.objects import Blob

# Gireoan
from gireoan.repo import Author
from gireoan.repo.File import File

from gireoan.report.Export import ChartExporter
from gireoan.report.Report import FileEndingReport, AuthorsCommitReport



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

            if not author_name in self.authors:
                self.authors[author_name] = Author.Author(name=author_name)

            self.authors[author_name].commits.append( change_tree.commit )

            for tree_change in change_tree.changes():
                # Save tree data
                self._save_tree_data(change_tree=change_tree, tree_change=tree_change)


    def report_file_endings(self):
        """
        """

        file_ending_report = FileEndingReport(paths=self.file_paths)
        file_ending_report.generate()

        chart_type = ChartExporter.EXPORT_TYPE['PIE']
        file_ending_report.report(exporter=ChartExporter(type=chart_type))
        #
        # # Print report
        # print("############################################")
        #
        # for ending in file_endings:
        #     print("%s: %s" % (ending, file_endings[ending]))
        #
        # print("############################################")


    def report_authors_commits(self):
        """
        """

        print("############################################")

        for author_name in self.authors:
            author_commit_count = len( self.authors[author_name].commits )
            print("%s has %s commits" % (author_name, author_commit_count))

        print("############################################")


    def report_commits_per_file(self):

        print("############################################")

        for file_path in self.file_paths:
            repo_file = self.file_paths[file_path]
            file_commit_count = len(repo_file.commits)
            print("%s is in %s commits" % (repo_file.path, file_commit_count))

        print("############################################")


    def report_top_10_commited_files(self):

        print("############################################")

        top_ten = []

        for file_path in self.file_paths:
            top_ten.append(self.file_paths[file_path])

        # Sort the files by the number of commits
        sorted_top_ten = sorted(top_ten, key=lambda repo_file: len(repo_file.commits), reverse=True)

        for idx, repo_file in enumerate(sorted_top_ten):

            # To have correct index we need to check here
            if idx is 10:
                break

            file_commit_count = len(repo_file.commits)
            print("%s is in %s commits" % (repo_file.path, file_commit_count))

        print("############################################")


    def report_for_all_authors(self):
        """
        """


        author_commit_report = AuthorsCommitReport(authors=self.authors)
        author_commit_report.generate()

        chart_type = ChartExporter.EXPORT_TYPE['SPLINE']
        author_commit_report.report(exporter=ChartExporter(type=chart_type))


    def report_for_author(self, name):
        """
        """

        author = self.authors[name]

        print("############################################")
        print("Author: %s" % author.name)

        # year
        years = {}

        for commit in author.commits:

            author_commit_time = time.localtime(commit.author_time)

            commit_year = str(author_commit_time.tm_year)

            if not commit_year in years:
                years[commit_year] = {}

            this_year = years[commit_year]
            commit_month = author_commit_time.tm_mon

            if not commit_month in this_year:
                this_year[commit_month] = {}

            this_month = this_year[commit_month]
            commit_day = author_commit_time.tm_mday

            if not commit_day in this_month:
                this_month[commit_day] = 0

            this_month[commit_day] += 1


            # author_commit_time = time.ctime(commit.author_time)
            # print("%s : %s" % (author_commit_time, commit.sha))

        reverse_sort_order = True

        sorted_years = sorted(years, reverse=reverse_sort_order)

        for year in sorted_years:
            print("Year %s:" % year)

            year_dict = years[year]
            sorted_year_dict = sorted(year_dict, reverse=reverse_sort_order)

            for month in sorted_year_dict:
                print('     Month %s:' % month)

                month_dict = year_dict[month]
                sorted_month_dict = sorted(month_dict, reverse=reverse_sort_order)

                for day in sorted_month_dict:
                    if day < 10:
                        print('             Day  %s: %s' % (day, month_dict[day]))
                    else:
                        print('             Day %s: %s' % (day, month_dict[day]))

        print("############################################")



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
                if not self._is_in_search_path(path=path, search_path=search_path):
                    return False

            if file_ending not in self.ALLOWED_ENDINGS or self._has_repo_file(file_path=path):
                return False

        except Exception as err:
            print(err)

        return True


    def _save_tree_data(self, change_tree, tree_change):

        # Check if is list
        if type(tree_change) is list:

            for change in tree_change:
                self._parse_change_tree(change_tree=change_tree, tree_change=change)

        else:
            self._parse_change_tree(change_tree=change_tree, tree_change=tree_change)


    def _parse_change_tree(self, change_tree, tree_change):

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

            # Try to get repo file
            try:
                repo_file = self._get_repo_file(file_path=file_path)
                # Add commit to repo file
                repo_file.commits.append( change_tree.commit )
            except:
                pass

            # Check if file is in allowed path
            if not self._is_allowed_path(path=file_path):
                return

            counted_lines = new_tree_data.count('\n')

            # Get repo file
            repo_file = self._create_repo_file(file_path=file_path)
            # Set repo file data
            repo_file.code_lines = counted_lines
            repo_file.ending = file_ending
            repo_file.commits.append( change_tree.commit )


        elif change_type is 'delete':
            file_path = tree_change.old.path

            self.deleted_paths[file_path] = True


    def _is_in_search_path(self, path, search_path):
        """
        """

        if not path.startswith('/'):
            path = '/' + path

        if search_path == '':
            search_path = '/'
        elif not search_path.startswith('/'):
            search_path = '/' + search_path

        return path.startswith(search_path)


    def _create_repo_file(self, file_path):
        """
        """

        if not self._has_repo_file(file_path=file_path):

            file = File(path=file_path)
            self.file_paths[file_path] = file

            return file

        else:
            return None


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