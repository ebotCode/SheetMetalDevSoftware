from Tkinter import * 
from DialogsGui import * 
import re 
import os 
import cPickle 

class TobeTopLevel(Toplevel):
    def __init__(self,root,parent,funcid = None,name = "project",\
                 askoption = 1,windowtype = 0,maximize = 0):
        self.parent = parent
        self.name = name
        self.filepath = None
        self.savefilecount = 0
        self.savefileafteredit = 0

        
        self.exp = re.compile(r"[\/]?")
        self.askoption =  askoption
        self.savedialog = SaveDialog(self)
        self.opendialog = OpenDialog(self)
        self.errordialog = WarningDialog(self)
        self.funcid = funcid
        Toplevel.__init__(self,root)
        self.protocol("WM_DELETE_WINDOW",self.CloseTopLevel)

        try:
            self.wm_iconbitmap(os.path.join('SubFiles2','Icon.ico'))
        except TclError:
            pass


        if maximize:
            try:
                self.state(GetZoomedStateOption(sys.platform))
            except Exception:
                pass             
            # self.state("zoomed")
        self.bind("<Control-s>",self.SaveFile)
        self.bind("<Control-o>",self.OpenFile)
        
   
    def CloseTopLevel(self):
        if self.savefileafteredit:
            answer = askyesnocancel("Quit","Save changes made to %s before Quiting?"%self.name,\
                                    parent = self,default = "yes")
            if answer:
                self.SaveFile()
                answer = 1
            elif answer == False:
                answer = 1
            else:
                answer = 0
                
        else:
            answer = 1
        if answer:
            if self.funcid:
                self.funcid()
                self.destroy()
            else:
                self.destroy()

    def CreateMenuBar(self):
        pass


    def CreateMenuBar2(self):
        self.menuobj = Menu(self)
        self.config(menu = self.menuobj)

        self.filemenu = Menu(self.menuobj)
        self.menuobj.add_cascade(label = "File",menu = self.filemenu)
        self.filemenu.add_command(label = "Open",command=self.OpenFile)
        self.filemenu.add_command(label = "Save Project",command = self.SaveFile)
        self.filemenu.add_command(label = "Save Project As",command = self.SaveFileAs)
        self.filemenu.add_command(label = "Print Result to Text file",command = self.CloseDemo)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit",command = self.CloseTopLevel)
        self.helpmenu = Menu(self.menuobj)
        self.menuobj.add_cascade(label = "Help",menu = self.helpmenu)
        self.helpmenu.add_command(label = "About Us",command = self.AboutUs)

    def AboutUs(self):
        pass

    def SetName(self,name):
        self.name = name
        self.title(self.name)
        self.parent.SetName(self.name)

    def SetOpenDetails(self,filepath):
        self.filepath = filepath
        self.savefilecount +=1
        

    def SaveFileAs(self,event = None):
        self.savefilecount +=1
        filepath = self.savedialog.SaveFile()
        if filepath:
            self.filepath = filepath
            self.GetDataToSave()
            self.savefileafteredit = 0
            

    def SaveFile(self,event = None):
        if self.savefilecount == 0:
            self.SaveFileAs()
            
        else:
            self.GetDataToSave()
            self.savefileafteredit = 0

    def SetHasEdited(self):
        self.savefileafteredit = 1
        

    def OpenFile(self,event = None):
        filepath = self.opendialog.OpenFile()
        if filepath:
            self.filepath = filepath
            self.ReadDataSaved()

    def ExtractFileName(self,path):
        filename = re.split(self.exp,path)
        filename2 = filename[-1].strip()
        filename3 = filename2.split(".cd")
        return filename3[-2].strip()

    def OpenFileObj(self):
        try:
            self.fileobj2 = open(self.filepath,"r")
            self.fileobj = cPickle.load(self.fileobj2)
        except EOFError:
            self.errordialog.ShowErrorMessag("file","Cannot Open file")
            try:
                self.fileobj2.close()
            except Exception:
                pass
            return 0
        except IOError:
            self.errordialog.ShowErrorMessage("file","Cannot Open file")
            return 0
        except Exception:
            self.errordialog.ShowErrorMessage("file","Cannot Open file")
            try:
                self.fileobj2.close()
            except Exception:
                pass
            return 0
        else:
            return 1


    def OpenFileObjToSave(self):
        try:
            self.fileobj2 = open(self.filepath,"w")
            self.fileobj = {}
        except EOFError:
            self.errordialog.ShowErrorMessag("file","Cannot Open file")
            try:
                self.fileobj2.close()
            except Exception:
                pass                
            return 0
        except IOError:
            self.errordialog.ShowErrorMessage("file","Cannot Open file")
            try:
                self.fileobj2.close()
            except Exception:
                pass                
            return 0

        except Exception:
            self.errordialog.ShowErrorMessage("file","Cannot Open file\n")
            try:
                self.fileobj2.close()
            except Exception:
                pass                
            return 0
        else:
            return 1


    def CloseFileSaveObj(self):
        try:
            cPickle.dump(self.fileobj,self.fileobj2)
            self.fileobj2.close()
        except Exception:
            self.errordialog.ShowErrorMessage("file","Could not close file")

    def CloseFileObj(self):
        try:
            self.fileobj2.close()
        except Exception:
            self.errordialog.ShowErrorMessage("file","Could not close file")

    def GetDataToSave(self):
        ans = self.OpenFileObjToSave()
        if ans:
            self.name = self.ExtractFileName(self.filepath)
            self.SetName(self.name)
            self.parent.GetDataToSave(self.fileobj)
            self.fileobj['name'] = self.name
            self.fileobj['format'] = 1
            self.fileobj['filepath'] = self.filepath
            self.CloseFileSaveObj()


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
                self.parent.parent.parent.ReceiveDataToOpen(self.fileobj)# parent(inputpage),parent(recttoroundpage),\
                                                                            #parent(transition piecepage)
                self.CloseFileObj()
                
        
        

    def CloseDemo(self):
        pass

    def CloseWindow(self):
        self.parent.CloseWindow()
