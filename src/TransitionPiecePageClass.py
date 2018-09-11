import os 

from Tkinter import*
from TransitionPages import*
from TobeTopLevel2Class import * 

import Pmw 
Pmw.initialise()

class TransitionPiecePage:
    def __init__(self,parent):
        self.parent = parent
        self.name = "TransitionPage"
        self.currentproject = {}
        self.idnumber = 0
        self.pagelist = {"Rectangular to Round Transition Piece":RectToRoundPage,\
                         "Rectangular to Round One Way offset Transition Piece":RectToRoundOff1Page,\
                         "Rectangular to Round Two Way offset Transition Piece":RectToRoundOff2Page,\
                         "Rectangular to Round Oblique Plane":RectToRoundObliquePage,\
                         "Conical Frustum":ConicalFrustumPage}
                          
        self.toplevellist = []
        
        

        base_dir = os.path.join("SubFiles2","transitionpieces")
        imagenames = [os.path.join(base_dir,"rect_round.gif"),\
                      os.path.join(base_dir,"oneway_offset.gif"),\
                      os.path.join(base_dir,"twoway_offset.gif"),\
                      os.path.join(base_dir,"oblique_plane.gif"),\
                      os.path.join(base_dir,"conical_frustum.gif")]

        self.imageobj = {}
        self.optionnames = ["Rectangular to Round Transition Piece",\
                            "Rectangular to Round One Way offset Transition Piece",\
                            "Rectangular to Round Two Way offset Transition Piece",\
                            "Rectangular to Round Oblique Plane",\
                            "Conical Frustum"]
        
        for i in range(len(imagenames)):
            self.imageobj[self.optionnames[i]] = PhotoImage(file = imagenames[i])


    def InitializeCount(self):
        self.parent.InitializeCount1()
        self.currentproject = {}



    def CreateWindow(self):
        self.master = TobeTopLevel2(self.parent,self,funcid = self.AnyProject)
        self.master.geometry("990x400+100+150")
        self.master.title("Transition Piece")
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)


        self.frame = Frame(self.master)
        self.frame.grid(sticky = W+E+N+S, row = 0, column = 0)
        self.frame.columnconfigure(0,weight = 1)
        self.frame.rowconfigure(0,weight = 1)

            
        
        try:
            self.grndimage = PhotoImage(file = os.path.join(os.getcwd(),"transition_home.gif"))
            raise IOError
        except Exception:
            self.frame1 = Frame(self.frame)
        else:
            self.frame1 = Label(self.frame, image = self.grndimage)
        

        
        
        self.frame1.grid(sticky = W+E+N+S, row = 0,column = 0)#,padx = 20,pady = 10)
        self.frame1.rowconfigure(0,weight = 1)
        self.frame1.rowconfigure(2,weight = 1)
        self.frame1.columnconfigure(0,weight = 1)




        self.scrolloption = Pmw.ScrolledListBox(self.frame1, items = self.optionnames,\
                                                selectioncommand = self.SwitchImage,\
                                                dblclickcommand =  self.StartOption,\
                                                listbox_font = "Arial 15",\
                                                listbox_height = 10,\
                                                labelpos = "nw",\
                                                label_text = "Transition Pieces",\
                                                label_font = "Arial 15 bold")
        self.scrolloption.component('listbox').bind("<KeyPress-Return>",self.StartOption)
        self.scrolloption.grid(sticky = W+E, row = 1, column = 0,padx = 20)
        self.displayimage = Label(self.frame1,image = self.imageobj[self.optionnames[0]])
        self.displayimage.grid(sticky = W+E+N+S, row = 1, column = 1,padx = 20)

    def SwitchImage(self):
        chosenoption = self.scrolloption.getcurselection()
        if chosenoption:
            
            choice = chosenoption[0]
            self.displayimage.config(image = self.imageobj[choice])
             

    def StartOption(self,event = None):
        chosenoption = self.scrolloption.getcurselection()
        if chosenoption:
            self.idnumber += 1
            choice = chosenoption[0]
            b = self.pagelist[choice](self)
            
            b.CreateWindow(self.master)
            b.SetIdnumber(self.idnumber)
            self.currentproject[str(self.idnumber)] = b


    def ReceiveDataToOpen(self,fileobj):
        
        classname = fileobj['classname']
        if classname == "Transition Piece":
            category = fileobj['category']
            self.idnumber +=1
            self.StartTransitionPiece()
            b = self.pagelist[category](self)
            b.CreateWindow(self.master)
            b.ReceiveDataToOpen(fileobj)  
            b.SetIdnumber(self.idnumber)
            self.currentproject[str(self.idnumber)] = b
        else:
            self.parent.OpenOption(classname,fileobj)
            self.parent.Lower1()

    def Lift(self):
        self.master.Lift()

    def Lower(self):
        self.master.lower()

    def StartTransitionPiece(self):
        self.parent.StartTransitionPiece()
        
 

    def CloseOption(self,idnumber,event = None):
        del(self.currentproject[str(idnumber)])        

        

    def AnyProject(self):
        if self.currentproject:
            return True
        else:
            return False
