import re

from .parser import Parser
import lxml.html


class Ggjav(Parser):
    source = 'ggjav'

    expr_number = '//div[@class="columns large-6 medium-4"]/div[1]/text()'
    expr_title = '//div[@class="columns small-12 title_text"]/text()'
    expr_cover = '//div[@class="info columns small-12"]//img/@src'

    def search(self, number):
        self.number = number
        if 'fc2' in number.lower():
            self.num = re.search(r'(\d\d\d\d\d\d\d)', number).group()
            self.number = "fc2-ppv-" + self.num
        search_url = f"https://ggjav.com/main/search?string={self.number}"
        self.htmlcode = self.getHtml(search_url)
        # htmltree = etree.fromstring(self.htmlcode, etree.HTMLParser())
        # result = self.dictformat(htmltree)
        if self.htmlcode == 404:
            return 404
        htmltree = lxml.html.fromstring(self.htmlcode)
        href = self.getTreeElement(htmltree,
                                   '//div[@class="columns large-3 medium-6 small-12 item float-left"]/a/@href',
                                   # '//div[starts-with(@class,columns)]'
                                   )
        if not href or href == '':
            return ""
        self.detailurl = f"https://ggjav.com/{href}"
        self.htmlcode = self.getHtml(self.detailurl)
        htmltree = lxml.html.fromstring(self.htmlcode)
        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        number = self.getTreeElement(htmltree, self.expr_number)
        number = number.split("：")[1]
        # if self.num and number == self.num:
        #     return self.number
        return number

    def getCover(self, htmltree):
        cover = self.getTreeElement(htmltree, self.expr_cover)
        return cover

    def getTitle(self, htmltree):
        return self.getTreeElement(htmltree, self.expr_title).strip()
