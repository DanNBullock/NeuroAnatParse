# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import numpy
import nltk


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
    cropDim=[50, 50, -50, -50]

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        #mediabox works, crobox does not
        #maybe replace this with https://pypi.org/project/pdfCropMargins/
        page.mediabox=numpy.ndarray.tolist(numpy.add(page.cropbox,cropDim))
        interpreter.process_page(page)
        
    #impliment term replacement function here.

    text = retstr.getvalue()


    
    fp.close()
    device.close()
    retstr.close()
    return text

def replace_text_terms(text):
    #clean newlines out
    text = text.replace('\n',' ')
    #join hyphen line splits
    text = text.replace('- ','')
    #replace abbreviation
    text = text.replace('\x0c',' ')
    import csv
    with open('/N/u/dnbulloc/Carbonate/PDFs/Code/Lexicons/ReplaceTerms', newline='\n') as csvfile:
        replaceText = csv.reader(csvfile, delimiter=',')
        for row in replaceText:
            dates.append(row[0])
            scores.append(row[1])
    
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
        introductionInd = [0]
    
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

#from https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


def make_corpus_freq_matricies(corpusTextString):
    corpusTextStringLower=corpusTextString.lower()
    sentencesProto=corpusTextStringLower.split('. ')
    
    #temporary hardcoding to anatomy terms
    anatTermsObject=open('/N/u/dnbulloc/Carbonate/PDFs/Code/Lexicons/AnatomicalTermsTemp','r')
    anatTerms = anatTermsObject.read().split('\n')
    
    #fix due to last newline
    anatTerms=anatTerms[0:-1]
    
    #initialize index matrix
    AnatIndex=numpy.zeros((len(sentencesProto),len(anatTerms)))
    
    #iterate over sentences
    for iSentence in range(len(sentencesProto)):
        for iAnat in range(len(anatTerms)):
            curSentence=sentencesProto[iSentence]
            curWords=curSentence.split(' ')
            #https://docs.python.org/3/glossary.html#term-lbyl
            AnatIndex[iSentence,iAnat]=curWords.index(anatTerms[iAnat]) if anatTerms[iAnat] in curWords else numpy.nan
            
    #temporary hardcoding to positional terms
    positTermsObject=open('/N/u/dnbulloc/Carbonate/PDFs/Code/Lexicons/PositionalTerms','r')
    positTerms = anatTermsObject.read().split('\n')
        
    for iSentence in range(len(sentencesProto)):
        #the logic is that at least two of the words are anatomy terms
        numpy.count_nonzero(~numpy.isnan(AnatIndex[iSentence,:]))
        if numpy.count_nonzero(~numpy.isnan(AnatIndex[iSentence,:]))>=2:
            print(sentencesProto[iSentence])
    
    


    





corpusTextString=clean_journal_pdf('/gpfs/home/d/n/dnbulloc/Carbonate/PDFs/PDFs/Bullock et al. Posterior Vertical Associative White Matter - ARXIV.pdf')

sentencesProto=pdfCleaned.split('. ')
 
testSentence=sentencesProto[1]



path='/N/u/dnbulloc/Carbonate/PDFs/PDFs/7604.full.pdf'


pageOut=PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True)