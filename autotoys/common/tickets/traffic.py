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
