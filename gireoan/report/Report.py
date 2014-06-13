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

            file = self.paths[file_path]
            file_ending = file.ending

            if file_ending in file_endings:
                file_endings[file_ending] += file.code_lines
            else:
                file_endings[file_ending] = file.code_lines
                
                
        for file_ending in file_endings:

            file_ending_count = file_endings[file_ending]
            report_data = ReportData(display_name=file_ending, data=file_ending_count)

            self.data_list.append(report_data)


    def report(self, exporter):
        """
        """

        exporter.export(data_list=self.data_list)
