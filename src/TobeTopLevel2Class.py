from Tkinter import * 
from DialogsGui import * 
import re 
import os 
import cPickle 

class TobeTopLevel2(Toplevel):
    def __init__(self,root,parent,funcid = None):
        self.parent = parent
        self.funcid = funcid
        self.filepath = None
        self.exp = re.compile(r"[\/]?")

        
        self.opendialog = OpenDialog(self)
        self.errordialog = WarningDialog(self)
        
        Toplevel.__init__(self,root)
        self.protocol("WM_DELETE_WINDOW",self.CloseTopLevel)
##        self.geometry
        self.CreateMenuBar()
        try:
            self.wm_iconbitmap(os.path.join('SubFiles2','Icon.ico'))
        except TclError:
            pass

        self.bind("<Control-o>",self.OpenFile)
        self.focus()


    def Lift(self):
        self.deiconify()
        self.lift()
        self.focus()



    def CloseTopLevel(self):
        self.askoption = self.funcid()
        if self.askoption:
            answer = askyesnocancel("Quit","You have Active Projects.\nDo you want to quit anyway?",\
                                    parent = self,default="yes")
        else:
            answer = 1
        if answer:
            if self.funcid:
                self.funcid()
                self.InitializeTransitionPiece()
                self.destroy()
            else:
                self.InitializeTransitionPiece()
                self.destroy()        
        

    def InitializeTransitionPiece(self):
        self.parent.InitializeCount()


    def CreateMenuBar(self):
        self.menuobj = Menu(self)
        self.config(menu = self.menuobj)

        self.filemenu = Menu(self.menuobj)
        self.menuobj.add_cascade(label = "File",menu = self.filemenu)
        self.filemenu.add_command(label = "Open",command=self.OpenFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit",command = self.CloseTopLevel)
        self.helpmenu = Menu(self.menuobj)
        self.menuobj.add_cascade(label = "Help",menu = self.helpmenu)
        self.helpmenu.add_command(label = "About Us",command = self.AboutUs)

    def AboutUs(self):
        pass


    def OpenFile(self,event = None):
        filepath = self.opendialog.OpenFile()
        if filepath:
            self.filepath = filepath
            self.ReadDataSaved()

    def ReadDataSaved(self):
        ans = self.OpenFileObj()
        if ans:
            try:
                isformat = self.fileobj['format']
            except KeyError:
                self.errordialog.ShowErrorMessage("file","This is not a recognised file")
                self.CloseFileObj()
            except Exception:
                self.errordialog.ShowErrorMessage("file","An Error Occured\nContact Manufacturer")
                self.CloseFileObj()
            else:
                self.parent.ReceiveDataToOpen(self.fileobj)# parent(inputpage),parent(recttoroundpage),\
                                                                            #parent(transition piecepage)
                self.CloseFileObj()



    def OpenFileObj(self):
        try:
            self.fileobj2 = open(self.filepath,"r")
            self.fileobj = cPickle.load(self.fileobj2)
        except EOFError:
            self.errordialog.ShowErrorMessage("file","Cannot Open file")
            try:
                self.fileobj2.close()
            except Exception:
                pass
            return 0
        except IOError:
            self.errordialog.ShowErrorMessage("file","Cannot Open file")
            return 0
        except Exception,msg:
            self.errordialog.ShowErrorMessage("file","Cannot Open file\n")
            try:
                self.fileobj2.close()
            except Exception:
                pass
            return 0
        else:
            return 1


    def CloseFileObj(self):
        try:
            if self.fileobj2:
                self.fileobj2.close()
        except Exception:
            self.errordialog.ShowErrorMessage("file","Could not close file")

