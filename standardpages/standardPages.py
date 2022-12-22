"""
This file contains methods for standard pages counting.

Author: Simona Dlouha, xdlouh06@vutbr.cz
"""

def countStandardPages(numberOfCharacters):
    return round(numberOfCharacters/1800, 2)

def countStandardPagesFromImage(volume):
    return round(volume/(15.5 * 22.5), 2)

def countTotalNumberOfStandardPages(text, images):
    return round(text + images, 3)

def countChaptersStandardPages(chapters):
    sum = 0
    for chapter in chapters:
        sum += chapter.numberOfImageStandardPages + chapter.numberOfStandardPages
    return round(sum, 2)
