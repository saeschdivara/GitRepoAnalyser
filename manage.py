from gireoan import Analyser
from gireoan.Errors import NoSettingsFileException


try:
    import local_settings
except:
    raise (NoSettingsFileException())

# Start main
if __name__ == '__main__':
    repo_analyser = Analyser.Analyser(
        repo_name=local_settings.REPOSITORY_PATH,
        searching_paths=local_settings.SEARCHING_PATHS,
        allowed_endings=local_settings.ALLOWED_ENDINGS,
        exclude_patters=local_settings.EXCLUDE_PATTERNS,
        exclude_paths=local_settings.EXCLUDE_PATHS
    )

    repo_analyser.do_analyse()
    repo_analyser.report_file_endings()
    repo_analyser.report_authors_commits()
    repo_analyser.report_top_10_commited_files()