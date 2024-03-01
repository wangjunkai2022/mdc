import re
from lxml import etree
from urllib.parse import urljoin

from .parser import Parser


class Missav(Parser):
    source = 'missav'

    def search(self, number):
        self.number = number.lower().replace('fc2-', 'fc2-ppv-').replace('fc2ppv-', 'fc2-ppv-')
        if self.specifiedUrl:
            self.detailurl = self.specifiedUrl
        else:
            self.detailurl = 'https://missav.com/dm13/cn/' + self.number + '/'
        self.htmlcode = self.getHtml(self.detailurl)
        if self.htmlcode == 404:
            return 404
        htmltree = etree.HTML(self.htmlcode)
        result = self.dictformat(htmltree)
        return result