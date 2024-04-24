import openpyxl

from exceptions.exceptions import SourceError
from logger_utils.logger_utils import logger
from product_id_extract_services.product_id_extract_service import ProductIDExtractService


class ExcelProductIDExtractService(ProductIDExtractService):
    ids: list[int]

    def __init__(self, excel_file_path):
        super().__init__()
        self.excel_file_path = excel_file_path

    def get_ids(self) -> list:

        logger.info(f'ID source is excel file: {self.excel_file_path}')
        self.ids = []
        try:
            workbook = openpyxl.load_workbook(self.excel_file_path)
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, max_col=1, max_row=sheet.max_row, values_only=True):
                if row[0] is not None:
                    self.ids.append(row[0])

        except Exception:
            raise SourceError

        return self.ids
