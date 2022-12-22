"""
This file contains methods for thesis file analysis.

Author: Simona Dlouha, xdlouh06@vutbr.cz
"""

import queue
import re
from rectangle import Rectangle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import  math
from contentsItem import ContentsItem
from contents import Contents
from chapter import Chapter

def getMostFrequentWords(wordsFrequency):
    if len(wordsFrequency) == 0:
        return None
    wordsFrequency = sorted(wordsFrequency.items(),  key=lambda kv: kv[1], reverse=True)[:50]
    wordsFrequency = dict(wordsFrequency)
    image = io.BytesIO()
    plt.figure(figsize=(20, 7))
    plt.gca().yaxis.grid(linestyle=':', zorder=0)
    rects = plt.bar(wordsFrequency.keys(), wordsFrequency.values(), color='#B8A68F', zorder=3)
    plt.xticks(rotation=50)
    plt.xlabel('Slovo',fontweight='bold')
    plt.ylabel('Četnost',fontweight='bold')
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.01 * height,
                '%d' % int(height),
                ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(image, format='png')
    plt.close()
    bytes = base64.encodebytes(image.getvalue())
    image.close()
    del rects
    return bytes.decode('ascii')

def countRectanglesVolume(imageRectangles):
    sum = 0
    for rectangle in imageRectangles:
        sum += rectangle.content
    return round(sum, 2)

def countImageCharacters(volume):
    return volume*10.1124

def countAverageImageSize(imageRectangles, volume):
    return None if imageRectangles.__len__() == 0 else round(math.sqrt(volume/imageRectangles.__len__()), 2)

def sortImages(imageRectangles):
    return sorted(imageRectangles, key=lambda x: x.content, reverse=True)

def cleanTextInconsistency(text):
    pattern1 = re.compile("U[˚°]( |)|[˚°] U")
    pattern2 = re.compile("u[˚°]( |)|[˚°] u")
    pattern3 = re.compile("[ˇ\-´]( |)")
    text = re.sub(pattern1, "U", text)
    text = re.sub(pattern2, "u", text)
    return re.sub(pattern3, "", text)

def cleanNewLines(text):
    return re.sub("(\r\n|\r|\n)( |)", "", text)

def appendRectangles(dict, imageRectangles, pixelsOnCentimeterY, pixelsOnCentimeterX, page):
    for bbox in dict:
        if bbox[6] == 1:
            imageRectangles.append(
                Rectangle((bbox[3] - bbox[1]) / pixelsOnCentimeterY, (bbox[2] - bbox[0]) / pixelsOnCentimeterX, page))

def hashWordsFrequency(splitText, wordsFrequency):
    for word in splitText:
        if len(word) > 2:
            word = word.lower()
            if word in wordsFrequency:
                wordsFrequency[word] += 1
            else:
                wordsFrequency[word] = 1

def getLongestCharactersCount(dictionary):
    return len(max(dictionary, key=len)) if len(dictionary) != 0 else None

def getLongestSentenceNumberOfWords(dictionary):
    longestSentence = max(dictionary, key=len) if len(dictionary) != 0 else None
    return len(longestSentence.split()) if longestSentence is not None else None

def getSentences(text):
    pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    return pat.findall(text)

def getNumberOfCharactersWithoutSpaces(text):
    text = re.sub(" ", "", text)
    return text.__len__()

def topTenLongestWords(wordsDictionary):
    return sorted(wordsDictionary, key=len, reverse=True)[:10]

