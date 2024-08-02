import re
from lxml import etree
from urllib.parse import urljoin

from .parser import Parser


class Missav(Parser):
    source = 'missav'

    expr_number = "//div[@class='space-y-2']/div[@class='text-secondary']/span[@class='font-medium']/text()"
    expr_cover = '//div[@class="plyr__poster"/'
    expr_cover2 = ''

    expr_title = "//h1[@class='text-base lg:text-lg text-nord6']/text()"

    def search(self, number):
        self.number = number.lower().replace(
            'fc2-', 'fc2-ppv-').replace('fc2ppv-', 'fc2-ppv-')
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

    def getNum(self, htmltree):
        return self.getTreeElement(htmltree, self.expr_number, 1)

    def getTitle(self, htmltree):
        title = self.getTreeElement(
            htmltree, self.expr_number, 2).replace("＆quot", "_")
        if not title or title == '':
            return self.getNum()

    def getYear(self, htmltree):
        return self.getTreeElement(htmltree, self.expr_number, 0)

    def getCover(self, htmltree):
        return f"https://eightcha.com/{self.number}/cover.jpg"
