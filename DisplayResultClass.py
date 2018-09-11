from Tkinter import *
from MathUtils import * 

import Pmw 
Pmw.initialise()

class DisplayResultClass:
    def __init__(self,parent,row= 0, column = 0,ftype = 0,size = (700,300)):
        self.parent = parent
        self.row =  row
        self.column = column
        self.ftype = ftype
        self.count = 0
        self.size = size
        self.rowmax = 8
        self.indexlist = [0.0]
        self.indexpos = -1
        self.rowmax4 = 0

    def CreateWindow(self,frame):
        
        self.frame = Frame(frame)
        self.frame.rowconfigure(0,weight = 1)
        self.frame.columnconfigure(0,weight = 1)

        self.CreateDisplayScreen2()
        self.CreateButton()
        self.frame.grid(sticky = W+E+N+S,\
                    row = self.row,column = self.column)

    def CreateDisplayScreen2(self):
        fixedFont = Pmw.logicalfont('Fixed')
        self.scrolledtext =\
            Pmw.ScrolledText(self.frame,\
                hscrollmode = "static",\
                             borderframe = 1,\
                
                labelpos = 'n',\
                label_text = "Result",\
                label_font = fixedFont,\

                usehullsize = 1,\
                hull_width = self.size[0],\
                hull_height = self.size[1],\

                text_wrap = 'none',\
                text_font = fixedFont,\
                text_foreground = 'black',\
                text_height = 5,\
                text_width = 5,\


                text_padx = 4,\
                text_pady = 4,\

                             )
        self.DisableScreen()
        

        self.scrolledtext.grid(sticky = W+E+N+S, row = 0,\
                               column = 0)

    def CreateButton(self):
        self.buttonframe = Frame(self.frame)
        self.buttonframe.columnconfigure(0,weight = 1)
        self.buttonframe.columnconfigure(3,weight = 1)
        self.buttonframe.rowconfigure(0,weight = 1)
        self.buttonframe.grid(sticky = W+E, row = 1,column = 0,pady = 10)
        self.clearbutton = Button(self.buttonframe, text = "Clear Result",\
                                  command = self.ClearScreen)
        self.clearbutton.grid(sticky = W+E, row = 0, column = 1)

        self.clearprevious = Button(self.buttonframe,text = "Clear Previous",\
                                    command = self.ClearPrevious)
        self.clearprevious.grid(sticky = W+E, row = 0, column = 2,padx = 4)

        self.overwrite_variable = BooleanVar()
        self.overwrite_button = Checkbutton(self.buttonframe, text = "Overwrite",\
                                            variable = self.overwrite_variable,command = self.Overwrite)
        self.overwrite_button.grid(sticky = W, row = 0,column = 3)

    def ClearPrevious(self):
        if len(self.indexlist) > 2:
            self.EnableScreen()
            self.scrolledtext.delete(self.indexlist[-2],self.indexlist[-1])
            del(self.indexlist[-1])
            self.indexpos -=1
            self.DisableScreen()
        elif len(self.indexlist) == 2:
            del(self.indexlist[-1])
            self.ClearScreen()
        self.HasEdited()
    def Overwrite(self):
        pass
    def HasEdited(self,event = None):
        self.parent.HasEdited()

    def ClearScreen(self):
        if self.ftype:
            self.EnableAll()
            self.scrolledtext.delete(0.0,END)
            self.scrolledtext.component('rowcolumnheader').delete(0.0,END)
            self.scrolledtext.component('columnheader').delete(0.0,END)
            self.scrolledtext.component('rowheader').delete(0.0,END)
            self.count = 0
            self.DisableAll()
            
        else:
            self.EnableScreen()
            self.scrolledtext.delete(0.0,END)
            self.indexlist = [0.0]
            self.indexpos = -1
            self.DisableScreen()
        self.HasEdited()

    def DisableScreen(self):
        self.scrolledtext.configure(text_state = 'disabled')

    def DisableAll(self):
        self.DisableScreen()
        self.scrolledtext.configure(Header_state = 'disabled')

    def EnableScreen(self):
        self.scrolledtext.configure(text_state = 'normal')

    def EnableAll(self):
        self.EnableScreen()
        self.scrolledtext.configure(Header_state  = 'normal')





    def InsertRCHeader(self,value):

        self.scrolledtext.component('rowcolumnheader').insert('end',value)


    def CreateColumnHeader(self,value):
        headerline = ''
        for i in range(len(value)):
            headerline = headerline + '%-7s'%value[i]

            
        self.InsertColumn(headerline)


    def InsertColumn(self,value):

        self.scrolledtext.component('columnheader').insert('0.0',\
                                    value)


    def Insert(self,value = " "):

        self.scrolledtext.insert('end',value+"\n")
        self.indexcounter +=1


    def InsertColumn0(self,value = " "):

        self.scrolledtext.component('rowheader').insert(\
            'end',value +"\n")



    def InsertData(self,dimensiondict,valuedict,othersdict = None):
        """
            Displays the data in tabular format. 

        Note:
            number of deciman places  = 4. 
        """
        if self.overwrite_variable.get():
            self.ClearScreen()
        self.indexpos += 1
        self.indexcounter = self.indexlist[self.indexpos]

        self.EnableScreen()
        self.count +=1
        self.rowmax = 0
        self.rowmax4 = 0
        if dimensiondict:
            self.InsertValue(dimensiondict,0)
        if othersdict:
            self.InsertValue(othersdict,0)
        
        if valuedict:
            self.columnheader = valuedict.keys()
            self.columnheader.sort()
            index = self.columnheader.index("N")
            if index != 0:              
                self.columnheader[0],self.columnheader[index] = self.columnheader[index],self.columnheader[0]
            

            # First, determine the maxlength of string in each column. 
            max_column_lengths = {item:len("%.4f"%max(valuedict[item])) for item in valuedict}

            # construct the format string template for each row. 
            number_format_template = "{:%d}  "
            float_format_template  = "{:%d}  "
            
            # Determine String formatting 
            header_format = "{:^5}  "
            header_row = ""
            print("Colummn header = ",self.columnheader[0])

            header_row += '{:5}  '.format(self.columnheader[0])
            for i in range(len(self.columnheader)-1):
                header_row += header_format.format(self.columnheader[i+1])

                    
            self.Insert(header_row)
            
            row2 = ""
            for i in range(len(valuedict["N"])):
                for item in self.columnheader:
                    nform = number_format_template%max_column_lengths[item]
                    fform = float_format_template%max_column_lengths[item]

                    if item == "N":
                        row2 += nform.format(valuedict[item][i])
                    else:
                        vvalue = '{:.4f}'.format(valuedict[item][i])
                        row2 += fform.format(vvalue)
                self.Insert(row2)
                self.RowMax(len(row2))
                row2 = ""

        if self.rowmax:
            self.MarkEnd1()
        else:
            self.MarkEnd4(self.rowmax4)
        self.indexlist.append(Decimal(self.indexcounter,1))

        if not self.overwrite_variable.get():
            self.scrolledtext.see(self.indexlist[-1])
            
        self.DisableScreen()
        

    def InsertValue(self,othersdict,mark = 1):
        
        if mark:
            self.indexpos += 1
            self.indexcounter = self.indexlist[self.indexpos]
            if self.overwrite_variable.get():
                self.ClearScreen()

        self.EnableScreen()
        if othersdict:
            self.Insert()
            for item in othersdict:
                b = item + " = " +str(othersdict[item])
                if len(b) > self.rowmax4:
                    self.rowmax4 = len(b)
                self.Insert(b)
                self.Insert()

        if mark:
            self.MarkEnd1()
            self.indexlist.append(Decimal(self.indexcounter,1))
            self.scrolledtext.see(self.indexlist[-1])
            self.DisableScreen()
            

    def MarkEnd1(self):
        self.Insert("*"*self.rowmax)

    def MarkEnd4(self,n):
        self.Insert("*"*n)

    def MarkEnd2(self):
        self.InsertColumn0("***")

    def RowMax(self,n):
        if n> self.rowmax:
            self.rowmax = n

    def GetDataToSave(self):
        btext = self.scrolledtext.get(0.0,END)
        indexlist = self.indexlist
        return [str(btext),indexlist] 

    def ReceiveDataToOpen(self,alist):
        self.EnableScreen()
        indexlist = alist[1]
        texts = alist[0]
        
        self.indexlist = indexlist[:]
        self.indexpos = len(self.indexlist) - 2
        self.indexcounter = self.indexlist[self.indexpos]
        texts = texts.rstrip()
        self.Insert(texts)
        self.Insert()
        self.scrolledtext.see(self.indexlist[-1])
        self.indexcounter -= 1
##        self.indexlist[self.indexpos] = Decimal(self.indexcounter,1)
        
        
        self.DisableScreen()


    