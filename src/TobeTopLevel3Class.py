from Tkinter import * 
from DialogsGui import * 
import re 
import os 
import shelve 

class TobeTopLevel3(Toplevel): # for graph window
    def __init__(self,root,parent,funcid = None,name = "project",askoption = 0,windowtype = 0):
        self.parent = parent
        self.name = name
        self.filepath = None
        self.savefilecount = 0
        self.savefileafteredit = 1

        
        self.exp = re.compile(r"[\/]?")
        self.askoption =  askoption
##        self.savedialog = SaveDialog()
##        self.opendialog = OpenDialog()
##        self.errordialog = WarningDialog()
        self.funcid = funcid
        Toplevel.__init__(self,root)
        self.protocol("WM_DELETE_WINDOW",self.CloseTopLevel)
        self.bind("<Control-p>",self.SaveFile)
        self.bind("<MouseWheel>",self.ZoomFigure)
        try:
            self.wm_iconbitmap(os.path.join('SubFiles2','Icon.ico'))
        except TclError:
            pass


        self.CreateMenuBar2()
        self.focus()

   
    def CloseTopLevel(self):
        if self.askoption:
            answer = askyesnocancel("Quit","Do you want to Quit\n%s"%self.name)
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

    def HasEdited(self,event = None):
        pass


    def CreateMenuBar2(self):
        self.menuobj = Menu(self)
        self.config(menu = self.menuobj)

        self.filemenu = Menu(self.menuobj)
        self.menuobj.add_cascade(label = "File",menu = self.filemenu)
        self.filemenu.add_command(label = "Print to pdf",command=self.OpenFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit",command = self.CloseTopLevel)
        self.editmenu = Menu(self.menuobj)
        self.menuobj.add_cascade(label = "Edit",menu = self.editmenu)
        self.editmenu.add_command(label = "Zoom Normal (initial view)",command = self.ZoomNormal)

        self.helpmenu = Menu(self.menuobj)
        self.menuobj.add_cascade(label = "Help",menu = self.helpmenu)
        self.helpmenu.add_command(label = "About Us",command = self.AboutUs)

    def SetZoomObject(self,zoom):
        self.zoomobj = zoom

    def ZoomNormal(self):
        self.linkerobj.SetNormal()

    def ZoomFigure(self,event):
        self.zoomobj.ZoomWheel(event.delta)

    def SetLinkerObject(self,linker):
        self.linkerobj = linker

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

    def SaveFile(self,event = None):
        if self.savefilecount == 0:
            self.SaveFileAs()
        else:
            self.GetDataToSave()

    def SetHasEdited(self):
        self.savefileafteredit = 0
        

    def OpenFile(self,event = None):
        pass
##        filepath = self.opendialog.OpenFile()
##        if filepath:
##            self.filepath = filepath
##            self.ReadDataSaved()
##
    def ExtractFileName(self,path):
        filename = re.split(self.exp,path)
        filename2 = filename[-1].strip()
        filename3 = filename2.split(".cd")
        return filename3[-2].strip()

    def OpenFileObj(self):
        try:
            self.fileobj = shelve.open(self.filepath)
        except IOError:
            self.errordialog.ShowErrorMessage("file","Could not Open file")
            return 0
        except Exception:
            self.errordialog.ShowErrorMessage("file","Cannot Open in file")
            return 0
        else:
            return 1

    def CloseFileObj(self):
        if self.fileobj: 
            self.fileobj.close()

    def GetDataToSave(self):
        ans = self.OpenFileObj()
        if ans:
            self.name = self.ExtractFileName(self.filepath)
            self.SetName(self.name)
            self.parent.GetDataToSave(self.fileobj)
            self.fileobj['name'] = self.name
            self.fileobj['format'] = 1
            self.fileobj['filepath'] = self.filepath
            self.CloseFileObj()


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



