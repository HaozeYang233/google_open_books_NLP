# HTML document parser to process the books provided for the Data Mining module
# create a txt file for each book with parsed text from html
from bs4 import SoupStrainer
import os
import codecs
import re

# Initialize global variables
baseFolder = "/Users/nicolavitale/Desktop/DataMining-COMP6237/Individual/Data/gap-html/"
pTags = SoupStrainer("p")
open = codecs.open

# Loop to iterate through the subfolders of the baseFolder path
for rSDir, rDirs, rFiles in os.walk(baseFolder):
    for sSdir, sDirs, sFiles in os.walk(os.path.join(baseFolder, rSDir)):
# Loops through the files in the folder sSdir
# for sSdir, sDirs, sFiles in os.walk(baseFolder):
        bodyFile = open(sSdir + "-body.txt", 'w+', encoding="utf-8")
        for cFile in sFiles:
            # print(os.path.join(sSdir, cFile))
            lFile = open(os.path.join(sSdir, cFile), "r").read()  # , encoding="utf-8"
            cleanHtml = re.sub(r'<head>(.*?)</head>', ' ', lFile, flags=re.DOTALL)
            cleanHtml = re.sub(r'<!DOC(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'<span(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'</span(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'<div(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'</div(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'<p(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'</p(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'<body(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'</body(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'<html(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'</html(.*?)>', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'&(.*?);', '', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'[^a-zA-Z\s\/<>-]+', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'\s[a-zA-Z]\s{1}', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'\/\s{1}', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'[\s]+', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'>\s', '>', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'\s<', '<', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'[\s]+', ' ', cleanHtml, flags=re.DOTALL)
            cleanHtml = re.sub(r'<p>.{2}<\/p>|<p>.{1}<\/p>|<p><\/p>', '', cleanHtml, flags=re.DOTALL)
            cleanHtml = cleanHtml.replace('\n', '')
            cleanHtml = re.sub(r'\b-<br>\b', '', cleanHtml)
            cleanHtml = re.sub(r'\b-</p><p>\b', '', cleanHtml)
            cleanHtml = re.sub(r'<br>|-', ' ', cleanHtml)
            cleanHtml = re.sub(r'>\s', '>', cleanHtml)
            cleanHtml = re.sub(r'\s<', '<', cleanHtml)
            cleanHtml = re.sub(r'[\s]+', ' ', cleanHtml)
            bodyFile.write(cleanHtml.encode("ascii", errors="ignore") + '\n')
        bodyFile.close()
