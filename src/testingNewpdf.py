import re
from reportlab.platypus import Paragraph,Frame,\
     SimpleDocTemplate,Table,TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,\
     ParagraphStyle



resultdict = \
{'Ln-B1': [100.0, 105.111, 120.096, 143.934, 175.0, 211.17700000000002, 250.0, 233.919, 218.934, 206.066, 196.192, 189.985, 187.868, 189.985, 196.192, 206.066, 218.934, 233.919, 250.0, 211.17700000000002, 175.0, 143.934, 120.096, 105.111, 100.0], 'Ln-B2': [100.0, 102.951, 111.603, 125.365, 143.301, 164.188, 186.603, 164.188, 143.301, 125.365, 111.603, 102.951, 100.0, 102.951, 111.603, 125.365, 143.301, 164.188, 186.603, 164.188, 143.301, 125.365, 111.603, 102.951, 100.0], 'Hn-A': [0.0, 2.117, 8.324, 18.198, 31.066, 46.051, 62.132, 46.051, 31.066, 18.198, 8.324, 2.117, 0.0, 2.117, 8.324, 18.198, 31.066, 46.051, 62.132, 46.051, 31.066, 18.198, 8.324, 2.117, 0.0], 'Mn': [0, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27, 39.27], 'N': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], 'Hn-B1': [0.0, 5.111, 20.096, 43.934, 75.0, 111.177, 150.0, 133.919, 118.934, 106.066, 96.192, 89.985, 87.868, 89.985, 96.192, 106.066, 118.934, 133.919, 150.0, 111.177, 75.0, 43.934, 20.096, 5.111, 0.0], 'Hn-B2': [0.0, 2.951, 11.603, 25.365, 43.301, 64.188, 86.603, 64.188, 43.301, 25.365, 11.603, 2.951, 0.0, 2.951, 11.603, 25.365, 43.301, 64.188, 86.603, 64.188, 43.301, 25.365, 11.603, 2.951, 0.0], 'Ln-A': [100.0, 102.117, 108.324, 118.19800000000001, 131.066, 146.051, 162.132, 146.051, 131.066, 118.19800000000001, 108.324, 102.117, 100.0, 102.117, 108.324, 118.19800000000001, 131.066, 146.051, 162.132, 146.051, 131.066, 118.19800000000001, 108.324, 102.117, 100.0]}

inputdicttobe = {'Angle of Intersection for pipe B1': 45.0,\
 'Angle of Intersection for pipe B2': 60.0,\
 'Junction Piece Diameter': 300.0, \
 'Partition Number': 24, \
 'Free Height of pipe B2': 100.0,\
 'Free Height of pipe A': 100.0,\
 'Free Height of pipe B1': 100.0}


hlist = \
"""
Angle of Intersection for pipe B1 = 45.0
 
Angle of Intersection for pipe B2 = 60.0
 
Junction Piece Diameter = 300.0
 
Partition Number = 24
 
Free Height of pipe B2 = 100.0
 
Free Height of pipe A = 100.0
 
Free Height of pipe B1 = 100.0
 
N   Hn-B1     Hn-B2     Ln-A      Ln-B1     Ln-B2     Mn        Hn-A      
0   0.0       0.0       100.0     100.0     100.0     0         0.0       
1   5.111     2.951     102.117   105.111   102.951   39.27     2.117     
2   20.096    11.603    108.324   120.096   111.603   39.27     8.324     
3   43.934    25.365    118.198   143.934   125.365   39.27     18.198    
4   75.0      43.301    131.066   175.0     143.301   39.27     31.066    
5   111.177   64.188    146.051   211.177   164.188   39.27     46.051    
6   150.0     86.603    162.132   250.0     186.603   39.27     62.132    
7   133.919   64.188    146.051   233.919   164.188   39.27     46.051    
8   118.934   43.301    131.066   218.934   143.301   39.27     31.066    
9   106.066   25.365    118.198   206.066   125.365   39.27     18.198    
10  96.192    11.603    108.324   196.192   111.603   39.27     8.324     
11  89.985    2.951     102.117   189.985   102.951   39.27     2.117     
12  87.868    0.0       100.0     187.868   100.0     39.27     0.0       
13  89.985    2.951     102.117   189.985   102.951   39.27     2.117     
14  96.192    11.603    108.324   196.192   111.603   39.27     8.324     
15  106.066   25.365    118.198   206.066   125.365   39.27     18.198    
16  118.934   43.301    131.066   218.934   143.301   39.27     31.066    
17  133.919   64.188    146.051   233.919   164.188   39.27     46.051    
18  150.0     86.603    162.132   250.0     186.603   39.27     62.132    
19  111.177   64.188    146.051   211.177   164.188   39.27     46.051    
20  75.0      43.301    131.066   175.0     143.301   39.27     31.066    
21  43.934    25.365    118.198   143.934   125.365   39.27     18.198    
22  20.096    11.603    108.324   120.096   111.603   39.27     8.324     
23  5.111     2.951     102.117   105.111   102.951   39.27     2.117     
24  0.0       0.0       100.0     100.0     100.0     39.27     0.0       
**************************************************************************
"""

##
##expdf = canvas.Canvas("mypdffile.pdf",bottomup = 0)
##textobj = expdf.beginText(2*inch, 2*inch)
##textobj.textLines(b)
##textobj.textLine(c)
##expdf.drawText(textobj)
##expdf.save()



##styles = getSampleStyleSheet()
##styles2 = ParagraphStyle("1")
##styles2.spaceBefore = 0.25*inch
##styles2.spaceAfter = 0.25*inch
##styles2.fontName = 'Times-Roman'
##styles2.fontSize = 12
##styleN  = styles['Normal']
##story = []

# first determine the length of the dimension and other dict:



number = len(inputdicttobe)
inputdicttobe2 = inputdicttobe.keys()
inputdicttobe2.sort()
story = []
datalist1 = []
count = 0
blist = []
for item in inputdicttobe2:
    blist.append(item + " = " +str(inputdicttobe[item]))
    count +=1
    if count == 2:
        datalist1.append(blist)
        blist = []
        count = 0
if number%2 != 0:
    blist.append(" ")
    datalist1.append(blist)

tableobj1 = Table(datalist1)
tableobj1.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Times-Roman',14),\
                             ('ALIGN',(0,0),(0,-1),'LEFT'),\
                              ('BOTTOMPADDING',(0,0),(-1,-1),5),\
                              ('TOPPADDING',(0,0),(-1,-1),5),\
                              ('TEXTCOLOR',(0,0),(-1,-1),colors.blue)]))

datalist2 = []
columnheader = resultdict.keys()
columnheader.sort()
index = columnheader.index("N")
if index != 0:              
    columnheader[0],columnheader[index] =\
                columnheader[index],columnheader[0]
datalist2.append(columnheader)
for i in range(len(resultdict["N"])):
    blist = []
    for item in columnheader:
       blist.append(resultdict[item][i])
    datalist2.append(blist)


tableobj2 = Table(datalist2)
tableobj2.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Times-Roman',14),\
                             ('ALIGN',(0,0),(0,-1),'LEFT'),\
                              ('BOTTOMPADDING',(0,0),(-1,-1),5),\
                              ('TOPPADDING',(0,0),(-1,-1),5),\
                              ('TEXTCOLOR',(0,0),(-1,-1),colors.blue)]))
    
story.append(tableobj1)
story.append(tableobj2)






##for item in inputdicttobe:
##    text.append(item + " = " +str(inputdicttobe[item])+"\n\n"
##    story.append(Paragraph(text,styles2))
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
