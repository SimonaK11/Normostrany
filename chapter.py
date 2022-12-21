"""
This file contains class Chapter. Instance of this class represents chapter of a thesis.

Author: Simona Dlouha, xdlouh06@vutbr.cz
"""

from standardpages.standardPages import countStandardPagesFromImage, countStandardPages

class Chapter:
    def __init__(self, contentItem, endPage, images, numberOfCharacters):
        self.contentItem = contentItem
        self.endPage = None if endPage is None else endPage - 1
        self.numberOfCharacters = numberOfCharacters
        self.imageVolume = 0
        self.numberOfImages = 0
        self.numberOfPages = None if self.endPage is None else (self.endPage - self.contentItem.startPage + 1)

        for image in images:
            if(image.page >= self.contentItem.startPage):
                if(self.endPage is None or image.page <= self.endPage):
                    self.imageVolume += image.content
                    self.numberOfImages += 1
        self.imageVolume = round(self.imageVolume, 2)
        self.numberOfImageStandardPages = countStandardPagesFromImage(self.imageVolume)
        self.numberOfStandardPages = countStandardPages(self.numberOfCharacters)