# -*- coding: utf-8 -*-
import re

from .parser import Parser
import lxml.html


class Javbit(Parser):
    source = 'javbit'

    expr_number = "//h3/em/text()"
    expr_title = '//h2[@class="postTitle"]/span/a/text()'

    expr_cover = '//div[@class="postContent"]//img/@src'

    expr_actor = '//div[@class="postContent"]/p[3]/text()'

    def search(self, number):
        self.number = number.strip().upper()
        self.detailurl = f"https://javbit.net/?s={self.number}"
        self.htmlcode = self.getHtml(self.detailurl)
        # htmltree = etree.fromstring(self.htmlcode, etree.HTMLParser())
        # result = self.dictformat(htmltree)
        if self.htmlcode == 404:
            return 404
        htmltree = lxml.html.fromstring(self.htmlcode)
        result = self.dictformat(htmltree)
        return result

    def getActors(self, htmltree):
        actor = self.getTreeElement(htmltree, self.expr_actor, 0)
        return actor

    def getTags(self, htmltree) -> list:
        alls = self.getTreeElement(htmltree, self.expr_actor, 1)
        tags = []
        for t in alls.strip().split():
            tags.append(t)
        return tags
