from reportlab.platypus import Paragraph,Frame,\
     SimpleDocTemplate
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle





inputdicttobe = {'Angle of Intersection for pipe B1': 45.0,\
 'Angle of Intersection for pipe B2': 60.0,\
 'Junction Piece Diameter': 300.0, \
 'Partition Number': 24, \
 'Free Height of pipe B2': 100.0,\
 'Free Height of pipe A': 100.0,\
 'Free Height of pipe B1': 100.0}

b =\
"""
Angle of Intersection for pipe B1 = 45.0

Angle of Intersection for pipe B2 = 60.0

Junction Piece Diameter = 300.0\n
 
Partition Number = 12
 
Free Height of pipe B2 = 100.0
 
Free Height of pipe A = 100.0
 
Free Height of pipe B1 = 100.0

"""
c = """
N   Hn-B1     Hn-B2     Ln-A      Ln-B1     Ln-B2     Mn        Hn-A      
0   0.0       0.0       100.0     100.0     100.0     0         0.0       
1   20.096    11.603    108.324   120.096   111.603   78.54     8.324     
2   75.0      43.301    131.066   175.0     143.301   78.54     31.066    
3   150.0     86.603    162.132   250.0     186.603   78.54     62.132    
4   118.934   43.301    131.066   218.934   143.301   78.54     31.066    
5   96.192    11.603    108.324   196.192   111.603   78.54     8.324     
6   87.868    0.0       100.0     187.868   100.0     78.54     0.0       
7   96.192    11.603    108.324   196.192   111.603   78.54     8.324     
8   118.934   43.301    131.066   218.934   143.301   78.54     31.066    
9   150.0     86.603    162.132   250.0     186.603   78.54     62.132    
10  75.0      43.301    131.066   175.0     143.301   78.54     31.066    
11  20.096    11.603    108.324   120.096   111.603   78.54     8.324     
12  0.0       0.0       100.0     100.0     100.0     78.54     0.0       
**************************************************************************

"""
##
##expdf = canvas.Canvas("mypdffile.pdf",bottomup = 0)
##textobj = expdf.beginText(2*inch, 2*inch)
##textobj.textLines(b)
##textobj.textLine(c)
##expdf.drawText(textobj)
##expdf.save()



styles = getSampleStyleSheet()
styles2 = ParagraphStyle("1")
styles2.spaceBefore = 0.25*inch
styles2.spaceAfter = 0.25*inch
styles2.fontName = 'Times-Roman'
styles2.fontSize = 12
styleN  = styles['Normal']
story = []
text = ''
for item in inputdicttobe:
    text = item + " = " +str(inputdicttobe[item])+"\n\n"
    story.append(Paragraph(text,styles2))
doc = SimpleDocTemplate('mydoc2.pdf')
doc.build(story)

##










