import time

# Gireoan
from gireoan.report.Data import ReportData


class FileEndingReport(object):

    def __init__(self, paths):
        """
        """

        self.paths = paths
        self.data_list = []


    def generate(self):
        """
        """

        file_endings = {}

        # Get file ending info
        for file_path in self.paths:

            file_obj = self.paths[file_path]
            file_ending = file_obj.ending

            if file_ending in file_endings:
                file_endings[file_ending] += file_obj.code_lines
            else:
                file_endings[file_ending] = file_obj.code_lines
                
                
        for file_ending in file_endings:

            file_ending_count = file_endings[file_ending]
            report_data = ReportData(display_name=file_ending, data=file_ending_count)

            self.data_list.append(report_data)


    def report(self, exporter):
        """
        """

        exporter.export(data_list=self.data_list)


class AuthorsCommitReport(object):


    def __init__(self, authors):
        """
        """

        self.authors = authors
        self.data_list = []


    def generate(self):
        """
        """

        for author_name in self.authors:
            author = self.authors[author_name]
            self.generate_for_author(author=author)


    def generate_for_author(self, author):

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

        # The order has to be normal for the charts to work correctly
        reverse_sort_order = False

        data_list = []
        author_data_object = ReportData(display_name=author.name, data=data_list)

        self.data_list.append(author_data_object)

        sorted_years = sorted(years, reverse=reverse_sort_order)

        for year in sorted_years:

            year_dict = years[year]
            sorted_year_dict = sorted(year_dict, reverse=reverse_sort_order)

            for month in sorted_year_dict:

                month_dict = year_dict[month]
                sorted_month_dict = sorted(month_dict, reverse=reverse_sort_order)

                for day in sorted_month_dict:

                    commit_count = month_dict[day]
                    data_format_string = '{0}, {1}, {2}'.format(year, month, day)
                    day_commit_data = ReportData(display_name=data_format_string, data=commit_count)
                    data_list.append(day_commit_data)


    def report(self, exporter):
        """
        """

        exporter.export(data_list=self.data_list)