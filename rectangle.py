"""
This file contains class Rectangle. Instance of this class represents an image from a thesis.

Author: Simona Dlouha, xdlouh06@vutbr.cz
"""

class Rectangle:
    def __init__(self, height, width, page):
        self.height = round(height, 2)
        self.width = round(width, 2)
        self.content = round(self.height * self.width, 2)
        self.page = page + 1