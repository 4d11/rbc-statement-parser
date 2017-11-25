""" Reference: http://denis.papathanasiou.org/posts/2010.08.04.post.html"""

from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure

def to_bytestring (s, enc='utf-8'):
    """Convert the given unicode string to a bytestring, using the standard encoding,
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)

def update_page_text_hash (h, lt_obj, pct=0.2):
    """Use the bbox x0,x1 values within pct% to produce lists of associated text within the hash"""
    x0 = lt_obj.bbox[0]
    x1 = lt_obj.bbox[2]

    key_found = False
    for k, v in h.items():
        hash_x0 = k[0]
        if x0 >= (hash_x0 * (1.0-pct)) and (hash_x0 * (1.0+pct)) >= x0:
            hash_x1 = k[1]
            if x1 >= (hash_x1 * (1.0-pct)) and (hash_x1 * (1.0+pct)) >= x1:
                # the text inside this LT* object was positioned at the same
                # width as a prior series of text, so it belongs together
                key_found = True
                v.append(to_bytestring(lt_obj.get_text()))
                h[k] = v
    if not key_found:
        # the text, based on width, is a new series,
        # so it gets its own series (entry in the hash)
        h[(x0,x1)] = [to_bytestring(lt_obj.get_text())]

    return h


def parse_lt_objs (lt_objs, page_number, text_content=None):
    """Iterate through the list of LT* objects and capture the text or image data contained in each"""
    if text_content is None:
        text_content = []

    page_text = {} # k=(x0, x1) of the bbox, v=list of text strings within that bbox width (physical column)
    for lt_obj in lt_objs:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # text, so arrange is logically based on its column width
            text = to_bytestring(lt_obj.get_text())
            text_content.append(text)
             # page_text = update_page_text_hash(page_text, lt_obj)
        elif isinstance(lt_obj, LTFigure):
            # LTFigure objects are containers for other LT* objects, so recurse through the children
            text_content.append(parse_lt_objs(lt_obj, page_number, text_content))

    # for k, v in sorted([(key,value) for (key,value) in page_text.items()]):
    #     sort the page_text hash by the keys (x0,x1 values of the bbox),
    #     which produces a top-down, left-to-right sequence of related columns
    #     text_content.append(''.join(v))

    print(text_content)
    return '\n'.join(text_content)


class StatementParser():
    def parse(self, file, password=''):
        fp = open(file, 'rb')
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        document = PDFDocument(parser, password)
        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            print("not extractable")

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()
        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

        # Set parameters for analysis.
        laparams = LAParams(all_texts=True)
        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        text_content = []
        for i, page in enumerate(PDFPage.create_pages(document)):
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = device.get_result()
            print(layout)
            text_content.append(parse_lt_objs(layout, (i + 1)))
        return text_content

if __name__ == '__main__':
    path = 'data/derp.pdf'
    sp = StatementParser()
    x = sp.parse(path)

"""
from pdf2 import StatementParser as SP
path = 'data/derp.pdf'
sp = SP()
x = sp.parse(path)

"""