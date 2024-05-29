import grobidAltoStuff.grobidStuff as grobidStuff
import grobidAltoStuff.altoStuff as altoStuff
import grobidAltoStuff.tryingDiff as tryingDiff


#takes 3 string filepaths
#grobidpath and altopath are the filepaths to the output of grobid and pdfalto, respectively.
#outputpath is wherever you want the scitex output to go.
def addScript(grobidpath, altopath, outputpath):

    #run other functions to get the list of words from grobid and all the pdfalto information.
    bodyStrings = grobidStuff.grobidBodyWords(grobidpath)
    altoStrings, altoWords, subFonts, superFonts = altoStuff.AltoLists(altopath)

    #find all the subscript/superscript in the body text.
    bodySupers, bodySubs = matchStuff(bodyStrings, altoStrings, altoWords, subFonts, superFonts)

    #get the words from the figure captions.
    figStrings = grobidStuff.grobidFigWords(grobidpath)
    
    #find super/sub script in the figure captions.
    figSupers, figSubs = matchStuff(figStrings, altoStrings, altoWords, subFonts, superFonts)

    supers = [bodySupers, figSupers]
    subs = [bodySubs, figSubs]

    #put the tags in and produce the output.
    grobidStuff.rebuild(grobidpath, outputpath, supers, subs)

    

#takes a list of words from grobid, and a lot of lists from pdfalto.
#returns a list of indices for where superscript and subscript are in the grobid xml file.
def matchStuff(groStrings, altoStrings, altoWords, subFonts, superFonts):
    #run difflib on the grobid and pdfalto text.
    matches = tryingDiff.getMatches(groStrings, altoStrings)

    subs = []
    supers = []

    #for each piece of text that lines up between the two xml files...
    for match in matches:
        altDex, groDex, matchLen = match
        #...look through it for subscript/superscript
        for i in range(matchLen):
            script = altoStuff.isScript(altoWords[altDex+i], superFonts, subFonts)

            #if we find subscript or superscript, add it to the respective list.
            if(script == "super"):
                supers.append([groDex+i, groStrings[groDex+i]])
            if(script == "sub"):
                subs.append([groDex+i, groStrings[groDex+i]])

    #return the super/sub script lists.
    return supers, subs
