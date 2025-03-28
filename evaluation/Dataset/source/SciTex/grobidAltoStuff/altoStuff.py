import xml.etree.ElementTree as ET
import difflib as dl


# takes an array of strings and makes sure none of them are empty strings.
# textArr: array of strings, some of which may be empty.
# returns: array of strings, none of which are empty.
def clean(textArr):
    if(len(textArr) == 0):
        return textArr
    i = -1
    while i < len(textArr)-1:
        i += 1
        if(textArr[i] == ''):
            textArr.pop(i)
            i -= 1
    return textArr
        

#if the word's font is on the list of fonts, then return True
# word: a pdfalto Word object.
# supers: list of fonts that are marked as superscript.
# subs: list of fonts that are marked as subscript.
def isScript(word, supers, subs):
    word_id = word.get("STYLEREFS")
    for font in supers:
        font_id = font.get("ID")
        if(word_id == font_id):
            return "super"
    for font in subs:
        if(word_id == font_id):
            return "sub"
    return False


#takes a filepath to a pdfalto output XML file.
#returns stringList, wordList, superFonts, subFonts
#stringList is an array of strings
#wordList is an array of alto words
#superFonts is a list of font objects that are marked as superscript.
#subFonts is a list of font objects that are marked as subscript.

#Note: stringlist and wordlist both have the full text, they're just formatted differently.
def AltoLists(filepath):
    tree = ET.parse(filepath)
    
    wordList = []    
    stringList = []
    subFonts = []
    superFonts = []

    root = tree.getroot() 
    
    layout = root[2]
    page = layout[0]

    styles = root[1]

    #run through all the fonts and figure out which are subscript and which are superscript.
    for font in styles:
        style = font.get("FONTSTYLE")
        if(style):
            if("superscript" in style):
                subFonts.append(font)
            elif("subscript" in style):
                superFonts.append(font)

    #sift through the very intensive XML layout.
    for page in layout:
        for space in page:
            for block in space:
                for line in block:
                    for string in line:
                        #things in "line" will either be words or spaces, 
                        # words will have a CONTENT string.
                        if(string.get("CONTENT")):
                            wordList.append(string)
                            stringList.append(string.get("CONTENT"))
    
    #clean stringList, then return the output.
    stringList = clean(stringList)
    return stringList, wordList, superFonts, subFonts

