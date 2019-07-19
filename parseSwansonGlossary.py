# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re

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

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    # found here: https://stackoverflow.com/questions/51436686/extract-text-from-pdf-table-of-contents-ignoring-page-and-indexing-numbers
    #text = text.replace('\n\n', ' ').replace('\n',' ').replace('?',' ').replace('_',' ').replace('\t',' ').encode('ascii', errors='replace').decode('utf-8').replace("?","").replace("\x0c","").replace(".","").replace('\\',"").replace('/',"").replace('\r',"").replace("-"," ").replace(".......*"," ")
    #text = text.replace('-\n','')
    #text = text.replace('\n',' ')
    text = text.replace('L i sT  o f  AL L  D e f i n eD\xa0 T e r m s\n\n','DELETENUMS')
    text = text.replace('DELETENUMS???',' ')
    #text = text.replace('(*,*), see','NAMEEND')
    #text = text.replace('\n\n','ENDLINE')
    text = text.replace('.\n\nd\ne\nv\nr\ne\ns\ne\nr\n \ns\nt\n\nh\ng\ni\nr\n \nl\nl\n\nA\n\n \n.\n\nd\ne\n\nt\n\na\nr\no\np\nr\no\nc\nn\n\nI\n \n,\ns\ns\ne\nr\nP\n \ny\nt\ni\ns\nr\ne\nv\nn\nU\nd\nr\no\n\n \n\ni\n\nf\nx\nO\n\n \n.\n\n4\n1\n0\n2\n©\n\n \n\n \nt\n\nh\ng\ni\nr\ny\np\no\nC\n?',' ')
    text = text.replace('Swanson, Larry. <i>Neuroanatomical Terminology : A Lexicon of Classical Origins and Historical Foundations</i>, Oxford University Press, Incorporated, 2014. ProQuest Ebook\n         Central, http://ebookcentral.proquest.com/lib/iub-ebooks/detail.action?docID=1963809.\nCreated from iub-ebooks on 2019-07-15 12:06:19.\n\n\x0c',' ')
    #text = text.replace('(*, *), see ',' ')
    
    
    #text = " ".join(text.split())

    fp.close()
    device.close()
    retstr.close()
    return text



convert_pdf_to_txt('/N/u/dnbulloc/Carbonate/PDFs/Page 2 SwansonAnatomyGlossary.pdf')

