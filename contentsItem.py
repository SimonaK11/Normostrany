"""
This file contains class ContentsItem. Instance of this class represents item of a thesis contents.

Author: Simona Dlouha, xdlouh06@vutbr.cz
"""

class ContentsItem:
    def __init__(self, startPage, title, itemNumber):
        self.startPage = startPage
        self.itemNumber = itemNumber
        self.title = title