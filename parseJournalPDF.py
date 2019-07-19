# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import numpy



def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    
    #figure out a better way to do this, maybe not hardcoded?
    # 1 in on all sides, 1 in = 96 pixels
    cropDim=[95, 95, -95, -95]

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        #mediabox works, crobox does not
        #maybe replace this with https://pypi.org/project/pdfCropMargins/
        page.mediabox=numpy.ndarray.tolist(numpy.add(page.cropbox,cropDim))
        interpreter.process_page(page)

    text = retstr.getvalue()
    #clean newlines out
    text = text.replace('\n',' ')
    #join hyphen line splits
    text = text.replace('- ','')
    #get rid of troublsome period
    text = text.replace('et al.','et al')
    #replace abbreviation
    text = text.replace('cf.','compare')
    #replace abbreviation
    text = text.replace('i.e.','in other words')
    #replace abbreviation
    text = text.replace('e.g.','for example')
    #replace abbreviation
    text = text.replace('p.','page')
    #replace abbreviation
    text = text.replace('Fig.','Figure')
    #completely remove abbreviated names, just a brute force tactic.
    #text = text.replace('[A-Z]\.[A-Z]\.','')
    
    #what do we do about numbers
    
    fp.close()
    device.close()
    retstr.close()
    return text

#define clean journal function
def clean_journal_pdf(path):
    #get 'raw' pdf output.  Truely though, the convert function does some of its own  
    out=convert_pdf_to_txt(path)
    wordProto=out.split(' ')
    
    #find starting point index, defaults to 0 if introduction isnt found
    if len([i for i, x in enumerate(wordProto) if x == "Introduction"])>0:
        introductionInd = [i for i, x in enumerate(wordProto) if x == "Introduction"]
    else:
        introductionInd = list(0)
    
    #find potential endingPoint, default usage makes robust against empty,
    #max usage ensures final instance of word
    if len( [i for i, x in enumerate(wordProto) if x == "References"])>0:
        referencesInd = [i for i, x in enumerate(wordProto) if x == "References"]
    else:
        referencesInd=[len(wordProto)]
        
    if len([i for i, x in enumerate(wordProto) if x == "Citations"])>0:
        citationsInd = [i for i, x in enumerate(wordProto) if x == "Citations"]
    else:
        citationsInd = [len(wordProto)]
        
    if len([i for i, x in enumerate(wordProto) if x == "Acknowledgements"])>0:
        AcknowledgementInd =[i for i, x in enumerate(wordProto) if x == "Acknowledgements"]
    else:
        AcknowledgementInd =[len(wordProto)]
    #make a list of the 
    cutOffIndList=sorted([max(referencesInd)]+[max(citationsInd)]+[max(AcknowledgementInd)])
    
    #initialize two empty lists for words and counts
    wordSpace= [None] * len(wordProto)
    dotCount2= [None] * len(wordProto)
    #loop over words to add space that was removed with split
    for i in range(len(wordProto)):
        wordSpace[i] = wordProto[i]+' '
        
        #DO SECONDARY / INELEGANT WORD CLEANING HERE
        #counting double periods for name abbreviations
        dotCount2[i]=wordProto[i].count('.')==2
        #find relevant indexes    
        doubleDotInd=[i for i, x in enumerate(dotCount2) if x]
    
    #remove periods in name abbreviations
    for i in doubleDotInd:
        wordSpace[i] = wordSpace[i].replace('.','')
    
    #cut it down to the desired words
    pdfTextList=wordSpace[introductionInd[0]+1:cutOffIndList [0]-1]
    #join them
    pdfCleaned=''.join(pdfTextList)
    return pdfCleaned

pdfCleaned=clean_journal_pdf('/N/u/dnbulloc/Carbonate/PDFs/PDFs/1-s2.0-S0959438800001963-main.pdf')

sentencesProto=pdfCleaned.split('. ')
 



path='/N/u/dnbulloc/Carbonate/PDFs/PDFs/1-s2.0-S0959438800001963-main.pdf'


pageOut=PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True)