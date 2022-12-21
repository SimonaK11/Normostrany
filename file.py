"""
This file contains class File. Instance of this class represents an analyzed thesis file.

Author: Simona Dlouha, xdlouh06@vutbr.cz
"""
from standardpages.standardPages import countStandardPagesFromImage, countStandardPages, countTotalNumberOfStandardPages,\
                                        countChaptersStandardPages
from standardpages.fileAnalysis import getSentences, isContentsPage,\
                                       hashWordsFrequency, appendRectangles, countRectanglesVolume, \
                                       countAverageImageSize, getMostFrequentWords,sortImages,\
                                       cleanTextInconsistency, getNumberOfCharactersWithoutSpaces, parseChapters, \
                                       cleanNewLines
class File:
    def __init__(self, doc):
        fileText = ""
        numberOfWords = 0
        wordsFrequency = {}
        imageRectangles = []
        contentsPage = None
        page = doc.loadPage(0)
        pixelsOnCentimeterX = (page.MediaBoxSize.x / 21.0) if (page.MediaBoxSize.x < page.MediaBoxSize.y) else (page.MediaBoxSize.x / 29.7)
        pixelsOnCentimeterY = (page.MediaBoxSize.y / 29.7) if (page.MediaBoxSize.x < page.MediaBoxSize.y) else (page.MediaBoxSize.y / 21.0)
        for pg in doc:
            appendRectangles(pg.getTextBlocks(True), imageRectangles, pixelsOnCentimeterY, pixelsOnCentimeterX, pg.number if contentsPage is None else pg.number - contentsPage)
            text = pg.getText("text")
            if(contentsPage is None):
                if (isContentsPage(text)):
                    contentsPage = pg.number
                    for rectangle in imageRectangles:
                        rectangle.page = 0
            fileText += text
        fileText = cleanTextInconsistency(fileText)
        text = fileText.split()
        numberOfWords += text.__len__()
        hashWordsFrequency(text, wordsFrequency)

        self.numberOfPages = doc.pageCount
        doc.close()
        del doc
        del text
        del page
        sentences = getSentences(fileText)
        if(contentsPage is not None):
            self.chapters = parseChapters(fileText, imageRectangles)
            self.chaptersStandardPages = 0 if self.chapters is None else countChaptersStandardPages(self.chapters)
        else:
            self.chapters = None
            self.chaptersStandardPages = None
        fileText = cleanNewLines(fileText)
        self.numberOfCharacters = fileText.__len__()
        self.numberOfCharactersWOSpaces = getNumberOfCharactersWithoutSpaces(fileText)
        del fileText
        self.numberOfStandardPages = countStandardPages(self.numberOfCharacters)
        self.numberOfImages = imageRectangles.__len__()
        self.imageVolume = countRectanglesVolume(imageRectangles)
        self.averageImageSize = countAverageImageSize(imageRectangles, self.imageVolume)
        self.numberOfStandardPagesImage = countStandardPagesFromImage(self.imageVolume)
        self.totalNumberOfStandardPages = countTotalNumberOfStandardPages(self.numberOfStandardPages, self.numberOfStandardPagesImage)
        self.sortedImages = sortImages(imageRectangles)
        self.mostFrequentWords = getMostFrequentWords(wordsFrequency)
        self.numberOfWords = numberOfWords
        self.numberOfSentences = sentences.__len__()
        if(self.totalNumberOfStandardPages > 0):
            self.imagesPercentage = round((self.numberOfStandardPagesImage / self.totalNumberOfStandardPages) * 100)
            self.textPercentage = round((self.numberOfStandardPages / self.totalNumberOfStandardPages)* 100)
        else:
            self.imagesPercentage = self.textPercentage = 0

        imageRectangles.clear()