##class PublishPdfClass:
##    def __init__(self,parent,ftype = 0,size = (700,300)):
##        self.parent = parent
##
##
##    def ClearPrevious(self):
##        if len(self.indexlist) > 2:
##            self.EnableScreen()
##            self.scrolledtext.delete(self.indexlist[-2],self.indexlist[-1])
##            del(self.indexlist[-1])
##            self.indexpos -=1
##            self.DisableScreen()
##        elif len(self.indexlist) == 2:
##            del(self.indexlist[-1])
##            self.ClearScreen()
##        self.HasEdited()
##    def Overwrite(self):
##        pass
##    def HasEdited(self,event = None):
##        self.parent.HasEdited()
##
##    def DisableScreen(self):
##        self.scrolledtext.configure(text_state = 'disabled')
##
##    def DisableAll(self):
##        self.DisableScreen()
##        self.scrolledtext.configure(Header_state = 'disabled')
##
##    def EnableScreen(self):
##        self.scrolledtext.configure(text_state = 'normal')
##
##    def EnableAll(self):
##        self.EnableScreen()
##        self.scrolledtext.configure(Header_state  = 'normal')
##
##
##
##    def Insert(self,value = " "):
##
##        self.scrolledtext.insert('end',value+"\n")
##        self.indexcounter +=1
##
##
##    def InsertColumn0(self,value = " "):
##
##        self.scrolledtext.component('rowheader').insert(\
##            'end',value +"\n")
##
##
##
##    def InsertData(self,dimensiondict,valuedict,othersdict = None):
##        if self.overwrite_variable.get():
##            self.ClearScreen()
##        self.indexpos += 1
##        self.indexcounter = self.indexlist[self.indexpos]
##
##        self.EnableScreen()
##        self.count +=1
##        self.rowmax = 0
##        self.rowmax4 = 0
##        if dimensiondict:
##            self.InsertValue(dimensiondict,0)
##        if othersdict:
##            self.InsertValue(othersdict,0)
##        
##        if valuedict:
##            self.columnheader = valuedict.keys()
##            self.columnheader.sort()
##            index = self.columnheader.index("N")
##            if index != 0:              
##                self.columnheader[0],self.columnheader[index] = self.columnheader[index],self.columnheader[0]
##            
##            
##            
##
##            formatstring  = "%-8s  "
##            formatstring2 = "%-2s  "
##            
##            row = ""
##            row += formatstring2%self.columnheader[0]
##            for i in range(len(self.columnheader)-1):
##                row += formatstring%self.columnheader[i+1]
##
##                    
##            self.Insert(row)
##            
##            row2 = ""
##            for i in range(len(valuedict["N"])):
##                for item in self.columnheader:
##                    if item == "N":
##                        row2 += formatstring2%valuedict[item][i]
##                    else:
##                        
##                        row2 += formatstring%valuedict[item][i]               
##                self.Insert(row2)
##                self.RowMax(len(row2))
##                row2 = ""
##
##        if self.rowmax:
##            self.MarkEnd1()
##        else:
##            self.MarkEnd4(self.rowmax4)
##        self.indexlist.append(Decimal(self.indexcounter,1))
##            
##        self.DisableScreen()
##        
##
##    def InsertValue(self,othersdict,mark = 1):
##        
##        if mark:
##            self.indexpos += 1
##            self.indexcounter = self.indexlist[self.indexpos]
##            if self.overwrite_variable.get():
##                self.ClearScreen()
##
##        self.EnableScreen()
##        if othersdict:
##            self.Insert()
##            for item in othersdict:
##                b = item + " = " +str(othersdict[item])
##                if len(b) > self.rowmax4:
##                    self.rowmax4 = len(b)
##                self.Insert(b)
##                self.Insert()
##
##        if mark:
##            self.MarkEnd1()
##            self.indexlist.append(Decimal(self.indexcounter,1))
##            self.DisableScreen()
##            
##
##    def MarkEnd1(self):
##        self.Insert("*"*self.rowmax)
##
##    def MarkEnd4(self,n):
##        self.Insert("*"*n)
##
##    def MarkEnd2(self):
##        self.InsertColumn0("***")
##
##    def RowMax(self,n):
##        if n> self.rowmax:
##            self.rowmax = n
##
##    def GetDataToSave(self):
##        btext = self.scrolledtext.get(0.0,END)
##        indexlist = self.indexlist
##        return [str(btext),indexlist] 
##
##    def ReceiveDataToOpen(self,alist):
##        self.EnableScreen()
##        indexlist = alist[1]
##        texts = alist[0]
##        print texts
##        BTEXTVALUE = texts
##        
##        self.indexlist = indexlist[:]
##        self.indexpos = len(self.indexlist) - 2
##        self.indexcounter = self.indexlist[self.indexpos]
##        texts = texts.rstrip()
##        self.Insert(texts)
##        self.Insert()
##        self.indexcounter -= 1
####        self.indexlist[self.indexpos] = Decimal(self.indexcounter,1)
##        
##        
##        self.DisableScreen()
