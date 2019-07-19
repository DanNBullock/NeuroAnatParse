# -*- coding: utf-8 -*-
import PyPDF4 
  
# creating a pdf file object 
pdfFileObj = open('/N/u/dnbulloc/Carbonate/PDFs/PDFs/Evolution and development of interhemispheric connections in the vertebrate forebrain.pdf', 'rb') 
  
# creating a pdf reader object 
pdfReader = PyPDF4.PdfFileReader(pdfFileObj) 
  
# printing number of pages in pdf file 
print(pdfReader.numPages) 
  
# creating a page object 
pageObj = pdfReader.getPage(0) 
  
# extracting text from page 
print(pageObj.extractText()) 