def parseContents(words):
    i = 0
    contentsItems = queue.Queue()
    title = ""
    itemNumber = None
    lastItemNumber = 0
    newLineDetected = False
    pageNumberDetected = False
    lenghtOfLastItem = 0
    for i in range(len(words)):
        lenghtOfLastItem += 1
        word = words[i]
        if(newLineDetected and pageNumberDetected):
            itemNumber, newLineDetected, pageNumberDetected, lenghtOfLastItem = handlePageNumberDetected()
        if (word != "\n"):
            pageNumberDetected = False
            if(itemNumber is None):
                itemNumber, newLineDetected, pageNumberDetected = parseItemNumber(itemNumber, newLineDetected,
                                                                                  pageNumberDetected, word)
            else:
                try:
                    startPage = int(word)
                    if (not pageNumberDetected
                            and itemNumber is not None
                            and not re.fullmatch(r"\d+(\.\d+)+", str(itemNumber))):
                        try:
                            if (itemNumber > lastItemNumber):
                                lastItemNumber = addContentItem(contentsItems, itemNumber, lastItemNumber, startPage, title)
                            else:
                                i -= lenghtOfLastItem
                                break
                        except TypeError:
                            break
                    title = ""
                    itemNumber = None
                    lenghtOfLastItem = 0
                except ValueError:
                    newLineDetected, title = parseTitle(newLineDetected, title, word)
        else:
            newLineDetected = True
    return Contents(contentsItems, i)


def addContentItem(contentsItems, itemNumber, lastItemNumber, startPage, title):
    lastItemNumber = itemNumber
    contentsItems.put(ContentsItem(startPage, title, itemNumber))
    return lastItemNumber


def handlePageNumberDetected():
    return None, False, False, 0


def parseTitle(newLineDetected, title, word):
    if (newLineDetected):
        newLineDetected = False
    if (word != "." and not re.match(r"\.+", word)):
        title += word + " "
    return newLineDetected, title


def parseItemNumber(itemNumber, newLineDetected, pageNumberDetected, word):
    try:
        itemNumber = word
        itemNumber = int(itemNumber)
        if (newLineDetected):
            pageNumberDetected = True
            newLineDetected = False
    except ValueError:
        pass
    return itemNumber, newLineDetected, pageNumberDetected


def parseChapters(fileText, images):
    words = re.findall(r'\S+|\n', fileText)
    isContentParsed = False
    chapters = []
    contentsItems = None
    contentsItem = None
    itemFound = False
    nextContentsItem = None
    numberOfCharacters = 0
    firstItemFound = False
    i = 0
    while i < len(words):
        word = words[i]
        if(not isContentParsed):
            if(word == 'Obsah' or word == 'Contents'):
                contents = parseContents(words[i+1:])
                if contents is None:
                    return None
                i += contents.numberOfWords
                contentsItems = contents.contentItems
                if(contentsItems.empty()):
                    return None
                nextContentsItem = contentsItems.get()
                isContentParsed = True
            elif(word == 'Table' and words[i+1] == 'of' and words[i+2] == 'Contents'):
                i += 2
                contents = parseContents(words[i+3:])
                i += contents.numberOfWords
                contentsItems = contents.contentItems
                nextContentsItem = contentsItems.get()
                isContentParsed = True
        else:
            if(itemFound):
                if(not firstItemFound):
                    chapters.append(Chapter(contentsItem, nextContentsItem.startPage, images, numberOfCharacters))
                contentsItem = nextContentsItem
                if(contentsItems.empty()):
                    nextContentsItem = ContentsItem(None, None, None)
                else:
                    nextContentsItem = contentsItems.get()
                numberOfCharacters = 0
                itemFound = False
            if(word != "\n"):
                numberOfCharacters += len(word) + 1
            if(word == str(nextContentsItem.itemNumber)):
                firstItemFound = nextContentsItem.itemNumber == 1
                j = 0
                title = nextContentsItem.title.split()
                for titleWord in title:
                    if(words[i + j + 1] == '\n'):
                        i += 1
                    if(words[i + j + 1] != titleWord):
                        j = 0
                        break
                    j += 1
                i += j
                numberOfCharacters -= j
                itemFound = j != 0
        i += 1
    if(isContentParsed):
        chapters.append(Chapter(contentsItem, nextContentsItem.startPage, images, numberOfCharacters))
        return chapters
    else:
        return None

def isContentsPage(text):
    re_pattern = r'\b(?:Obsah|Contents)\b'
    return re.search(re_pattern, text) is not None