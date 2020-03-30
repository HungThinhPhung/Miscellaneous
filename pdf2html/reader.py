from collections.abc import Iterable

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextLineHorizontal
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


class PdfReader():
    def __init__(self, file):
        self.file = file
        resource_manager = PDFResourceManager()
        self.device = PDFPageAggregator(resource_manager, laparams=LAParams(word_margin=0.15, char_margin=1.0))
        self.interpreter = PDFPageInterpreter(resource_manager, self.device)

    @staticmethod
    def __slice(obj):
        yield obj
        if isinstance(obj, Iterable):
            for v in obj:
                for k in PdfReader.__slice(v):
                    yield k

    def read_file(self):
        parser = PDFParser(self.file)
        pdf_document = PDFDocument(parser, caching=True)
        if not pdf_document.is_extractable:
            raise PDFTextExtractionNotAllowed

        result = []

        for page in PDFPage.create_pages(pdf_document):
            self.interpreter.process_page(page)
            layout = self.device.get_result()
            result.append(layout)
        return result

    def get_data(self):
        pages = self.read_file()
        data = []
        for page in pages:
            page_data = []
            for line in PdfReader.__slice(page):
                if not isinstance(line, LTTextLineHorizontal):
                    continue
                text = line.get_text().strip(' ')
                page_data.append(text)
            page_data = self.reformat_page(page_data)
            data.append(page_data)

        return data

    @staticmethod
    def reformat_page(page_data: list):
        i = len(page_data) - 1
        while not i == -1 and page_data[i] == '\n':
            i -= 1
        page_data = page_data[:i + 1]

        if page_data == []:
            return []
        i = 0
        while page_data[i] == '\n' and not i == len(page_data):
            i += 1
        page_data = page_data[i:]

        remove = []
        previous = None
        for i in range(len(page_data)):
            if not previous == '\n':
                previous = page_data[i]
                continue
            if page_data[i] == '\n':
                remove.append(i)
        for r in sorted(remove, reverse=True):
            del page_data[r]
        return page_data
