import grobidAltoStuff.scitex as scitex
import os

INPUT = "CelloGraph-main/scitex/scitexIn"
OUTPUT = "CelloGraph-main/scitex/scitexOut/"


#run grobid on the entire INPUT folder.
grobidCMD = "java -Xmx4G -jar grobid/grobid-core/build/libs/grobid-core-0.7.2-SNAPSHOT-onejar.jar -gH grobid/grobid-home -dIn " + INPUT + " -dOut " + OUTPUT + " -exe processFullText -ignoreAssets"

os.system(grobidCMD)

#for each thing in the INPUT folder
for root, dirs, files in os.walk(INPUT):
    for file in files:
        if file.endswith(".pdf"):
            gro = OUTPUT + file[:-4] + ".tei.xml"
            alto = OUTPUT + file[:-4] + "Alto.lxml"
            sci = OUTPUT + file[:-4] + "SciTEx.xml"
            file = os.path.abspath(INPUT + "/" + file)
            
            #run pdfalto
            #we put extra quotes around the filepaths because if a PDF name has whitespace the terminal throws a fit.
            pdfAltocmd = "grobid/grobid-home/pdfalto/lin-64/pdfalto -fullFontName -noLineNumbers -noImage \"" + file + "\" \"" + alto + "\""
            os.system(pdfAltocmd)


            #run scitex
            scitex.addScript(gro, alto, sci)

            #remove grobid and pdfalto outputs
            os.system("rm " + "\"" + gro + "\"")
            os.system("rm " + "\"" + alto + "\"")
            os.system("rm " + "\"" + alto + "_metadata.xml\"")


