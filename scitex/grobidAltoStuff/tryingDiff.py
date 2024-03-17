import difflib

#gro is the array of strings from the grobid XML output
#alto is the array of strings from the pdfAlto XML output

#returns a complicated list of where those two arrays line up, which makes up *most* of the input document.
def getMatches(gro, alt):
    seq = difflib.SequenceMatcher(b=gro, a=alt)

    matches = seq.get_matching_blocks()

    return matches