testString='   DELETENUMS845ENDLINEaccessory internal crural nerve (Schmidt, 1794), see \naccessory obturator nerve (Schmidt,\xa01794)ENDLINEaccessory internal cutaneous nerve of arm (Cruveilhier, ENDLINE1826), see medial cutaneous nerve of arm (>1840)ENDLINEaccessory nerve (Vieussens,\xa01684)\naccessory nerve of internal crural nerve (Schmidt, 1794), see ENDLINEaccessory obturator nerve (Schmidt,\xa01794)ENDLINEaccessory nerve of obturator nerve (Cloquet, 1828), see ENDLINEaccessory obturator nerve (Schmidt,\xa01794)\naccessory nerve of wandring pair (Willis, 1664), see ENDLINEaccessory nerve (Vieussens,\xa01684)ENDLINEaccessory nerve of Weber (Bischoff, 1832), see accessory ENDLINEnerve (Vieussens,\xa01684)ENDLINEacromial nerve (Quain, 1832), see lateral supraclavicular ENDLINEnerves (>1840)ENDLINEacromial nerves (Bang, 1770), see intermediate ENDLINEsupraclavicular nerves (>1840)ENDLINEacromial supraclavicular branch (Peipers, 1793), see lateral ENDLINEsupraclavicular nerves (>1840)ENDLINEacromian branch of thoracic part of trachelo-cutanean ENDLINEplexus (Burdin, 1803), see intermediate \nsupraclavicular nerves (>1840)ENDLINEadcessory pair of cerebral nerves (Soemmerring, 1798), see ENDLINEaccessory nerve (Vieussens,\xa01684)ENDLINEadductor longus femoris nerve (Jördens, 1788), see common ENDLINEfibular nerve (>1840)ENDLINEaccessory nerve of Willis (Vieussens 1684), see spinal ENDLINEaccessory nerve (Willis,\xa01664)ENDLINEaccessory nerve to vagal pair (Frotscher, 1788), see accessory ENDLINEaden colatorius (Hall, 1565), see pituitary gland (>1840)\nadenohypophysis (Rioch et\xa0al.,\xa01940)\nadhesio interthalamica (>1840), see interthalamic adhesion ENDLINEnerve (Vieussens,\xa01684)ENDLINE(>1840)ENDLINEaccessory nerve trunk (Frotscher, 1788), see spinal root of ENDLINEaditus ad aquaeductum (Bartholin, 1654), see opening of ENDLINEaccessory sympathetic nerve trunk (Walter, 1783), see lesser ENDLINEagranular retrolimbic area (Brodmann, 1909), see agranular ENDLINEaccessory nerve trunk (>1840)ENDLINEaccessory nerve trunk (Wrisberg,\xa01786)\naccessory nerves to eighth pair of Lobstein (Frotscher, 1788), ENDLINEsee accessory nerve (Vieussens,\xa01684)\naccessory obturator nerve (Schmidt,\xa01794)\naccessory olfactory bulb (>1840)\naccessory phrenic nerve (>1840)\naccessory roots from medulla oblongata (Scarpa, 1788), see ENDLINEcranial root of accessory nerve rootlets (>1840)ENDLINEaccessory splanchnic nerve (Walter, 1783), see lesser ENDLINEsplanchnic nerve (Haller,\xa01762)ENDLINEaccessory splanchnic nerve roots (Walter, 1783), see lesser ENDLINEsplanchnic nerve (Haller,\xa01762)ENDLINEaccessory splanchnic nerve trunk (Walter, 1783), see lesser ENDLINEsplanchnic nerve (Haller,\xa01762)ENDLINEaccessory sympathetic nerve (Walter, 1783), see lesser ENDLINEsplanchnic nerve (Haller,\xa01762)ENDLINEsplanchnic nerve (Haller,\xa01762)ENDLINEaccumbens nucleus (Ziehen, 1897–1901)\nacervulo cerebri (Soemmerring & Lisignolo, 1785), see brain ENDLINEsand (Soemmerring & Lisignolo,\xa01785)ENDLINE(Soemmerring & Lisignolo,\xa01785)ENDLINEacervulus of pineal gland (Bock, 1824), see brain sand ENDLINE(Soemmerring & Lisignolo,\xa01785)ENDLINEacoustic nerve (Galen, c173), see vestibulocochlear nerve ENDLINE(>1840)ENDLINEnerves (>1840)ENDLINEacoustic nerve trunk (Scarpa, 1789), see vestibulocochlear ENDLINEnerve trunk (>1840)ENDLINEacromial branch of descending superficial branches \nof cervical plexus (Quain, 1828), see lateral \nsupraclavicular nerves (>1840)ENDLINEacromial branch of descending superficial branches \nof cervical plexus (Quain, 1834), see lateral \nsupraclavicular nerves (>1840)ENDLINEacromial branch of thoracic part of tracheosubcutaneous ENDLINEnerves (Chaussier, 1809), see intermediate \nsupraclavicular nerves (>1840)ENDLINEcerebral aqueduct (>1840)ENDLINEaditus ad aquaeductum Sylvii (Haase, 1781), see opening of ENDLINEcerebral aqueduct (>1840)ENDLINEaditus ad infundibulum (Bock, 1824), see ventricles ENDLINEaditus ad infundibulum (Haase, 1781), see interventricular ENDLINE(Hippocrates)ENDLINEforamen (>1840)ENDLINEaditus ad ventriculum tertium (Haase, 1781), see ENDLINEinterventricular foramen (>1840)ENDLINEadrenal plexus (>1840)\nafterbrain (Baer,\xa01837)\nafter-brain (Crooke, 1615), see cerebellum (Aristotle)\nafterbrain vesicle (Baer,\xa01837)\nagger lunatus (Meckel, 1817), see trigeminal ganglion ENDLINEagranular frontal area (Brodmann, 1909), see frontal region ENDLINE(>1840)ENDLINE(Vicq d’Azyr,\xa01786)ENDLINEretrosplenial area (>1840)ENDLINEagranular retrosplenial area (>1840)\nais (Smith Papyrus, c1700 BC), see brain (Smith Papyrus, ENDLINEc1700\xa0BC)ENDLINE(Vesalius,\xa01543a)ENDLINE(Burdach,\xa01822)ENDLINEala cinerea (Arnold, 1838b), see vagal triangle (>1840)\nala lobulus centralis (Reil, 1807–1808a), see central lobule ENDLINEalae of inferior vermiform process (Gordon, 1815), see caudal ENDLINEalar plate (>1840)\nalbicantes prominentiae duae pone infundibulum ENDLINE(Vieussens, 1684), see mammillary body \n(Ludwig,\xa01779)ENDLINEalmond-like lobe (Reil, 1807–1808a), see tonsil ENDLINE(Malacarne,\xa01776)ENDLINEalveolar branch of inferior maxillary nerve (Jacobson, 1818), ENDLINEsee inferior dental nerve (Meckel,\xa01817)ENDLINEalveolar branch of second branch of fifth pair (Haase, 1781), ENDLINEsee posterior superior dental nerve (Haller,\xa01762)ENDLINEalveolar branch of superior maxillary nerve (Cuvier, 1800), ENDLINEsee posterior superior dental nerve (Haller,\xa01762)ENDLINEacervulus (Soemmerring & Lisignolo, 1785), see brain sand ENDLINEajaz (Avicenna or Ibn Sina, c1030), see fornix ENDLINEacoustic nerve (Straus Durckheim, 1828), see invertebrate ENDLINEmedullary velum (>1840)ENDLINE.ENDLINEd\ne\nv\nr\ne\ns\ne\nr\n \ns\ntENDLINEh\ng\ni\nr\n \nl\nlENDLINEAENDLINE \n.ENDLINEd\neENDLINEtENDLINEa\nr\no\np\nr\no\nc\nnENDLINEI\n \n,\ns\ns\ne\nr\nP\n \ny\nt\ni\ns\nr\ne\nv\nn\nU\nd\nr\noENDLINE ENDLINEiENDLINEf\nx\nOENDLINE \n.ENDLINE4\n1\n0\n2\n©ENDLINE ENDLINE \ntENDLINEh\ng\ni\nr\ny\np\no\nCENDLINESwanson, Larry. <i>Neuroanatomical Terminology : A Lexicon of Classical Origins and Historical Foundations</i>, Oxford University Press, Incorporated, 2014. ProQuest Ebook\n         Central, http://ebookcentral.proquest.com/lib/iub-ebooks/detail.action?docID=1963809.\nCreated from iub-ebooks on 2019-07-15 12:06:19.ENDLINE\x0c'
lpars=testString.finditer('(')
