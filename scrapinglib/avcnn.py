import re

from .parser import Parser
import lxml.html


class Avcnn(Parser):
    source = 'avcnn'

    expr_number = '//div[starts-with(@class,"styles_mainHeaderMetaGroup_")]/div[2]/text()'
    expr_title = '//h1[starts-with(@class,"styles_mainHeaderTitle")]/span[2]/text()'
    expr_tags = '//div[starts-with(@class,"styles_mainHeaderMetaContainer")]/a/text()'
    expr_actor = '//div[starts-with(@class,"styles_articleContainer")]/div/a[1]/text()'

    # expr_actor = '//a[@class=styles_articleLink__ukyWs]/text()'

    def search(self, number):
        self.number = number.strip().upper()
        search_url = f"https://avcnn.com/article/{self.number}"
        self.detailurl = search_url
        self.htmlcode = self.getHtml(search_url)
        if self.htmlcode == 404:
            return 404
        htmltree = lxml.html.fromstring(self.htmlcode)
        print(htmltree)
        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        number = self.getTreeElement(htmltree, self.expr_number)
        # number = number.split("：")[1]
        return number

    # def getActors(self, htmltree):
    #     actors = self.getTreeElement(htmltree, self.expr_actor)
    #     return actors

    def getTitle(self, htmltree):
        title = self.getTreeElement(htmltree, self.expr_title).strip()
        return title

    def getCover(self, htmltree):
        cover = f"https://avcnn.com/video-cover/{self.number}/Cover.webp"
        return cover
