# -*- coding: utf-8 -*-
import re
import logging
import os

import pdfplumber

LOG = logging.getLogger(__name__)


class TrafficTicket(object):

    def __init__(self, file) -> None:
        self.file = file
        self.text = None

    @property
    def name(self):
        return os.path.basename(self.file)

    @property
    def code(self):
        found = re.findall(r'发 *票 *代 *码 *. *([0-9]+)', self.text)
        return found and found[0]

    @property
    def number(self):
        found = re.findall(r'发 *票 *号 *码 *. *([0-9]+)', self.text)
        return found and found[0]

    @property
    def date(self):
        found = re.findall(r'开 *票 *日 *期 *. *([0-9年月日 ]+)', self.text)
        return found and found[0].replace(' ', '')

    @property
    def check_code(self):
        found = re.findall(r'校 *验 *码 *. *([0-9 ]+)', self.text)
        return found and found[0].replace(' ', '')

    @property
    def money(self):
        found = re.findall(r'.小写. *. *([0-9.]+)', self.text)
        return found and found[0].replace(' ', '')

    def parse(self):
        with pdfplumber.open(self.file) as pdf:
            LOG.debug('page num is %s', len(pdf.pages))
            page = pdf.pages[0]
            self.text = page.extract_text()

    def rename(self, new_name):
        _, ext = os.path.splitext(os.path.basename(self.file))
        dest_file = os.path.join(os.path.dirname(self.file),
                                 f'{new_name}{ext}')
        LOG.debug('rename %s to: %s', self.file, dest_file)
        os.rename(self.file, dest_file)
        self.file = dest_file


def screenshot_and_merge(pdf_list, output=None):
    import fitz
    from PIL import Image
    import tempfile
    import fpdf

    merged_pdf = fpdf.FPDF()
    x, y = 0, 0
    img_width = 98
    img_heigh = 144
    img_num = 0
    for pdf_file in pdf_list:
        pdf = fitz.Document(pdf_file)
        page = pdf[0]
        mattrix = fitz.Matrix(1, 1)

        pixmap = page.get_pixmap(matrix=mattrix, alpha=False)
        with tempfile.TemporaryFile('wb', suffix='.png') as tmp_img:
            LOG.debug('saving image to temp %s %s', tmp_img.name, img_num)
            pixmap.save(tmp_img.name)
            im = Image.open(tmp_img.name)
            new_im = im.transpose(Image.ROTATE_90)
            new_im.save(tmp_img.name, quality=95, subsampling=0)

            if (img_num % 4) == 0:
                merged_pdf.add_page()
            merged_pdf.image(tmp_img.name, x, y, img_width, type='png')
            img_num += 1
            os.remove(tmp_img.name)
        x = (x == 0) and (x + img_width + 10) or 0
        y = (x == 0) and (y + img_heigh + 2) or y

    merged_pdf.output(os.path.join(output or '.', 'merge.pdf'))
    LOG.info('output merged pdf: %s', 'merge.pdf')
