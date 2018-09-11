
import os 

from Tkinter import*
from InterpenetrationPages import * 
from TobeTopLevel2Class import * 

class InterpenetrationPiecePage:

    def __init__(self,parent):
        self.parent = parent
        self.name = "InterpenetrationPage"
        self.currentproject = {}
        self.idnumber = 0
        self.pagelist =\
          {"T-Junction Piece":TJunctionPage,\
             "Interpenetration of Cylindrical Pipes At Any Angle":CylindricalPipeAtAnyAnglePage,\
             "Square pipe Interpenetrating A Cylindrical pipe Vertically":SquareToCylinderPage,\
             "Y-Junction Piece":YJunctionPiecePage,\
             "Right Cylinder Cut Obliquely":CylinderCutAtAnyPage,\
              "Elbow Piece":ElbowPiecePage,"Offset Piece":OffsetPiecePage}

        base_dir = os.path.join("SubFiles2","interpenetrationpieces")

        imagenames = [os.path.join(base_dir,"t_junction.gif"),\
                      os.path.join(base_dir,"cylindrical_any.gif"),\
                      os.path.join(base_dir,"square_cylinder.gif"),\
                      os.path.join(base_dir,"y_junction.gif"),\
                      os.path.join(base_dir,"offset.gif"),\
                      os.path.join(base_dir,"elbow.gif"),\
                      os.path.join(base_dir,"cylinder_oblique.gif")]

        self.imageobj = {}
        self.optionnames = [\
                            "T-Junction Piece",\
                            "Interpenetration of Cylindrical Pipes At Any Angle",\
                            "Square pipe Interpenetrating A Cylindrical pipe Vertically",\
                            "Y-Junction Piece","Offset Piece",
                            "Elbow Piece",\
                            "Right Cylinder Cut Obliquely"]


        for i in range(len(imagenames)):
            self.imageobj[self.optionnames[i]] = PhotoImage(file = imagenames[i])



    def InitializeCount(self):
        self.parent.InitializeCount2()
        self.currentproject = {}



    def CreateWindow(self):
        self.master = TobeTopLevel2(self.parent,self,funcid = self.AnyProject)
        self.master.geometry("990x400+100+150")
        self.master.title("Interpenetration Piece")
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)

        self.frame = Frame(self.master)
        self.frame.grid(sticky = W+E+N+S, row = 0, column = 0)
        self.frame.columnconfigure(0,weight = 1)
        self.frame.rowconfigure(0,weight = 1)


        try:
            self.grndimage = PhotoImage(file = os.path.join("SubFiles2","transition_home.gif"))
            raise IOError
        except Exception:
            self.frame1 = Frame(self.frame)
        else:
            self.frame1 = Label(self.frame, image = self.grndimage)

        self.frame1.grid(sticky = W+E+N+S, row = 0,column = 0)#,padx = 20,pady = 10)
        self.frame1.rowconfigure(0,weight = 1)
        self.frame1.rowconfigure(2,weight = 1)
        self.frame1.columnconfigure(0,weight = 1)

              
        self.toplevellist = []
        




        self.scrolloption = Pmw.ScrolledListBox(self.frame1, items = self.optionnames,\
                                                selectioncommand = self.SwitchImage,\
                                                dblclickcommand =  self.StartOption,\
                                                listbox_font = "Arial 15",\
                                                listbox_height = 10,\
                                                labelpos = "nw",\
                                                label_text = "Interpenetration",\
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
        if classname == "Interpenetration Piece":
            category = fileobj['category']
            self.idnumber +=1
            self.StartInterpenetration()
            b = self.pagelist[category](self)
            b.CreateWindow(self.master)
            
            b.ReceiveDataToOpen(fileobj)  
            b.SetIdnumber(self.idnumber)
            self.currentproject[str(self.idnumber)] = b
        else:
            self.parent.OpenOption(classname,fileobj)
            self.parent.Lower0()


    def Lift(self):
        self.master.Lift()
    def Lower(self):
        self.master.lower()



    def StartInterpenetration(self):
        self.parent.StartInterpenetration()

    def GoBehind(self):
        self.master.lower()
        
 

    def CloseOption(self,idnumber,event = None):
        del(self.currentproject[str(idnumber)])        

        

    def AnyProject(self):
        if self.currentproject:
            return True
        else:
            return False

