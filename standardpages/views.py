"""
This file contains view, in which is processed given file into File class instance and new HTML file is rendered.

Author: Simona Dlouha, xdlouh06@vutbr.cz
"""

from django.shortcuts import render
from file import File
import gc
import fitz

def index(request):
    if request.method == 'POST':
        if 'myfile' not in request.FILES:
            return render(request, 'standardpages/index.html', {
                'wrong_file': "Nebyl vybrán žádný soubor"
            })
        myfile = request.FILES['myfile']
        try:
            doc = fitz.open(myfile.temporary_file_path())
        except:
            return render(request, 'standardpages/index.html', {
                'wrong_file': "Nahraný soubor se nepodařilo přečíst"
            })
        if not doc.isPDF:
            return render(request, 'standardpages/index.html', {
                'wrong_file': "Nahraný soubor nelze přečíst jako PDF"
            })
        file = File(doc)
        myfile.close()
        filename = request.FILES['myfile'].name
        fileAttributes = {
            'number_of_standart_pages': file.numberOfStandardPages,
            'number_of_characters' : file.numberOfCharacters,
            'number_of_images' : file.numberOfImages,
            'image_pixels': file.imageVolume,
            'average_image_size': file.averageImageSize,
            'number_of_standard_pages_image': file.numberOfStandardPagesImage,
            'total_number_of_sp' : file.totalNumberOfStandardPages,
            'sorted_images' : file.sortedImages,
            'most_frequent_words' : file.mostFrequentWords,
            'number_of_pages' : file.numberOfPages,
            'number_of_words' : file.numberOfWords,
            'number_of_sentences' : file.numberOfSentences,
            'number_of_characters_wo_spaces': file.numberOfCharactersWOSpaces,
            'image_percentage' : file.imagesPercentage,
            'text_percentage' : file.textPercentage,
            'chapters' : file.chapters,
            'chapters_standard_pages' : file.chaptersStandardPages,
            'filename': filename
        }
        del file
        del myfile
        gc.collect()
        return render(request, 'standardpages/index.html', fileAttributes)

    return render(request, 'standardpages/index.html')