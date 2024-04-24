import sys

from settings import DEFAULT_EXCEL_FILE_PATH


class FileProvider:
    @staticmethod
    def get_file_path() -> str:
        args = sys.argv
        if '--ids-file-path' not in args:
            excel_file_path = DEFAULT_EXCEL_FILE_PATH
        else:
            excel_file_path_index = args.index("--ids-file-path") + 1
            excel_file_path = args[excel_file_path_index]
        return excel_file_path
