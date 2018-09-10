import os
import sys
import cPickle
import re
from Tkinter import*
from tkMessageBox import*
from tkFileDialog import askopenfilename,asksaveasfilename
import Pmw


Pmw.initialise()

import math

def DegtoRad(x):
    return math.pi* x/ 180
def RadtoDeg(x):
    return x * 180/ math.pi

def Cos(x):
    return math.cos(DegtoRad(x))

def Sin(x):
    return math.sin(DegtoRad(x))


def Cosec(x):
    return (1 / (Sin(x)))
def Cot(x):
    return (Cos(x)/Sin(x))
def Tan(x):
    return (Sin(x)/Cos(x))

def Atan(x):
    return RadtoDeg(math.atan(x))

def Acos(x):
    return RadtoDeg(math.acos(x))
def Asin(x):
    return RadtoDeg(math.asin(x))


def Decimal(x,place= 3):
    astring = "%."
    bstring = "%d"%place
    template = astring + bstring + "f"
    return float(template%x)


def CosineAngle(x,y,z):
    return   Acos(((pow(y,2)) + (pow(z,2)) - (pow(x,2)))/(2*y*z))


def GetZoomedStateOption(platform_type):
    if 'linux' in platform_type:
        return 'normal'
    else: # windows. 

        return 'zoomed'    
    
########################################################################
########################################################################


class ChartScale:
    def __init__(self,linkerobject):
        self.pto_mm = 0.26484375
        self.linkerobject = linkerobject
        self.linkerobject.Add(self, "ChartScale")
        self.k = 1
        self.initial = [2,2,30,30]
        self.sx = 5  # 2pixel to 10mm unit
        self.sxu = 10 # unit mm
        self.sy = 5  # 2 pixel to 10mm unit
        self.syu = 10 # unit mm
        self.xoffset = 30
        self.yoffset = 30
        self.zx = 1
        self.zxp = 100  # setting 2Px to rep 10Px in zoom
        self.countzp = 0

        self.startwindowcoord = None

    def SetOwnScale(self,x = 2,y = 2):
        self.sx = x
        self.sy = y
        self.initial = [x,y,30,30]

    def ChangeK(self,k):
        self.k = k
        self.ScaleUnit()
        self.linkerobject.ZoomPoints()
    
    def ScaleUnit(self):
        self.sx = self.sx * self.k
        self.sy = self.sy*self.k


    def ScaleZoom(self,y):
        self.ScaleZoom2(y)

    def ScaleZoom2(self,y):
        k = 1 + (self.zx*(y-self.zoompoint)/self.zxp)
        self.zoompoint = self.zoompoint + (y - self.zoompoint)
        self.ChangeK(k)
        
    def SetZoomPoint(self, y):
        self.zoompoint = y

    def ScaleZoom3(self,y0):
        deltascale1 = 120
        fraction = 0.2
        k = 1 + (fraction * y0/deltascale1)
        self.ChangeK(k)


    def ScaleNormal(self):
        self.k = 1
        self.sx = self.initial[0]
        self.sy = self.initial[1]
        self.xoffset = self.initial[2]
        self.yoffset = self.initial[3]
        self.linkerobject.ZoomNormal()


    def ScalePan(self,deltax,deltay):
        
        self.xoffset = self.xoffset + deltax
        self.yoffset = self.yoffset + deltay
        self.PanPoints()

    def PanPoints(self):
        self.linkerobject.PanPoints()

    

    def GetGeometry(self):
        width,height = self.linkerobject.GetCanvasGeometry()
        self.width = width - 1
        self.height = height - 1

    def PxCoordx(self,xunit): # recives unit values (in mm or in..)
                               # and returns pixel based on scale
        return (float(xunit)*self.sx/self.sxu) + self.xoffset

    def PxCoordy(self,yunit):# recives unit values (in mm or in..)
                               # and returns pixel based on scale
        return (float(yunit)*self.sy/self.syu) + self.yoffset

    def PxtoUnitx(self,xpixelvalue): # receives pixel value and
                                    #returns unit value based on scale
        return float(xpixelvalue - self.xoffset)*self.sxu/self.sx

    def PxtoUnity(self,ypixelvalue):
        return float(ypixelvalue - self.yoffset)*self.syu/self.sy










class ChartScreen:
    
    def __init__(self,linkerobject):
    # creating scrolled canvas

        self.linkerobject = linkerobject
        self.canvas = None

        
        self.posstring = "(x= %.3fmm, y = %.3fmm),(x = %.3f, y = %.3f)"
        self.pto_mm = 0.26484375
    def SetChartScale(self,reference):
        self.chartscale = reference
        
    def InitialiseCanvas(self,parent):
        self.parent1 = parent
        self.scrolledcanvas = Pmw.ScrolledCanvas(self.parent1,\
                              borderframe = 1,\
                              hscrollmode = "static",\
                              vscrollmode = "static")
        self.canvas = self.scrolledcanvas.interior()
        
        self.canvas.config(bg = "white",width = 631,height = 498)
        self.canvas.focus()
        self.Bind()
        self.linkerobject.AddCanvas(self,name = "ChartScreen")


        
        

    def UnBind(self):
        self.canvas.unbind("<Motion>",self.funcid1)
        

    def Bind(self):
        self.funcid1 =self.canvas.bind("<Motion>",self.ShowPoint)

    def ClearScreen(self):
        if self.canvas:
            self.canvas.delete(ALL)


        
    
    def SetNormal(self,event):
        self.linkerobject.ScaleNormal()

    def ShowSize(self,event):
        pass




    def Grid(self,row  = 0, column = 0):
        self.scrolledcanvas.grid(sticky = W+E+N+S,\
                         row = row, column = column)

        
    def ShowPoint(self,event):
        posstring = self.posstring%(\
        self.ScalePointx(self.canvas.canvasx(float(event.x),0.001)),\
        self.ScalePointy(self.canvas.canvasy(float(event.y),0.001)),\
        event.x,event.y)
        
        self.linkerobject.ShowPosition(posstring)

    def ScalePointx(self, xpoint):
        return self.chartscale.PxtoUnitx(xpoint)
    def ScalePointy(self, ypoint):
        return self.chartscale.PxtoUnity(ypoint)

    def Pixel_to_mm(self,number):
        return self.pto_mm * number


    def GetWidth(self):
        return self.canvas.winfo_width()
    def GetHeight(self):
        return self.canvas.winfo_height()
    def GetCanvasSheet(self):
        return self.canvas

    
    def CreateCenterPoint(self):
        width = (630 - 1 - self.chartscale.xoffset)/2
        height = (497 - 1 - self.chartscale.yoffset)/2
        self.centerpoint = self.linkerobject.PlotPoint(width+self.chartscale.xoffset,\
                                 height + self.chartscale.yoffset)
        


    


class DisplayLabel:
    def __init__(self, linkerobject):
        
        self.linkerobject = linkerobject
        self.linkerobject.Add(self,name = "DisplayLabel")

        
        self.posvariable = StringVar()
        self.posvariable.set('x=0,y =0')

    def SetFrame(self,frame):
        self.parent1 = frame
        self.label = Label(self.parent1,\
                textvariable = self.posvariable)


    def DisplayValue(self,astring):
        
        self.posvariable.set(astring)

    def Grid(self, row = 0, column = 0):
        self.label.grid(sticky = W+E+N+S, row = row,\
                        column = column)


class ToolBar:
    def __init__(self,linkerobject):


        self.linkerobject = linkerobject
        self.linkerobject.Add(self,name = "ToolBar")

    def SetFrame(self,frame):
        self.parent1 = frame
        self.GridComponent()
    def GridComponent(self):
        self.frame = Frame(self.parent1)
        self.frame.rowconfigure(0,weight = 1)
        


        self.panbutton = PanButton(self.frame,self.linkerobject)
        self.zoombutton = ZoomButton(self.frame,self.linkerobject)
        self.showbutton = ShowButton(self.frame, self.linkerobject)
        self.rotatebutton = RotateButton(self.frame, self.linkerobject)
        self.panbutton.Grid(row = 0, column = 0)
        self.zoombutton.Grid(row = 0, column = 1)
        self.rotatebutton.Grid(row =0, column = 2)
        self.showbutton.Grid(row = 0, column = 3)
        
    def Grid(self,row = 0, column = 0):
        self.frame.grid(sticky = NW, row = row,column = column)


#ZoomButtonClass begin
##################################################        
class ZoomButton:
    def __init__(self,parent1,linkerobject):
        self.parent1 = parent1
        self.count = 0
        self.count2 = 0
        self.linkerobject = linkerobject
        self.linkerobject.AddTool(self,name = "Zoom")
        self.GetCanvas()
        self.GetChartScale()
        self.BindDefault()
        try:
            self.image = PhotoImage(file = "SubFiles2\\Zoom_tool.gif")
        except Exception:
            self.zoombutton = Button(self.parent1,text = "Zoom",command = self.Zoom)
        else:
            self.zoombutton = Button(self.parent1,text = "Zoom",image = self.image ,command = self.Zoom)


    def Grid(self,row= 0, column = 0):
        self.zoombutton.grid(sticky = NW, row = row,column = column)

    def BindDefault(self):
        self.canvas.bind("<Enter>",self.Register)
        self.canvas.bind("<Leave>",self.UnRegister)
        self.funcid3 = self.canvas.bind("<Double-Button-2>",self.SetNormal)

    def Register(self,event):
        self.ingraph = 1

    def UnRegister(self,event):
        self.ingraph = 0

    def GetCanvas(self):
        self.canvasobject = self.linkerobject.GetCanvas()
        self.canvas = self.canvasobject.GetCanvasSheet() #come back1

    def GetChartScale(self):
        self.chartscale = self.linkerobject.GetChartScale()

    def Zoom(self):
        self.count2+= 1
        if self.count2 == 1:
            self.SetAsCurrent()
        self.Zoom1()

    def Zoom1(self):
        self.count +=1
        if self.count == 1:
            self.Bind()
            self.zoombutton.configure(relief = RIDGE)
        else:
            self.RemoveAsCurrent()
            self.count = 0
            self.count2 = 0
            self.UnBind()
            self.zoombutton.configure(relief = RAISED)

    def TurnOff(self):
        self.Zoom1()
        


    def Bind(self):
        self.linkerobject.UnBindCanvas()
        self.funcid1 = self.canvas.bind("<Button-1>",self.SetZoomPoint)
        self.funcid2 = self.canvas.bind("<B1-Motion>",self.ZoomFigure)

    def UnBind(self):
        
        self.linkerobject.BindCanvas()
        self.canvas.unbind("<Button-1>",self.funcid1)
        self.canvas.unbind("<B1-Motion>",self.funcid2)
##        self.canvas.unbind("<Double-Button-2>",self.funcid3)

    def SetAsCurrent(self):
        self.linkerobject.SetCurrentTool("Zoom")
    def RemoveAsCurrent(self):
        self.linkerobject.SetCurrentTool2()


    def SetNormal(self,event):
        self.TurnOff()
        self.linkerobject.SetNormal()

    def SetZoomPoint(self,event):
        self.zoompointy = self.canvas.canvasy(event.y)
        self.chartscale.SetZoomPoint(self.zoompointy)

    def ZoomFigure(self,event):
        self.chartscale.ScaleZoom(self.canvas.canvasy(event.y))

##    def ZoomFigure2(self,event):
##        self.chartscale.ScaleZoom(event.delta / 360)

    def ZoomWheel(self,value):
        if self.ingraph:
            self.chartscale.ScaleZoom3(value)
        else:
            pass

#ZoomButtonClass end
##########################################




#PanButtonClass begin
################################################################        
class PanButton:
    def __init__(self,parent1,linkerobject):
        self.parent1 = parent1
        self.count = 0
        self.count2 = 0
        self.linkerobject = linkerobject
        self.linkerobject.AddTool(self,name = "Pan")
        self.GetCanvas()
        self.GetChartScale()
        self.BindDefault()
        try:
            self.panimage = PhotoImage(file = "SubFiles2\\pan_tool.gif")
        except Exception:
            self.panbutton = Button(self.parent1,text = "Pan",command = self.Pan)
        else:
            self.panbutton = Button(self.parent1,image = self.panimage,command = self.Pan)

    def BindDefault(self):
        self.default1 = self.canvas.bind("<ButtonPress-2>",self.SetPanPoint)
        self.BindDefault2()
    def BindDefault2(self,event = None):
        self.default2 = self.canvas.bind("<B2-Motion>",self.PanFigure)
        self.default3 = self.canvas.bind("<ButtonRelease-2>",self.UnbindDefault)

    def UnbindDefault(self,event):
        self.canvas.unbind(self.default2)
        self.canvas.unbind(self.default3)
        
        
    def Grid(self,row= 0, column = 0):
        self.panbutton.grid(sticky = NW, row = row,column = column)

    def GetCanvas(self):
        self.canvasobject = self.linkerobject.GetCanvas()
        self.canvas = self.canvasobject.GetCanvasSheet()

    def GetChartScale(self):
        self.chartscale = self.linkerobject.GetChartScale()


    def Pan(self):
        self.count2 += 1
        if self.count2 == 1:
            self.SetAsCurrent()
        self.Pan1()
    def Pan1(self):
        self.count +=1
        if self.count == 1:
            self.Bind()
            self.panbutton.configure(relief = RIDGE)
        else:
            self.RemoveAsCurrent()
            self.count = 0
            self.count2 = 0
            self.UnBind()
            self.panbutton.configure(relief = RAISED)
            

    def TurnOff(self,event = None):
        self.Pan1()
    def SetAsCurrent(self):
        self.linkerobject.SetCurrentTool("Pan")
    def RemoveAsCurrent(self):
        self.linkerobject.SetCurrentTool2()

    def Bind(self):
        self.linkerobject.UnBindCanvas()
        self.funcid1 = self.canvas.bind("<Button-1>",self.SetPanPoint)
        self.funcid2 = self.canvas.bind("<B1-Motion>",self.PanFigure)
        self.funcid3 = self.canvas.bind("<Double-Button-2>",self.SetNormal)

    def UnBind(self):
        self.linkerobject.BindCanvas()
        self.canvas.unbind("<Button-1>",self.funcid1)
        self.canvas.unbind("<B1-Motion>",self.funcid2)
        self.canvas.unbind("<Double-Button-2>",self.funcid3)


    def SetNormal(self,event):
        self.TurnOff()
        self.linkerobject.SetNormal()

    def SetPanPoint(self,event):
        self.panpointx = self.canvas.canvasx(event.x)
        self.panpointy = self.canvas.canvasy(event.y)

    def PanFigure(self,event):
        deltax = self.canvas.canvasx(event.x) - self.panpointx
        deltay = self.canvas.canvasx(event.y) - self.panpointy
        self.panpointx = self.panpointx + deltax
        self.panpointy = self.panpointy + deltay
        self.chartscale.ScalePan(deltax,deltay,)
    
#PanButtonClass end
####################################################


#ShowButtonClass begin
########################################        
class ShowButton:
    def __init__(self,parent1,linkerobject):
        self.parent1 = parent1
        self.linkerobject = linkerobject
        self.linkerobject.AddTool(self,name = "Show")
        
        self.frame = Frame(self.parent1)
        self.frame.rowconfigure(0, weight = 1)
        self.frame.columnconfigure(0,weight = 1)
        self.frame.columnconfigure(1,weight = 1)
        
        self.button1variable = BooleanVar()
        self.button2variable = BooleanVar()
        self.button1 = Checkbutton(self.frame,text = "ShowLabels",\
                                   variable = self.button1variable,
                                   command = self.ShowLabels)
        self.button2 = Checkbutton(self.frame,text = "ShowPatternLines",\
                                   variable = self.button2variable,
                                   command = self.ShowPatternLines)
        self.button1.grid(sticky = W, row = 0, column = 0)
        self.button2.grid(sticky = W,row = 0, column = 1)

        self.button1.invoke()
        self.button2.invoke()
        
        
    def Grid(self,row= 0, column = 0):
        self.frame.grid(sticky = NW, row = row,column = column)


    def ShowLabels(self):
        if self.button1variable.get():
            self.linkerobject.ShowLabels()
        else:
            self.linkerobject.UnShowLabels()

    def ShowPatternLines(self):
        if self.button2variable.get():
            self.linkerobject.ShowPatternLines()
        else:
            self.linkerobject.UnShowPatternLines()
#ShowButtonClass end
################################################################             

#RotateDialogClass begin
##############################################            
class RotateDialog(Toplevel):
    def __init__(self):
        Toplevel.__init__(self,root = None)
        self.title('Rotate')
        self.geometry('100x100')#currently working


#RotateDialogClass end
###########################

#RotateButtonClass begin
################################################            
class RotateButton:
    def __init__(self,parent1,linkerobject):
        self.parent1 = parent1
        self.count = 0
        self.count2 = 0
        try:
            self.image = PhotoImage(file = "SubFiles2\\Zoom_tool.gif")
            raise IOError
        except Exception:
            self.zoombutton = Button(self.parent1,text = "Rotate",command = self.Rotate)
        else:
            self.zoombutton = Button(self.parent1,text = "Rotate",image = self.image ,command = self.Rotate)

    def Grid(self,row= 0, column = 0):
        self.zoombutton.grid(sticky = NW, row = row,column = column)

    def GetCanvas(self):
        self.canvasobject = self.linkerobject.GetCanvas()
        self.canvas = self.canvasobject.GetCanvasSheet()

    def GetChartScale(self):
        self.chartscale = self.linkerobject.GetChartScale()

    def Rotate(self):
        pass

    def Zoom1(self):
        self.count +=1
        if self.count == 1:
            self.Bind()
            self.zoombutton.configure(relief = RIDGE)
        else:
            self.RemoveAsCurrent()
            self.count = 0
            self.count2 = 0
            self.UnBind()
            self.zoombutton.configure(relief = RAISED)

    def TurnOff(self):
        self.Zoom1()
        


    def Bind(self):
        self.linkerobject.UnBindCanvas()
        self.funcid1 = self.canvas.bind("<Button-1>",self.SetZoomPoint)
        self.funcid2 = self.canvas.bind("<B1-Motion>",self.ZoomFigure)
        self.funcid3 = self.canvas.bind("<Double-Button-2>",self.SetNormal)

    def UnBind(self):
        
        self.linkerobject.BindCanvas()
        self.canvas.unbind("<Button-1>",self.funcid1)
        self.canvas.unbind("<B1-Motion>",self.funcid2)
        self.canvas.unbind("<Double-Button-2>",self.funcid3)

    def SetAsCurrent(self):
        self.linkerobject.SetCurrentTool("Zoom")
    def RemoveAsCurrent(self):
        self.linkerobject.SetCurrentTool2()


    def SetNormal(self,event):
        self.TurnOff()
        self.linkerobject.SetNormal()

    def SetZoomPoint(self,event):
        self.zoompointy = self.canvas.canvasy(event.y)
        self.chartscale.SetZoomPoint(self.zoompointy)

    def ZoomFigure(self,event):
        self.chartscale.ScaleZoom(self.canvas.canvasy(event.y))





#RotateButtonClass end
################################################            



class PointClass:
    def __init__(self,linkerobject):        
        self.Count = 0
        self.LineOn = 0
        self.PointDict = {}
        self.SetLinkerObject(linkerobject)
        
        

    def Point(self,x,y,see = 0, usescale = 0):
        point = PointObject(x,y,see = see, usescale = usescale,parent = self)
        return point

    def InsertPoint(self,pointname,reference):
        self.PointDict[pointname] = reference

    def CountPoint(self):
        self.Count += 1
        return self.Count

    def SetLinkerObject(self,reference):
        self.linkerobject = reference

    def SetChartScale(self):
        self.PointChartScale = self.linkerobject.GetChartScale()

    def SetPointCanvas(self):
        self.PointCanvas = self.PointCanvasClass.GetCanvasSheet()

    def SetPointCanvasClass(self):
        self.PointCanvasClass = self.linkerobject.GetCanvas()

    def SetAll(self):
        self.SetChartScale()
        self.SetPointCanvasClass()
        self.SetPointCanvas()

    def Update(self):
        for item in self.PointDict:
            self.PointDict[item].RescalePoint()
        
    def ZoomNormal(self):
        for item in self.PointDict:
            self.PointDict[item].SetNormal()
       
    def SetNormal(self):
        for item in self.PointDict:
            self.PointDict[item].SetNormal()

    def ShowPoints(self):
        for item in self.PointDict:
            self.PointDict[item].CreatePoint()
    def HidePoints(self):        
        for item in self.PointDict:
            self.PointDict[item].Delete()

    def ClearScreen(self):
        self.PointDict = {}
        
    


class PointObject: 
    def __init__(self,x,y,see = 1,usescale = 0,parent = None):

        self.xunit = x
        self.yunit = y
        self.parent = parent
        self.CountPoint()
        self.see = see
        
        if usescale:
            self.ScalePoint()
        else:
            self.x = self.xunit
            self.y = self.yunit
            
        self.tagname = "%.3f,%.3f,%d"%(self.xunit,self.yunit,self.no)
        self.InsertPoint()

        if see:
            self.CreatePoint()

    def InsertPoint(self):
        self.parent.InsertPoint(self.tagname,self)

    def CountPoint(self):
        self.no = self.parent.CountPoint()


    def ScalePointx(self,x):
        return self.parent.PointChartScale.PxCoordx(x)

    def ScalePointy(self,y):
        return self.parent.PointChartScale.PxCoordy(y)


    
    def ScalePoint(self):
        self.x = self.ScalePointx(self.xunit)
        self.y = self.ScalePointy(self.yunit)

        

    def Delete(self):
        self.parent.PointCanvas.delete(self.tagname)
    def RescalePoint(self):
        self.Delete()
        self.ScalePoint()
        if self.see:
            self.CreatePoint()
        
    def SetNormal(self):
        self.ScalePoint()
        self.Delete()
        if self.see:
            self.CreatePoint()
        


    def Pixel_to_mm(self,number):
        return self.pto_mm * number




    def CreatePoint(self):
        self.parent.PointCanvas.create_oval(self.x-3,self.y-3,self.x+3,\
                                 self.y+3,fill = "green",\
                                  tag = self.tagname,activefill = "blue",\
                                          )

    
        
####################################################################################
####################################################################################
####################################################################################

class LineClass:
    def __init__(self,linkerobject):
        self.Count = 0
        self.LineOn = 0
        self.LineDict = {}
        self.OutLineDict = {}
        self.NotOutLineDict = {}
        self.SetLinkerObject(linkerobject)
        self.showlabels = 1
        self.showpatternlines = 1


    def Line(self,color = "green",outline = 1,label = None):
        line = LineObject(parent = self,color = color,\
                          outline = outline,label = label)
        return line

    def CountLine(self):
        self.Count += 1
        return self.Count

    def InsertLine(self,name,reference,outline = 1):
        self.LineDict[name] = reference
        if not outline:
            self.NotOutLineDict[name] = reference

    def Point(self,x,y,see = 0, usescale = 0):
        pointref = self.Pointclass.Point(x = x,y = y, see = see, usescale = usescale)
        return pointref
    
    def SetLinkerObject(self,reference):
        self.linkerobject = reference

    def SetLineCanvas(self):
        self.LineCanvas = self.LineCanvasClass.GetCanvasSheet()

    def SetLineChartScale(self):
        self.LineChartScale = self.linkerobject.GetChartScale()

    def SetLineCanvasClass(self):
        self.LineCanvasClass = self.linkerobject.GetCanvas()

    def SetPointClass(self):
        self.Pointclass = self.linkerobject.GetPointClass()

    def SetAll(self):
        self.SetLineCanvasClass()
        self.SetLineCanvas()
        self.SetLineChartScale()
        self.SetPointClass()

    def Update(self):
        for item in self.LineDict:
            self.LineDict[item].ReDrawLine()

    def ZoomNormal(self):
        for item in self.LineDict:
            self.LineDict[item].ReDrawLine()


    def ClearScreen(self):
        self.showpatternlines = 0
        self.showlabels = 0
        self.LineDict = {}
        self.NotOutLineDict = {}
        

        
    def ShowLabels(self):
        self.showlabels = 1
        for item in self.LineDict:
            self.LineDict[item].showlabel = 1
            self.LineDict[item].CreateLabel()
            

    def UnShowLabels(self):
        self.showlabels = 0
        for item in self.LineDict:
            self.LineDict[item].DeleteLabel()
            self.LineDict[item].showlabel = 0

    def ShowPatternLines(self):
        self.showpatternlines = 1
        for item in self.NotOutLineDict:
            self.NotOutLineDict[item].showpatternline = 1
            self.NotOutLineDict[item].CreateLine2()

    def UnShowPatternLines(self):
        self.showpatternlines = 0
        for item in self.NotOutLineDict:
            self.NotOutLineDict[item].DeleteLine()
            self.NotOutLineDict[item].showpatternline = 0

    def DisplayResult(self,value):
        self.linkerobject.DisplayResult(value)






class LineObject:
    def __init__(self,parent = None,color = "green",outline = 1,label = None,showlabel = 1):
        self.parent = parent
        self.CountLine()
        self.outline = outline
        self.showlabel = showlabel
        self.showpatternline = 1
        self.label = label
        self.drawnalready = 0
        self.labelalready = 0
        
        self.tagname = "Line%s"%str(self.no)
        if self.label:
            self.labeltagname = self.tagname+self.label

        self.InsertLine()
        self.SetColor(color)
        self.multiline = 0

    def Bind(self):
        self.parent.LineCanvas.tag_bind(self.tagname,"<Button-1>",self.ShowValues)

    def CountLine(self):
        self.no = self.parent.CountLine()

    def InsertLine(self):
        self.parent.InsertLine(self.tagname,self,self.outline)

    def CreateLabel(self):
        if not self.labelalready:
            if self.label:
                if self.showlabel:
                    self.parent.LineCanvas.create_text(self.GetMidPoint3() + 4,\
                                                                   self.GetMidPoint4() + 4,\
                                                               text = self.label,font = "Times 5",\
                                                                   tag = self.labeltagname
                                                                   )
                    self.labelalready = 1


                    
    def DeleteLabel(self,showlabel = 1):
        if self.label:
            self.parent.LineCanvas.delete(self.labeltagname)
        self.labelalready = 0

    def DeleteLine(self):
        self.parent.LineCanvas.delete(self.tagname)
        self.drawnalready = 0


    def CreateLine(self):   # creates line on canvas
        self.CreateLine2()

##        self.CreateLabel()
##
##
##        self.parent.LineCanvas.create_line(self.point1.x,self.point1.y,\
##                                self.point2.x,self.point2.y,width = 1.2,\
##                                    fill = self.color,\
##                  splinesteps = 0,tag = self.tagname,activefill = "blue")
##        self.drawnalready = 1
##        self.Bind()

    def CreateLine2(self):
        if not self.drawnalready:
            self.CreateLabel()
            if self.showpatternline:
               


                self.parent.LineCanvas.create_line(self.point1.x,self.point1.y,\
                                        self.point2.x,self.point2.y,width = 1.2,\
                                            fill = self.color,\
                          splinesteps = 0,tag = self.tagname,activefill = "blue")
                self.Bind()
                self.drawnalready = 1




    def Delete(self):
        if self.label:
            self.parent.LineCanvas.delete(self.labeltagname)
        self.parent.LineCanvas.delete(self.tagname)
        self.drawnalready = 0
        self.labelalready = 0

        

    def CreatePoint1(self,x,y): # creates point1 attr
        self.point1 = self.parent.Point(x,y,see = 0,usescale = 1)

    def CreatePoint2(self,x,y): # creates point2 attr
        self.point2 = self.parent.Point(x,y,see = 0,usescale = 1)
        
    def CreatePoints(self,x1,y1,x2,y2): # create point attr given two points
        self.CreatePoint1(x1,y1)
        self.CreatePoint2(x2,y2)

    def CreatePointN(self,atuple):
        pointn = self.parent.Point(atuple[0],atuple[1],see = 0, usescale = 1)
        return pointn

    


    def CalculateCoord(self,length,angle): # calc next coord given pt, len & angle,
        self.length = length
        self.angle = angle
        self.CalculateGradient()
        x2 = self.Getx1() + Decimal((length*Cos(angle)))
        y2 = self.Gety1() + Decimal((length*Sin(angle)))
        self.CreatePoint2(x2, y2)



    def DrawLine1(self,x1,y1,x2,y2):# given two points (x0,y0),(x1,y1)
        self.CreatePoints(x1,y1,x2,y2)
        self.CalculateLength()
        self.CalculateAngle()
        self.CalculateGradient()
        self.CreateLine()

    def DrawLine2(self,point1,point2):# given two point objects
        self.SetPointObject(point1,point2)
        self.CalculateLength()
        self.CalculateAngle()
        self.CalculateGradient()
        self.CreateLine()
        


    def DrawLine3(self,atuple,point2): # given 1 point & 1 point object
        self.SetPointObj2(point2)
        self.CreatePoint1(atuple[0],atuple[1])
        self.CalculateLength()
        self.CalculateAngle()
        self.CalculateGradient()
        self.CreateLine()

    def DrawLine4(self,atuple,length,angle = 30):# given pt, length ,
                                                # and angle
        self.CreatePoint1(atuple[0], atuple[1])
        self.CalculateCoord(length,angle)
        self.CreateLine()
        

    def DrawLine5(self,point1,length,angle): # given point obj, length ,
                                                # and angle
        
        self.SetPointObj1(point1)
        self.CalculateCoord(length,angle)
        self.CreateLine()

  
    def DrawLine6(self,ptuple,splinesteps = 3,smooth= True):
        self.CreateMultiplePoints(ptuple)
        self.CreateLine3()

    def CreateMultiplePoints(self,ptuple):
        self.plist = []
        for item in ptuple:
            self.plist.append(self.CreatePointN(item))

    def GetMultiplePoints(self):
        self.plist2 = []
        for item in self.plist:
            self.plist2.append((item.x,item.y))
        

    def CreateLine3(self):
        self.GetMultiplePoints()
        self.parent.LineCanvas.create_line(self.plist2,width = 1.2,\
                                    fill = self.color,\
                  splinesteps = self.splinesteps,smooth = True,tag = self.tagname,activefill = "blue")




    def Initialize1(self,atuple1,atuple2):# given two points (x0,y0),(x1,y1)
        self.DrawLine1(atuple1[0],atuple1[1],\
                       atuple2[0],atuple2[1])

    def Initialize2(self,point1,point2): # given two point objects
        self.DrawLine2(point1,point2)

    def Initialize3(self,atuple,point2): # given 1 point & 1 object
        self.DrawLine3(atuple,point2)

    def Initialize4(self,atuple,length,angle = 30): # given pt, length ,
        self.DrawLine4(atuple,length,angle)            # and angle



    def Initialize5(self,point1,length, angle = 30):# given point obj, length ,
                                                # and angle
        self.DrawLine5(point1,length,angle)

    def Initialize6(self,ptuple,splinesteps= 3,smooth = True): # a list of tuples of pt
        self.multiline = 1
        self.splinesteps = splinesteps
        self.DrawLine6(ptuple,splinesteps = splinesteps,smooth = smooth)



    def ShowValues(self,event):
        information = {}
        if self.label:
            information ["Name"] = self.label
        information ["Length"] = Decimal(self.length,1)
        information["Angle"] = Decimal(self.angle,1)

        self.parent.DisplayResult(information)

    # Set Methods
    def SetColor(self,color = "green"):
        if self.outline:
            self.color = "green"
        else:
            self.color = "red"
            


        
    def SetPointObject(self,point1,point2): # 2 point object
        self.SetPointObj1(point1)
        self.SetPointObj2(point2)

    def SetPointObjectAndLine(self,point1,length,angle):
        self.point1 = point1
        self.length = length


    def SetPointObj1(self,point): # create point attr given obj
        self.point1 = point

    def SetPointObj2(self,point): # create point attr given obj
        self.point2 = point

    def GetPoint1(self):
        return self.point1

    def GetPoint2(self):
        return self.point2

    def GetMidPoint3(self):
        return (self.point1.x + self.point2.x)/2.0
    def GetMidPoint4(self):
        return (self.point1.y + self.point2.y)/2.0

    def GetMidPoint1(self):
        return (self.Getx1() + self.Getx2())/2.0
    def GetMidPoint2(self):
        return (self.Gety1() + self.Gety2())/2.0

    def GetDividePoint(self,a,b):
        xp = ((b*self.Getx1()) + (a * self.Getx2()))/(a + b)
        yp = ((b*self.Gety1()) + (a * self.Gety2()))/(a + b)
        return (xp,yp)


    def Getx1(self):
        return self.point1.xunit
    def Getx2(self):
        return self.point2.xunit
    def Gety1(self):
        return self.point1.yunit
    def Gety2(self):
        return self.point2.yunit



    def CalculateLength(self):
        self.length =  math.sqrt(pow((self.point2.xunit  - self.point1.xunit),2) + \
                         pow((self.point2.yunit - self.point1.yunit),2))
    
    def CalculateAngle(self):
        if (self.point2.xunit - self.point1.xunit) == 0:
            self.angle = None
        else:
            self.angle = RadtoDeg(math.atan((self.point2.yunit - self.point1.yunit)/\
                                  (self.point2.xunit - self.point1.xunit)))
    def CalculateGradient(self):
        self.gradient = 0# math.tan(DegtoRad(self.angle))
        
        
        
    def ReDrawLine(self):
        self.Delete()
        if self.multiline:
            self.CreateLine3()
        else:
            self.CreateLine2()


####################################
####################################  END OF IMPLEMENTATION CLASS
####################################
####################################



#LinkerObjectClass begin
##########################################################
class LinkerObject:
    def __init__(self):
        self.itemdict = {}
        self.classobjdict = {}
        self.tooldict = {}
        self.currenttool = None
        self.SetClasses()

    def GetPointClass(self):
        return selt.classobjdict["PointClass"]

    def SetClasses(self):
        self.classobjdict["PointClass"] = PointClass(self)
        self.classobjdict["LineClass"] = LineClass(self)

    def DisplayResult(self,value):
        self.itemdict["DisplayResult"].InsertValue(value)


    def AddCanvas(self, item, name):
        self.Add(item,name)
        self.AddCanvasToPoint()
        self.AddCanvasToLine()
        
    def Add(self,item,name):
        self.itemdict[name] = item

    def ShowPosition(self, astring):
        self.itemdict["DisplayLabel"].DisplayValue(astring)

    def ShowLabels(self):
        self.classobjdict["LineClass"].ShowLabels()

    def UnShowLabels(self):
        self.classobjdict["LineClass"].UnShowLabels()

    def ShowPatternLines(self):
        self.classobjdict["LineClass"].ShowPatternLines()

    def UnShowPatternLines(self):
        self.classobjdict["LineClass"].UnShowPatternLines()

    def PlotPoint(self, x,y,usescale = 0):
        Point(x,y,usescale= usescale)

    def ClearScreen(self):
        if self.itemdict.has_key("ChartScreen"):
            self.itemdict["ChartScreen"].ClearScreen()
            self.classobjdict["LineClass"].ClearScreen()

   

    
    def AddCanvasToPoint(self):
        self.classobjdict["PointClass"].SetAll()

    def AddCanvasToLine(self):
        self.classobjdict["LineClass"].SetAll()

    def AddTool(self,tool,name):
        self.tooldict[name] = tool

    def SetCurrentTool(self,name):
        if self.currenttool:
            self.currenttool.TurnOff()
        self.currenttool = self.tooldict[name]
    def SetCurrentTool2(self):
        self.currenttool = None

    def SetScale(self,x,y):
        self.itemdict["ChartScale"].SetOwnScale(x,y)


    def GetCanvasGeometry(self):
        return self.itemdict["ChartScreen"].GetWidth(),\
               self.itemdict["ChartScreen"].GetHeight()
    def GetCanvas(self):
        return self.itemdict["ChartScreen"]
    def GetChartScale(self):
        return self.itemdict["ChartScale"]
    def GetPointClass(self):
        return self.classobjdict["PointClass"]
    def GetLineClass(self):
        return self.classobjdict["LineClass"]
    def Get(self,name):
        return self.itemdict["name"]
        
    def ZoomPoints(self):
        self.Update()
    def Update(self):
        self.classobjdict["PointClass"].Update()
        self.classobjdict["LineClass"].Update()

    def UnBindCanvas(self):
        self.itemdict["ChartScreen"].UnBind()
        
    def BindCanvas(self):
        self.itemdict["ChartScreen"].Bind()

    def PanPoints(self):
        self.Update()

    def TurnAllToolOff(self):
        if self.currenttool:
            self.currenttool.TurnOff()
        
        
    def ZoomNormal(self):
        self.classobjdict["PointClass"].SetNormal()
        self.classobjdict["LineClass"].ZoomNormal()

    def SetNormal(self): #go back
        self.itemdict["ChartScale"].ScaleNormal()
        self.ZoomNormal()

    def AdjustView(self,xf,yf):
        self.itemdict["ChartScreen"].canvas.xview_scroll(xf,"units")
        self.itemdict["ChartScreen"].canvas.yview_scroll(yf,"units")

    def DeltaAlpha(self,z1,z2,theta):
        return Acos(((pow(z1,2)) + \
                (pow(z2,2)) - (pow((2*300*Sin(theta/2)),2)))/\
                    (2*z1*z2))

    
    def Run(self,name):
        pass
        






class GraphGui:
    def __init__(self,optionref):
        self.count = 0
        self.SetOptionRef(optionref)
        self.SetLinkerObject()
        self.frame = None
        self.cleargraph = 0


        self.chartscale = ChartScale(self.linkerobject)

        
        self.canvas = \
                    ChartScreen(self.linkerobject)

        self.canvas.SetChartScale(self.chartscale)

        self.poslabel = \
                      DisplayLabel(self.linkerobject)

        self.toollabel = \
                      ToolBar(self.linkerobject)

        self.displayresult = DisplayResultClass(self,row = 0,column = 0,size = (100,300) )
        self.linkerobject.Add(self.displayresult,"DisplayResult")


    def InitialisePlot(self,parent):  #return to graph
        self.count += 1
        if self.count == 1:
            self.master = parent
            try:
                self.master.state(GetZoomedStateOption(sys.platform))
            except Exception:
                pass             
            self.master.CreateMenuBar() #Include menubar
            self.master.title(self.optionref.name+" Plot")
            self.master.SetLinkerObject(self.linkerobject)
            
            
            self.master.rowconfigure(1, weight = 1)
            self.master.columnconfigure(0, weight = 1)

            self.frame = Frame(self.master)
            self.frame.columnconfigure(0,weight = 1)
            
            self.frame.grid(sticky = W+E+N+S, row = 1, column = 0)
            self.frame.rowconfigure(1,weight = 1)
            self.frame.columnconfigure(0,weight = 1)
            self.frame2 = Frame(self.frame)
##            self.frame2.columnconfigure(0,weight = 1)
            self.frame2.columnconfigure(1,weight = 1)
            self.frame2.rowconfigure(0,weight = 1)
            self.frame2.grid(sticky = W+E+N+S, row = 1, column = 0)

            self.SetFrames()
            self.master.SetZoomObject(self.toollabel.zoombutton)
            self.cleargraph = 1
            
        else:
##            self.frame.grid(sticky = W+E+N+S, row = 0, column = 0)
            self.ClearGraph()

            
    def HasEdited(self,event = None):
        self.master.SetHasEdited()

        

    def SetLinkerObject(self):
        self.linkerobject  = self.optionref.GetLinkerObject()

    def ClearGraph(self):
        self.cleargraph = 0
        self.linkerobject.ClearScreen()
        self.displayresult.ClearScreen()

    def SetOptionRef(self,reference):
        self.optionref = reference

    def GridComponents(self):
        self.canvas.Grid(row = 0, column = 1)
        self.poslabel.Grid(row = 2, column = 0)
        self.toollabel.Grid(row = 0, column = 0)

    def SetFrames(self):
        self.canvas.InitialiseCanvas(self.frame2)
        self.displayresult.CreateWindow(self.frame2)
        self.poslabel.SetFrame(self.frame)
        self.toollabel.SetFrame(self.frame)
        self.GridComponents()

    def SetName(self,name):
        self.name = name
        if self.count:
            self.master.title(self.name+" Plot")
        

    def ShowPlot(self):
        self.mainloop()

    def Destroy(self):
        self.count = 0
        if self.cleargraph:
            self.ClearGraph()
        self.linkerobject.TurnAllToolOff()
        if self.frame:
            self.frame.destroy()



############################################################################ BEGINING OF TRANSITION PIECE CLASS
############################################################################
############################################################################




#ConicalFrustumClass begin
##########################################################################################            
class ConicalFrustum:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.5
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        self.parent.ShowResult1(\
            self.dimensiondict,\
            self.valuedict,\
            self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle

        self.topdiameter = self.diameter1 - self.thickness # mean diameter
        self.basediameter = self.diameter2 - self.thickness # mean diameter
        self.topradius = self.topdiameter / 2
        self.baseradius = self.basediameter / 2
        # calculate L values
        self.CalcL1()
        self.CalcRp()
        self.CalcRc()
        self.CalcThetaPattern()
        self.CalcZ()

        
    def CalcL1(self):
        self.l1 = Decimal(math.sqrt(pow((self.baseradius - self.topradius),2) + pow((self.height),2)))
        self.otherdict["L1"] = self.l1
    def CalcRp(self):
        self.rp = Decimal((self.basediameter / (2 * (self.basediameter - self.topdiameter)))*\
                          math.sqrt(pow((self.basediameter - self.topdiameter),2) + (4*pow((self.height),2))))
        self.otherdict["Pattern Radius Rp"] = self.rp
        
    def CalcRc(self):
        self.rc = Decimal((self.topdiameter / (2 * (self.basediameter - self.topdiameter)))*\
                          math.sqrt(pow((self.basediameter - self.topdiameter),2) + (4*pow((self.height),2))))
        self.otherdict["Cut Radius Rc"] = self.rc

    def CalcThetaPattern(self):
        self.thetapattern = Decimal((360 * (self.basediameter - self.topdiameter)/\
                          math.sqrt(pow((self.basediameter - self.topdiameter),2) + (4*pow((self.height),2)))))
        self.deltatheta_pattern = self.thetapattern / self.n
        self.otherdict["Pattern Angle"] = self.thetapattern

    def CalcZ(self):
        self.z =  Decimal(math.sqrt( pow((-self.topradius  + (self.baseradius* Cos(self.circleangle))),2) +\
                                  pow((self.baseradius*Sin(self.circleangle)),2) +\
                                  pow((self.height),2)))

        self.otherdict["Z"] = self.z

    def CalcThetaN(self,n):
        return self.thetapattern * n

    def CalcPoint1(self,n):
        line2coordx1 = self.a0 + (self.rp*(1 - Cos(n *self.deltatheta_pattern)))
        line2coordy1 = self.a1 + (self.rp*Sin(n *self.deltatheta_pattern))
        return (line2coordx1, line2coordy1)

    def CalcPoint2(self,n):
        line2coordx2 = self.a0 + (self.rp - ((self.rp - self.l1) * Cos(n* self.deltatheta_pattern)))
        line2coordy2 = self.a1 + ((self.rp - self.l1)*Sin(n * self.deltatheta_pattern))
        return (line2coordx2, line2coordy2)
                            
            
      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.linelist = []
        self.line1 = self.Line(label = "Z")
        self.line1.Initialize4((self.a0,self.a1),self.l1,0)
        self.linelist.append(self.line1)

        for i in range(self.n):
            if i == self.n-1:
                outline2 = 1
            else:
                outline2 = 0
            line2 = self.Line(label = "Z",outline = outline2)
            line2.Initialize1(self.CalcPoint1(i+1),self.CalcPoint2(i+1))
            self.linelist.append(line2)


        for i in range(self.n):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i].GetPoint1(),\
                              self.linelist[i+1].GetPoint1())
            
            line4 = self.Line()
            line4.Initialize2(self.linelist[i].GetPoint2(),\
                              self.linelist[i+1].GetPoint2())

            line6 = self.Line()
            line6.Initialize2(self.linelist[i].GetPoint2(),\
                              self.linelist[i+1].GetPoint1())



    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Top Diameter"] = self.diameter1
        self.dimensiondict["Base Diameter"] = self.diameter2
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n

    def SetInput(self,values):
        self.SetDiameterTop(values ["Top diameter"])
        if not self.stop:
            self.SetDiameterBase(values["Base diameter"])
            if not self.stop:
                self.SetHeight(values["Height"])
                if not self.stop:
                    self.SetFacetNumber(values["Facet number"])


    def SetDiameterTop(self,value):
        if value:
            try:

                self.diameter1 = float(value)
                if self.diameter1 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Top Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Top Diameter")


    def SetDiameterBase(self,value):
        if value:
            try:
                self.diameter2 = float(value)
                if self.diameter2 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Base Diameter"""%value)
            else:
                if self.diameter1 == self.diameter2:
                    self.ShowError("""Cannot have base diameter and top diameter\nto be the same""")
                    self.stop = 1
                else:           
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Base Diameter")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Facet Number"""% value)
            else:
                    
                if value2 > 18 or value2 < 6:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Facet Number\n valid range 6 to 18"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Facet Number")

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject

#ConicalFrustumClass end
##########################################################################################            


#RectToRoundObliqueClass begin
##########################################################################################            

class RectToRoundOblique:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()
        
        self.a0 = 150
        self.a1 = 700

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Zlines = []
        self.Ylines = []
        self.Wlines = []
        self.Xlines = []
        self.Zulines = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        self.parent.ShowResult1(\
            self.dimensiondict,\
            self.valuedict,\
            self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 90.0/float(self.n)

        self.v = (self.length/2)
        self.vprime = (self.length/2)*Sin(self.inclination)
        self.hprime = self.height - (self.length*Cos(self.inclination))
        self.u = self.breadth/2
        self.r = self.diameter/2 #+ (self.thickness/2)
        # calculate L values. Only compute L5

        self.CalcL3()
        self.CalcL5()

        self.CalcMValues()
        self.CalcZValues()
        self.CalcYValues()
        self.CalcWValues()
        self.CalcXValues()

        
        self.CalcPhi_U()
        self.CalcPhi_U2()
        self.CalcPhi_U3()
        self.CalcPhi_U4()
        self.CalcPhi_V()
        self.CalcPhi_V2()
        self.CalcPhi_V3()
        self.CalcPhi_V4()
        self.CalcPhi_V5()


        self.CalcTheta1()
        self.CalcTheta2()
        self.CalcTheta3()
        self.CalcTheta4()
        
    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter / (4*self.n),2)
        self.otherdict["M"] = self.M


    def CalcL3(self):
        self.l3 = Decimal(math.sqrt(pow((self.vprime - self.r),2) + pow((self.hprime),2)))
        self.otherdict["L3"] = self.l3


    def CalcL5(self):
        self.l5 = Decimal(math.sqrt(pow((self.vprime - self.r),2) + pow((self.height),2)))
        self.otherdict["L5"] = self.l5


    def CalcPhi_V(self):
        self.phi_v = CosineAngle(self.Ylist1[-1],self.Zlist1[-1],2*self.v)
        

    def CalcPhi_V2(self):
        self.phi_v2 = CosineAngle(self.Zlist1[-1],self.Ylist1[-1],2*self.v)

    def CalcPhi_V3(self):
        self.phi_v3 = self.phi_v2

    def CalcPhi_V4(self):
        self.phi_v4 = self.phi_v


    def CalcPhi_V5(self):
        self.phi_v5 = CosineAngle(2*self.v,self.Ylist1[-1],self.Zlist1[-1])


        
    def CalcPhi_U(self):
        self.phi_u =  Atan(self.l5/self.u)


    def CalcPhi_U2(self):
        self.phi_u2 =  Atan(self.l3/self.u)


    def CalcPhi_U3(self):
        self.phi_u3 =  self.phi_u2

    def CalcPhi_U4(self):
        self.phi_u4 =  self.phi_u


        
    def CalcZ(self,n):
        return Decimal(math.sqrt( pow((self.u - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.vprime - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcY(self,n):
        return Decimal(math.sqrt( pow((self.u - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.vprime - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.hprime),2)))

    def CalcW(self,n):
        return self.CalcY(n)        #Since Yn  = Wn
    
    def CalcX(self,n):
        return self.CalcZ(n)        # since Zn = Xn


    def CalcMValues(self):
        self.CalcM()
        self.Mlist1  = []
        self.Mlist2 = []
        m = 0
        for i in range(self.n+1):
            if i == 0:
                m = 0
            else:
                m += self.M
            self.Mlist1.append(m)
        for i in range(self.n+1):
            self.Mlist2.append(self.Mlist1[-(i+1)])
        self.valuedict["M"] = self.Mlist1


    def CalcZValues(self):
        self.Zlist1 = []
        self.Zlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcZ(i))
            self.Zlist1.append(z)
        for i in range(self.n+1):
            self.Zlist2.append(self.Zlist1[-(i+1)])
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Z"] = self.Zlist1


    def CalcYValues(self):
        self.Ylist1 = []
        self.Ylist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcY(i))
            self.Ylist1.append(z)
        for i in range(self.n+1):
            self.Ylist2.append(self.Ylist1[-(i+1)])
        self.valuedict["Y"] = self.Ylist1


    def CalcWValues(self):
        self.Wlist1 = self.Ylist1
        self.Wlist2 = self.Ylist2
        self.valuedict["W"] = self.Wlist1


    def CalcXValues(self):
        self.Xlist1 = self.Zlist1
        self.Xlist2 = self.Zlist2
        self.valuedict["X"] = self.Xlist1


            

    def CalcDeltaAlpha(self,z1,z2):
        return   Acos(((pow(z1,2)) + \
                             (pow(z2,2)) - (pow((2*self.r*Sin(self.circleangle/2)),2)))/\
                             (2*z1*z2))
    


    def CalcTheta1(self):
        sum_delta = 0
        for i in range(len(self.Xlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1]),2)
        
        self.theta1 = 180 - Decimal((self.phi_v4 + sum_delta + self.phi_u4),2)

                            
            

    def CalcTheta2(self):
        sum_delta = 0
        for i in range(len(self.Wlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Wlist1[i],self.Wlist1[i+1]),2)
        
        self.theta2 = 180 - Decimal((self.phi_v3 + sum_delta + self.phi_u3),2)



    def CalcTheta3(self):
        sum_delta = 0
        for i in range(len(self.Ylist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Ylist2[i],self.Ylist2[i+1]),2)
        
        self.theta3 = 180 - Decimal((self.phi_v2 + sum_delta + self.phi_u2),2)



    def CalcTheta4(self):
        sum_delta = 0
        for i in range(len(self.Zlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Zlist1[i],self.Zlist1[i+1]),2)
        
        self.theta4 = 180 - Decimal((self.phi_v + sum_delta + self.phi_u),2)



        

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.line1 = self.Line()
        self.line1.Initialize4((self.a0,self.a1),self.length,0)
        
        
        self.line2 = self.Line()
        self.line2.Initialize5(self.line1.GetPoint2(),self.breadth,-self.theta3)
##
        
        self.line3 = self.Line()
        self.line3.Initialize5(self.line2.GetPoint2(),\
                  self.length,-(self.theta2 + self.theta3))

##
##        
##
        self.line4 = self.Line()
        self.line4.Initialize5(self.line3.GetPoint2(),\
                        self.u,-(self.theta3 + self.theta1 + self.theta2))
##        
##
        self.line5 = self.Line()
        self.line5.Initialize5(self.line4.GetPoint2(),\
                            self.l5,-(90 + self.theta3 + self.theta2 + self.theta1))
##
        self.line6 = self.Line()
        self.line6.Initialize5(self.line1.GetPoint1(),\
                        self.u, -(180 - self.theta4))
##
##        
        self.line7 = self.Line()
        self.line7.Initialize5(self.line6.GetPoint2(),\
                     self.l5,270 + self.theta4)
##
##
##
##
####
##
##
        self.line9= self.Line()
        self.line9.Initialize5(self.line2.GetPoint2(),\
                     self.Wlist1[-1],-(self.phi_v3 + self.theta2 + self.theta3))       
##
        self.line11= self.Line()
        self.line11.Initialize5(self.line1.GetPoint2(),\
                     self.Ylist1[0],-(self.theta2 + self.phi_u2))      
##
        self.line13= self.Line()
        self.line13.Initialize5(self.line1.GetPoint1(),\
                     self.Zlist1[-1],-self.phi_v)
##
        self.line14= self.Line()
        self.line14.Initialize5(self.line1.GetPoint1(),\
                     self.Zlist1[0],-(180-(self.theta4 + self.phi_u)))      
##
        self.line15= self.Line()
        self.line15.Initialize5(self.line3.GetPoint2(),\
                     self.Xlist1[0],-(self.phi_u4 +self.theta1 + self.theta2 + self.theta3))     
##        
##
        self.line8= self.Line()
        self.line8.Initialize2(self.line3.GetPoint2(),self.line9.GetPoint2())


        self.line10= self.Line()
        self.line10.Initialize2(self.line2.GetPoint2(),self.line11.GetPoint2())

        self.line12= self.Line()
        self.line12.Initialize2(self.line1.GetPoint2(),self.line13.GetPoint2())       
####
##        

        

##        # all main lines end here. from here we begin lines that
##        #may vary in number
        self.GenerateZlines()
        self.GenerateYlines()
        self.GenerateWlines()
        self.GenerateXlines()
##
        for i in range(len(self.Zlines)):
            for j in range(len(self.Zlines[0]) - 1):
                line = self.Line()
                line.Initialize2(self.Zlines[i][j].GetPoint2(),\
                                 self.Zlines[i][j+1].GetPoint2())
                line2 = self.Line()
                line2.Initialize2(self.Ylines[i][j].GetPoint2(),\
                                 self.Ylines[i][j+1].GetPoint2())
                line3 = self.Line()
                line3.Initialize2(self.Wlines[i][j].GetPoint2(),\
                                 self.Wlines[i][j+1].GetPoint2())

                line4 = self.Line()
                line4.Initialize2(self.Xlines[i][j].GetPoint2(),\
                                 self.Xlines[i][j+1].GetPoint2())
                
            


    def GenerateZlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line14)

        for i in range(len(self.Zlist1) - 1):
            sum_delta += self.CalcDeltaAlpha(self.Zlist1[i],self.Zlist1[i+1])
                                    
            angleinc = -(180 - (self.phi_u + self.theta4 + sum_delta))
            anglelist1.append(angleinc)

            line = self.Line(label = "Z%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint1(),\
                     self.Zlist1[i+1],angleinc)
            templinelist.append(line)
            
        templinelist.append(self.line13)

        self.Zlines.append(templinelist)


    def GenerateYlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line11)
        for i in range(len(self.Ylist1) - 1):
            sum_delta += self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1])
                                    
            angleinc =  - (self.theta3 +self.phi_u2 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "Y%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint2(),\
                     self.Ylist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line12)
        self.Ylines.append(templinelist)




    def GenerateWlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line9)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Wlist2) - 1):
            
            sum_delta += self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1])
                                    
            angleinc = - (self.phi_v3 + self.theta2 + self.theta3+sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "W%d"%(b - i),outline = 0)
            line.Initialize5(self.line2.GetPoint2(),\
                     self.Wlist2[i+1],angleinc)


            templinelist.append(line)
            
        templinelist.append(self.line10)
        self.Wlines.append(templinelist)



        
    def GenerateXlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line15)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Xlist1) - 1):
            sum_delta += self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1])
                                    
            angleinc = -(self.theta1 + self.theta2 + self.theta3 + self.phi_u4 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "X%d"%(b - i),outline = 0)

            line.Initialize5(self.line3.GetPoint2(),\
                     self.Xlist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line8)
        self.Xlines.append(templinelist)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Diameter"] = self.diameter
        self.dimensiondict["Bevel Length"] = self.length
        self.dimensiondict["Breadth"] = self.breadth
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n
        self.dimensiondict["Vertical Inclination"] = self.inclination
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetLength(values["Length"])
            if not self.stop:
                self.SetBreadth(values["Breadth"])
                if not self.stop:
                    self.SetHeight(values["Height"])
                    if not self.stop:
                        self.SetInclination(values["Inclination"])
                        if not self.stop:
                            self.SetFacetNumber(values["Facet number"])
            
    def SetLength(self,value):
        if value:
            try:
                self.length = float(value)
                if self.length <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Bevel Length"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Bevel Length")
    def SetDiameter(self,value):
        if value:
            try:

                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Diameter")


    def SetBreadth(self,value):
        if value:
            try:
                self.breadth = float(value)
                if self.breadth <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Breadth"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Breadth")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.ShowError("""Invalid Input "%s" for Facet Number"""% value)
            else:
                    
                if value2 > 10 or value2 < 3:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Facet Number\n valid range 3 to 10"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Facet Number")

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetInclination(self,value):
        if value:
            try:
                value2 = float(value)
            except ValueError:
                self.ShowError("""Invalid Input "%s" for Inclination to the vertical"""% value)
            else:
                    
                if abs(value2) > 90 or value2 <= 0:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Vertical Inclination\n valid range +0 to +90"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.inclination = value2
        else:
            self.stop = 1
            self.ShowError("No value for Vertical Inclination")

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def GetLinkerObject(self):
        return self.linkerobject
    def SetScale(self):
        self.linkerobject.SetScale(4,4)
    def SetErrorDialog(self,reference):
        self.errordialog = reference

#RectToRoundObliqueClass end
##########################################################################################            


#RectToRoundOff2Class begin
##########################################################################################            

class RectToRoundOff2:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        
        self.a0 = 400
        self.a1 = 500

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Zlines = []
        self.Ylines = []
        self.Wlines = []
        self.Xlines = []
        self.Zulines = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []
        

    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        self.parent.ShowResult1(\
            self.dimensiondict,\
            self.valuedict,\
            self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()



    def Calculate(self):
        self.circleangle = 90.0/float(self.n)

        self.v = self.length/2
        self.u = self.breadth/2
        self.r = self.diameter/2 #+ (self.thickness/2)
        # calculate L values
        self.CalcL1()
        self.CalcL2()
        self.CalcL3()
        self.CalcL4()
        

        
        self.CalcPhi_U()
        self.CalcPhi_U2()
        self.CalcPhi_U3()
        self.CalcPhi_U4()
        self.CalcPhi_V()
        self.CalcPhi_V2()
        self.CalcPhi_V3()
        self.CalcPhi_V4()

        self.CalcMValues()
        self.CalcZValues()
        self.CalcYValues()
        self.CalcWValues()
        self.CalcXValues()

        self.CalcTheta1()
        self.CalcTheta2()
        self.CalcTheta3()
        self.CalcTheta4()

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter / (4*self.n),2)
        
        
    def CalcL1(self):
        self.l1 = Decimal(math.sqrt(pow((self.u + self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L1"] = self.l1
    def CalcL2(self):
        self.l2 = Decimal(math.sqrt(pow((self.v - self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L2"] = self.l2

    def CalcL3(self):
        self.l3 = Decimal(math.sqrt(pow((self.v + self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L3"] = self.l3
        
    def CalcL4(self):
        self.l4 = Decimal(math.sqrt(pow((self.u - self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L4"] = self.l4


    def CalcPhi_V(self):
        self.phi_v = Atan(self.l1/(self.v + self.offsetx))


    def CalcPhi_V2(self):
        self.phi_v2 = Atan(self.l1/(self.v - self.offsetx))

    def CalcPhi_V3(self):
        self.phi_v3 = Atan(self.l4/(self.v - self.offsetx))

    def CalcPhi_V4(self):
        self.phi_v4 = Atan(self.l4/(self.v + self.offsetx))

        
    def CalcPhi_U(self):
        self.phi_u =  Atan(self.l2/(self.u + self.offsety))

    def CalcPhi_U2(self):
        self.phi_u2 =  Atan(self.l2/(self.u - self.offsety))

    def CalcPhi_U3(self):
        self.phi_u3 =  Atan(self.l3/(self.u + self.offsety))

    def CalcPhi_U4(self):
        self.phi_u4 =  Atan(self.l3/(self.u - self.offsety))

        


        
    def CalcZ(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcY(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcW(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))
    def CalcX(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))


    def CalcMValues(self):
        self.CalcM()
        self.Mlist1  = []
        self.Mlist2 = []
        m = 0
        for i in range(self.n+1):
            if i == 0:
                m = 0
            else:
                m += self.M
            self.Mlist1.append(m)
        for i in range(self.n):
            self.Mlist2.append(self.Mlist1[-(i+1)])
        self.valuedict["M"] = self.Mlist1
        



    def CalcZValues(self):
        self.Zlist1 = []
        self.Zlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcZ(i))
            self.Zlist1.append(z)
        for i in range(self.n+1):
            self.Zlist2.append(self.Zlist1[-(i+1)])
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Z"] = self.Zlist1


    def CalcYValues(self):
        self.Ylist1 = []
        self.Ylist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcY(i))
            self.Ylist1.append(z)
        for i in range(self.n+1):
            self.Ylist2.append(self.Ylist1[-(i+1)])
        self.valuedict["Y"] = self.Ylist1


    def CalcWValues(self):
        self.Wlist1 = []
        self.Wlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcW(i))
            self.Wlist1.append(z)
        for i in range(self.n+1):
            self.Wlist2.append(self.Wlist1[-(i+1)])
        self.valuedict["W"] = self.Wlist1


    def CalcXValues(self):
        self.Xlist1 = []
        self.Xlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcX(i))
            self.Xlist1.append(z)
        for i in range(self.n+1):
            self.Xlist2.append(self.Xlist1[-(i+1)])
        self.valuedict["X"] = self.Xlist1


            

    def CalcDeltaAlpha(self,z1,z2):
        return   Acos(((pow(z1,2)) + \
                             (pow(z2,2)) - (pow((2*self.r*Sin(self.circleangle/2)),2)))/\
                             (2*z1*z2))


    def CalcTheta1(self):
        sum_delta = 0
        for i in range(len(self.Xlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1]),2)
        
        self.theta1 = 180 - Decimal((self.phi_u4 + sum_delta + self.phi_v4),2)

                            
            

    def CalcTheta2(self):
        sum_delta = 0
        for i in range(len(self.Wlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1]),2)
        
        self.theta2 = 180 - Decimal((self.phi_v + sum_delta + self.phi_u3),2)


    def CalcTheta3(self):
        sum_delta = 0
        for i in range(len(self.Ylist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1]),2)
        
        self.theta3 = 180 - Decimal((self.phi_u + sum_delta + self.phi_v2),2)


    def CalcTheta4(self):
        sum_delta = 0
        for i in range(len(self.Zlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1]),2)
        
        self.theta4 = 180 - Decimal((self.phi_v3 + sum_delta + self.phi_u2),2)


        

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.line1 = self.Line(label = "length")
        self.line1.Initialize4((self.a0,self.a1),self.length,0)
        
        
        self.line2 = self.Line(label = "breadth")
        self.line2.Initialize5(self.line1.GetPoint2(),self.breadth,-self.theta2)

        
        self.line3 = self.Line()
        self.line3.Initialize5(self.line2.GetPoint2(),\
                  self.v + self.offsetx,-(self.theta1 + self.theta2))


        

        self.line4 = self.Line(label = "L4")
        self.line4.Initialize5(self.line3.GetPoint2(),\
                        self.l4,-(90 + self.theta1 + self.theta2))
        

        self.line5 = self.Line()
        self.line5.Initialize5(self.line1.GetPoint1(),\
                            self.breadth,180 + self.theta3)

        self.line6 = self.Line()
        self.line6.Initialize5(self.line5.GetPoint2(),\
                        self.v - self.offsetx, 180 + self.theta3 + self.theta4)

        
        self.line7 = self.Line(label = "L4")
        self.line7.Initialize5(self.line6.GetPoint2(),\
                     self.l4,270 + self.theta3 + self.theta4)


        self.line8 = self.Line(label = "L2")
        self.line8.Initialize4(\
            self.line5.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l2,270 + self.theta3) 



        self.line9= self.Line(label = "L1")
        self.line9.Initialize4((self.line1.Getx1()+self.v - self.offsetx,self.line1.Gety1()),\
                          self.l1,270)        

        self.line10= self.Line()
        self.line10.Initialize4(\
            self.line2.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l3,-(90+self.theta2))        

        self.line11= self.Line(label = "X%d"%(self.n),outline = 0)
        self.line11.Initialize2(self.line2.GetPoint2(),self.line4.GetPoint2())

        self.line12= self.Line(label = "X0",outline = 0)
        self.line12.Initialize2(self.line2.GetPoint2(),self.line10.GetPoint2())       
##
        self.line13 = self.Line(label = "W0",outline = 0)
        self.line13.Initialize2(self.line1.GetPoint2(),self.line10.GetPoint2())

        self.line14 = self.Line(label = "W%d"%(self.n),outline = 0)
        self.line14.Initialize2(self.line1.GetPoint2(),self.line9.GetPoint2())


        self.line15 = self.Line(label = "Y%d"%(self.n),outline = 0)
        self.line15.Initialize2(self.line1.GetPoint1(),self.line9.GetPoint2())
        
        
        self.line16 = self.Line(label = "Y0",outline = 0)
        self.line16.Initialize2(self.line1.GetPoint1(),self.line8.GetPoint2())
        

        
        self.line17 = self.Line(label = "Z0",outline = 0)
        self.line17.Initialize2(self.line5.GetPoint2(),self.line8.GetPoint2())


        self.line18 = self.Line(label = "Z%d"%(self.n),outline = 0)
        self.line18.Initialize2(self.line5.GetPoint2(),self.line7.GetPoint2())

        self.GenerateZlines()
        self.GenerateYlines()
        self.GenerateWlines()
        self.GenerateXlines()


        for i in range(len(self.Zlines)):
            for j in range(len(self.Zlines[0]) - 1):
                line = self.Line()
                line.Initialize2(self.Zlines[i][j].GetPoint2(),\
                                 self.Zlines[i][j+1].GetPoint2())
                line2 = self.Line()
                line2.Initialize2(self.Ylines[i][j].GetPoint2(),\
                                 self.Ylines[i][j+1].GetPoint2())
                line3 = self.Line()
                line3.Initialize2(self.Wlines[i][j].GetPoint2(),\
                                 self.Wlines[i][j+1].GetPoint2())

                line4 = self.Line()
                line4.Initialize2(self.Xlines[i][j].GetPoint2(),\
                                 self.Xlines[i][j+1].GetPoint2())
                


    def GenerateZlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line18)
        b = len(self.Zlist2) - 2

        for i in range(len(self.Zlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1])
                                    
            angleinc = -(180 - ((self.phi_v3 + self.theta3 + self.theta4) + sum_delta))
            anglelist1.append(angleinc)

            line = self.Line(label = "Z%d"%(b - i),outline = 0)
            line.Initialize5(self.line5.GetPoint2(),\
                     self.Zlist2[i+1],angleinc)
            templinelist.append(line)
            
        templinelist.append(self.line17)

        self.Zlines.append(templinelist)

    def GenerateYlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line16)
        for i in range(len(self.Ylist1) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1])
                                    
            angleinc = -(180  - ((self.theta3 + self.phi_u) + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "Y%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint1(),\
                     self.Ylist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line15)
        self.Ylines.append(templinelist)




    def GenerateWlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line14)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Wlist2) - 2):
            
            sum_delta += self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1])
                                    
            angleinc = -(180  - (self.phi_v + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "W%d"%(b - i),outline = 0)
            line.Initialize5(self.line1.GetPoint2(),\
                     self.Wlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line13)
        self.Wlines.append(templinelist)



        
    def GenerateXlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line11)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Xlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Xlist2[i],self.Xlist2[i+1])
                                    
            angleinc = -(self.theta1 + self.theta2 + self.phi_v4 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "X%d"%(b - i),outline = 0)

            line.Initialize5(self.line2.GetPoint2(),\
                     self.Xlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line12)
        self.Xlines.append(templinelist)

    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)

    def ReceiveInput(self):
        self.dimensiondict["Diameter"] = self.diameter
        self.dimensiondict["Length"] = self.length
        self.dimensiondict["Breadth"] = self.breadth
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n
        self.dimensiondict["Offset distance x"] = self.offsetx
        self.dimensiondict["Offset distance y"] = self.offsety

    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetLength(values["Length"])
            if not self.stop:
                self.SetBreadth(values["Breadth"])
                if not self.stop:
                    self.SetHeight(values["Height"])
                    if not self.stop:
                        self.SetOffsetx(values["Offset distance x"])
                        if not self.stop:
                            self.SetOffsety(values["Offset distance y"])
                            if not self.stop:
                                self.SetFacetNumber(values["Facet number"])

    def SetLength(self,value):
        if value:
            try:
                self.length = float(value)
                if self.length <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Length"""%value)
            else:
                self.stop = 0

        else:
            self.stop = 1
            self.ShowError("No Value in Length")
    def SetDiameter(self,value):
        if value:
            try:

                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Diameter"""%value)
            else:                
                self.stop = 0
                
        else:
            self.stop = 1
            self.ShowError("No Value in Diameter")


    def SetBreadth(self,value):
        if value:
            try:
                self.breadth = float(value)
                if self.breadth <= 0:
                    raise ValueError
                
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Breadth"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Breadth")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height"""%value)
            else:
                self.stop = 0
           
        else:
            self.stop = 1
            self.ShowError("No Value in Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Facet Number"""% value)
            else:
                    
                if value2 > 10 or value2 < 3:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Facet Number\n valid range 3 to 10"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Facet Number")

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetOffsetx(self,offset):
        if offset:
            try:
                offset2 = float(offset)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Offset distance x"""%offset)
            else:
                if abs(offset2) > (self.length/2):
                    self.stop = 1
                    self.ShowError("""Offset distance x %s is too large"""%str(offset2))
                else:
                    self.stop = 0
                    self.offsetx = offset2
                

        else:
            self.stop = 1
            self.ShowError("""No value in Offset distance x""")

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)
            
    def SetOffsety(self,offset):
        if offset:
            try:
                offset2 = float(offset)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Offset distance y"""%offset)
            else:
                if abs(offset2) > (self.length/2):
                    self.stop = 1
                    self.ShowError("""Offset distance y %s is too large """%str(offset2))
                else:
                    self.stop = 0
                    self.offsety = offset2
                

        else:
            self.stop = 1
            self.ShowError("""No value in Offset distance y""")


    
    def SetErrorDialog(self,reference):
        self.errordialog = reference

    def GetLinkerObject(self):
        return self.linkerobject
#RectToRoundOff2Class end
##########################################################################################            





#RectToRoundOff1Class begin
##########################################################################################            
class RectToRoundOff1:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()
        
        self.a0 = 400
        self.a1 = 500
        

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)


        
    def InitialiseCalcData(self):
        self.stop = 0
        self.Zlines = []
        self.Ylines = []
        self.Wlines = []
        self.Xlines = []
        self.Zulines = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []
        


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        self.parent.ShowResult1(\
            self.dimensiondict,\
            self.valuedict,\
            self.otherdict)

        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()
        
    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()



    def Calculate(self):
        self.circleangle = 90.0/float(self.n)

        self.v = self.length/2
        self.u = self.breadth/2
        self.r = self.diameter/2 #+ (self.thickness/2)
        # calculate L values
        self.CalcL1()
        self.CalcL2()
        self.CalcL3()
        self.CalcL4()

        
        self.CalcPhi_U()
        self.CalcPhi_U2()
        self.CalcPhi_U3()
        self.CalcPhi_U4()
        self.CalcPhi_V()
        self.CalcPhi_V2()
        self.CalcPhi_V3()
        self.CalcPhi_V4()

        self.CalcMValues()
        self.CalcZValues()
        self.CalcYValues()
        self.CalcWValues()
        self.CalcXValues()

        self.CalcTheta1()
        self.CalcTheta2()
        self.CalcTheta3()
        self.CalcTheta4()
        
    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter / (4*self.n),2)
        


    def CalcL1(self):
        self.l1 = Decimal(math.sqrt(pow((self.u + self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L1"] = self.l1
    def CalcL2(self):
        self.l2 = Decimal(math.sqrt(pow((self.v - self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L2"] = self.l2
    def CalcL3(self):
        self.l3 = Decimal(math.sqrt(pow((self.v + self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L3"] = self.l3
    def CalcL4(self):
        self.l4 = Decimal(math.sqrt(pow((self.u - self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L4"] = self.l4


    def CalcPhi_V(self):
        self.phi_v = Atan(self.l1/(self.v + self.offsetx))


    def CalcPhi_V2(self):
        self.phi_v2 = Atan(self.l1/(self.v - self.offsetx))

    def CalcPhi_V3(self):
        self.phi_v3 = Atan(self.l4/(self.v - self.offsetx))

    def CalcPhi_V4(self):
        self.phi_v4 = Atan(self.l4/(self.v + self.offsetx))

        
    def CalcPhi_U(self):
        self.phi_u =  Atan(self.l2/(self.u + self.offsety))

    def CalcPhi_U2(self):
        self.phi_u2 =  Atan(self.l2/(self.u - self.offsety))

    def CalcPhi_U3(self):
        self.phi_u3 =  Atan(self.l3/(self.u + self.offsety))

    def CalcPhi_U4(self):
        self.phi_u4 =  Atan(self.l3/(self.u - self.offsety))


        
    def CalcZ(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcY(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcW(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))
    def CalcX(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))


    def CalcMValues(self):
        self.CalcM()
        self.Mlist1  = []
        self.Mlist2 = []
        m = 0
        for i in range(self.n+1):
            if i == 0:
                m = 0
            else:
                m += self.M
            self.Mlist1.append(m)
        for i in range(self.n+1):
            self.Mlist2.append(self.Mlist1[-(i+1)])
        self.valuedict["M"] = self.Mlist1


    def CalcZValues(self):
        self.Zlist1 = []
        self.Zlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcZ(i))
            self.Zlist1.append(z)
        for i in range(self.n+1):
            self.Zlist2.append(self.Zlist1[-(i+1)])
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Z"] = self.Zlist1


    def CalcYValues(self):
        self.Ylist1 = []
        self.Ylist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcY(i))
            self.Ylist1.append(z)
        for i in range(self.n+1):
            self.Ylist2.append(self.Ylist1[-(i+1)])
        self.valuedict["Y"] = self.Ylist1


    def CalcWValues(self):
        self.Wlist1 = []
        self.Wlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcW(i))
            self.Wlist1.append(z)
        for i in range(self.n+1):
            self.Wlist2.append(self.Wlist1[-(i+1)])
        self.valuedict["W"] = self.Wlist1

    def CalcXValues(self):
        self.Xlist1 = []
        self.Xlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcX(i))
            self.Xlist1.append(z)
        for i in range(self.n+1):
            self.Xlist2.append(self.Xlist1[-(i+1)])
        self.valuedict["X"] = self.Xlist1


            

    def CalcDeltaAlpha(self,z1,z2):
        return   Acos(((pow(z1,2)) + \
                             (pow(z2,2)) - (pow((2*self.r*Sin(self.circleangle/2)),2)))/\
                             (2*z1*z2))


    def CalcTheta1(self):
        sum_delta = 0
        for i in range(len(self.Xlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1]),2)
        
        self.theta1 = 180 - Decimal((self.phi_u4 + sum_delta + self.phi_v4),2)

                            
            

    def CalcTheta2(self):
        sum_delta = 0
        for i in range(len(self.Wlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1]),2)
        
        self.theta2 = 180 - Decimal((self.phi_v + sum_delta + self.phi_u3),2)


    def CalcTheta3(self):
        sum_delta = 0
        for i in range(len(self.Ylist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1]),2)
        
        self.theta3 = 180 - Decimal((self.phi_u + sum_delta + self.phi_v2),2)


    def CalcTheta4(self):
        sum_delta = 0
        for i in range(len(self.Zlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1]),2)
        
        self.theta4 = 180 - Decimal((self.phi_v3 + sum_delta + self.phi_u2),2)


        

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.line1 = self.Line(label = "length")
        self.line1.Initialize4((self.a0,self.a1),self.length,0)
        
        
        self.line2 = self.Line(label = "breadth")
        self.line2.Initialize5(self.line1.GetPoint2(),self.breadth,-self.theta2)

        
        self.line3 = self.Line()
        self.line3.Initialize5(self.line2.GetPoint2(),\
                  self.v + self.offsetx,-(self.theta1 + self.theta2))


        

        self.line4 = self.Line(label = "L4")
        self.line4.Initialize5(self.line3.GetPoint2(),\
                        self.l4,-(90 + self.theta1 + self.theta2))
        

        self.line5 = self.Line()
        self.line5.Initialize5(self.line1.GetPoint1(),\
                            self.breadth,180 + self.theta3)

        self.line6 = self.Line()
        self.line6.Initialize5(self.line5.GetPoint2(),\
                        self.v - self.offsetx, 180 + self.theta3 + self.theta4)

        
        self.line7 = self.Line(label = "L4")
        self.line7.Initialize5(self.line6.GetPoint2(),\
                     self.l4,270 + self.theta3 + self.theta4)


        self.line8 = self.Line(label = "L2")
        self.line8.Initialize4(\
            self.line5.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l2,270 + self.theta3) 



        self.line9= self.Line(label = "L1")
        self.line9.Initialize4((self.line1.Getx1()+self.v - self.offsetx,self.line1.Gety1()),\
                          self.l1,270)        

        self.line10= self.Line()
        self.line10.Initialize4(\
            self.line2.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l3,-(90+self.theta2))        

        self.line11= self.Line(label = "X%d"%(self.n),outline = 0)
        self.line11.Initialize2(self.line2.GetPoint2(),self.line4.GetPoint2())

        self.line12= self.Line(label = "X0",outline = 0)
        self.line12.Initialize2(self.line2.GetPoint2(),self.line10.GetPoint2())       
##
        self.line13 = self.Line(label = "W0",outline = 0)
        self.line13.Initialize2(self.line1.GetPoint2(),self.line10.GetPoint2())

        self.line14 = self.Line(label = "W%d"%(self.n),outline = 0)
        self.line14.Initialize2(self.line1.GetPoint2(),self.line9.GetPoint2())


        self.line15 = self.Line(label = "Y%d"%(self.n),outline = 0)
        self.line15.Initialize2(self.line1.GetPoint1(),self.line9.GetPoint2())
        
        
        self.line16 = self.Line(label = "Y0",outline = 0)
        self.line16.Initialize2(self.line1.GetPoint1(),self.line8.GetPoint2())
        

        
        self.line17 = self.Line(label = "Z0",outline = 0)
        self.line17.Initialize2(self.line5.GetPoint2(),self.line8.GetPoint2())


        self.line18 = self.Line(label = "Z%d"%(self.n),outline = 0)
        self.line18.Initialize2(self.line5.GetPoint2(),self.line7.GetPoint2())

        self.GenerateZlines()
        self.GenerateYlines()
        self.GenerateWlines()
        self.GenerateXlines()


        for i in range(len(self.Zlines)):
            for j in range(len(self.Zlines[0]) - 1):
                line = self.Line()
                line.Initialize2(self.Zlines[i][j].GetPoint2(),\
                                 self.Zlines[i][j+1].GetPoint2())
                line2 = self.Line()
                line2.Initialize2(self.Ylines[i][j].GetPoint2(),\
                                 self.Ylines[i][j+1].GetPoint2())
                line3 = self.Line()
                line3.Initialize2(self.Wlines[i][j].GetPoint2(),\
                                 self.Wlines[i][j+1].GetPoint2())

                line4 = self.Line()
                line4.Initialize2(self.Xlines[i][j].GetPoint2(),\
                                 self.Xlines[i][j+1].GetPoint2())
                
            


    def GenerateZlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line18)
        b = len(self.Zlist2) - 2

        for i in range(len(self.Zlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1])
                                    
            angleinc = -(180 - ((self.phi_v3 + self.theta3 + self.theta4) + sum_delta))
            anglelist1.append(angleinc)

            line = self.Line(label = "Z%d"%(b - i),outline = 0)
            line.Initialize5(self.line5.GetPoint2(),\
                     self.Zlist2[i+1],angleinc)
            templinelist.append(line)
            
        templinelist.append(self.line17)

        self.Zlines.append(templinelist)


    def GenerateYlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line16)
        for i in range(len(self.Ylist1) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1])
                                    
            angleinc = -(180  - ((self.theta3 + self.phi_u) + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "Y%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint1(),\
                     self.Ylist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line15)
        self.Ylines.append(templinelist)





    def GenerateWlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line14)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Wlist2) - 2):
            
            sum_delta += self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1])
                                    
            angleinc = -(180  - (self.phi_v + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "W%d"%(b - i),outline = 0)
            line.Initialize5(self.line1.GetPoint2(),\
                     self.Wlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line13)
        self.Wlines.append(templinelist)


        
    def GenerateXlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line11)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Xlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Xlist2[i],self.Xlist2[i+1])
                                    
            angleinc = -(self.theta1 + self.theta2 + self.phi_v4 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "X%d"%(b - i),outline = 0)

            line.Initialize5(self.line2.GetPoint2(),\
                     self.Xlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line12)
        self.Xlines.append(templinelist)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)

    def ReceiveInput(self):
        yoffset = 0
        self.SetOffsety(yoffset)
        self.dimensiondict["Diameter"] = self.diameter
        self.dimensiondict["Length"] = self.length
        self.dimensiondict["Breadth"] = self.breadth
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n
        self.dimensiondict["Offset distance"] = self.offsetx

    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        
        if not self.stop:
            
            self.SetLength(values["Length"])
            if not self.stop:
                self.SetBreadth(values["Breadth"])
                if not self.stop:
                    self.SetHeight(values["Height"])
                    if not self.stop:
                        self.SetOffsetx(values["Offset distance"])
                        if not self.stop:
                            self.SetFacetNumber(values["Facet number"])


    def SetLength(self,value):
        if value:
            try:
                self.length = float(value)
                if self.length <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Length"""%value)
            else:
                self.stop = 0

        else:
            self.stop = 1
            self.ShowError("No Value in Length")
    def SetDiameter(self,value):
        if value:
            try:

                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Diameter"""%value)
            else:                
                self.stop = 0
                
        else:
            self.stop = 1
            self.ShowError("No Value in Diameter")


    def SetBreadth(self,value):
        if value:
            try:
                self.breadth = float(value)
                if self.breadth <= 0:
                    raise ValueError
                
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Breadth"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Breadth")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height"""%value)
            else:
                self.stop = 0
           
        else:
            self.stop = 1
            self.ShowError("No Value in Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)

            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Facet Number"""% value)
            else:
                    
                if value2 > 10 or value2 < 3:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Facet Number\n valid range 3 to 10"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Facet Number")

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetOffsetx(self,offset):
        if offset:
            try:
                offset2 = float(offset)
                
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Offset distance"""%offset)
            else:
                if abs(offset2) >=(self.length/2):
                    self.stop = 1
                    self.ShowError("""Offset distance %s too large"""%str(offset2))
                else:
                    self.stop = 0
                    self.offsetx = offset2
                

        else:
            self.stop = 1
            self.ShowError("""No value in Offset distance x""")

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)
            
 


    def SetOffsety(self,offset):
        self.offsety = offset



    def SetErrorDialog(self,reference):
        self.errordialog = reference

   
    def GetLinkerObject(self):
        return self.linkerobject

#RectToRoundOff1Class end
##########################################################################################            


#RectToRoundClass begin
##########################################################################################            
class RectToRound:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 400
        self.a1 = 500
        

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Zlines = []
        self.Ylines = []
        self.Wlines = []
        self.Xlines = []
        self.Zulines = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []



    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    

    def Calculate(self):
        self.circleangle = 90.0/float(self.n)

        self.v = self.length/2
        self.u = self.breadth/2
        self.r = self.diameter/2 #+ (self.thickness/2)
        # calculate L values
        self.CalcL1()
        self.CalcL2()
        self.CalcL3()
        self.CalcL4()
        

        
        self.CalcPhi_U()
        self.CalcPhi_U2()
        self.CalcPhi_U3()
        self.CalcPhi_U4()
        self.CalcPhi_V()
        self.CalcPhi_V2()
        self.CalcPhi_V3()
        self.CalcPhi_V4()

        self.CalcMValues()
        self.CalcZValues()
        self.CalcYValues()
        self.CalcWValues()
        self.CalcXValues()

        self.CalcTheta1()
        self.CalcTheta2()
        self.CalcTheta3()
        self.CalcTheta4()

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter / (4*self.n),2)
        


        
    def CalcL1(self):
        self.l1 = Decimal(math.sqrt(pow((self.u + self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L1"] = self.l1

    def CalcL2(self):
        self.l2 = Decimal(math.sqrt(pow((self.v - self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L2"] = self.l2
    def CalcL3(self):
        self.l3 = Decimal(math.sqrt(pow((self.v + self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L3"] = self.l3

    def CalcL4(self):
        self.l4 = Decimal(math.sqrt(pow((self.u - self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L4"] = self.l4



    def CalcPhi_V(self):
        self.phi_v = Atan(self.l1/(self.v + self.offsetx))


    def CalcPhi_V2(self):
        self.phi_v2 = Atan(self.l1/(self.v - self.offsetx))

    def CalcPhi_V3(self):
        self.phi_v3 = Atan(self.l4/(self.v - self.offsetx))

    def CalcPhi_V4(self):
        self.phi_v4 = Atan(self.l4/(self.v + self.offsetx))

        
    def CalcPhi_U(self):
        self.phi_u =  Atan(self.l2/(self.u + self.offsety))

    def CalcPhi_U2(self):
        self.phi_u2 =  Atan(self.l2/(self.u - self.offsety))

    def CalcPhi_U3(self):
        self.phi_u3 =  Atan(self.l3/(self.u + self.offsety))

    def CalcPhi_U4(self):
        self.phi_u4 =  Atan(self.l3/(self.u - self.offsety))


        
    def CalcZ(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcY(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcW(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))
    def CalcX(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))


    def CalcMValues(self):
        self.CalcM()
        self.Mlist1  = []
        self.Mlist2 = []
        m = 0
        for i in range(self.n+1):
            if i == 0:
                m = 0
            else:
                m += self.M
            self.Mlist1.append(m)
        for i in range(self.n+1):
            self.Mlist2.append(self.Mlist1[-(i+1)])
        self.valuedict["M"] = self.Mlist1


    def CalcZValues(self):
        self.Zlist1 = []
        self.Zlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcZ(i))
            self.Zlist1.append(z)
        for i in range(self.n+1):
            self.Zlist2.append(self.Zlist1[-(i+1)])
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Z"] = self.Zlist1


    def CalcYValues(self):
        self.Ylist1 = []
        self.Ylist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcY(i))
            self.Ylist1.append(z)
        for i in range(self.n+1):
            self.Ylist2.append(self.Ylist1[-(i+1)])
        self.valuedict["Y"] = self.Ylist1


    def CalcWValues(self):
        self.Wlist1 = []
        self.Wlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcW(i))
            self.Wlist1.append(z)
        for i in range(self.n+1):
            self.Wlist2.append(self.Wlist1[-(i+1)])
        self.valuedict["W"] = self.Wlist1

    def CalcXValues(self):
        self.Xlist1 = []
        self.Xlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcX(i))
            self.Xlist1.append(z)
        for i in range(self.n+1):
            self.Xlist2.append(self.Xlist1[-(i+1)])
        self.valuedict["X"] = self.Xlist1


            

    def CalcDeltaAlpha(self,z1,z2):
        return   Acos(((pow(z1,2)) + \
                             (pow(z2,2)) - (pow((2*self.r*Sin(self.circleangle/2)),2)))/\
                             (2*z1*z2))


    def CalcTheta1(self):
        sum_delta = 0
        for i in range(len(self.Xlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1]),2)
        
        self.theta1 = 180 - Decimal((self.phi_u4 + sum_delta + self.phi_v4),2)

                            
            

    def CalcTheta2(self):
        sum_delta = 0
        for i in range(len(self.Wlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1]),2)
        
        self.theta2 = 180 - Decimal((self.phi_v + sum_delta + self.phi_u3),2)


    def CalcTheta3(self):
        sum_delta = 0
        for i in range(len(self.Ylist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1]),2)
        
        self.theta3 = 180 - Decimal((self.phi_u + sum_delta + self.phi_v2),2)


    def CalcTheta4(self):
        sum_delta = 0
        for i in range(len(self.Zlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1]),2)
        
        self.theta4 = 180 - Decimal((self.phi_v3 + sum_delta + self.phi_u2),2)


        

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.line1 = self.Line(label = "length")
        self.line1.Initialize4((self.a0,self.a1),self.length,0)
        
        
        self.line2 = self.Line(label = "breadth")
        self.line2.Initialize5(self.line1.GetPoint2(),self.breadth,-self.theta2)

        
        self.line3 = self.Line()
        self.line3.Initialize5(self.line2.GetPoint2(),\
                  self.v + self.offsetx,-(self.theta1 + self.theta2))


        

        self.line4 = self.Line(label = "L4")
        self.line4.Initialize5(self.line3.GetPoint2(),\
                        self.l4,-(90 + self.theta1 + self.theta2))
        

        self.line5 = self.Line()
        self.line5.Initialize5(self.line1.GetPoint1(),\
                            self.breadth,180 + self.theta3)

        self.line6 = self.Line()
        self.line6.Initialize5(self.line5.GetPoint2(),\
                        self.v - self.offsetx, 180 + self.theta3 + self.theta4)

        
        self.line7 = self.Line(label = "L4")
        self.line7.Initialize5(self.line6.GetPoint2(),\
                     self.l4,270 + self.theta3 + self.theta4)


        self.line8 = self.Line(label = "L2")
        self.line8.Initialize4(\
            self.line5.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l2,270 + self.theta3) 



        self.line9= self.Line(label = "L1")
        self.line9.Initialize4((self.line1.Getx1()+self.v - self.offsetx,self.line1.Gety1()),\
                          self.l1,270)        

        self.line10= self.Line()
        self.line10.Initialize4(\
            self.line2.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l3,-(90+self.theta2))        

        self.line11= self.Line(label = "X%d"%(self.n),outline = 0)
        self.line11.Initialize2(self.line2.GetPoint2(),self.line4.GetPoint2())

        self.line12= self.Line(label = "X0",outline = 0)
        self.line12.Initialize2(self.line2.GetPoint2(),self.line10.GetPoint2())       
##
        self.line13 = self.Line(label = "W0",outline = 0)
        self.line13.Initialize2(self.line1.GetPoint2(),self.line10.GetPoint2())

        self.line14 = self.Line(label = "W%d"%(self.n),outline = 0)
        self.line14.Initialize2(self.line1.GetPoint2(),self.line9.GetPoint2())


        self.line15 = self.Line(label = "Y%d"%(self.n),outline = 0)
        self.line15.Initialize2(self.line1.GetPoint1(),self.line9.GetPoint2())
        
        
        self.line16 = self.Line(label = "Y0",outline = 0)
        self.line16.Initialize2(self.line1.GetPoint1(),self.line8.GetPoint2())
        

        
        self.line17 = self.Line(label = "Z0",outline = 0)
        self.line17.Initialize2(self.line5.GetPoint2(),self.line8.GetPoint2())


        self.line18 = self.Line(label = "Z%d"%(self.n),outline = 0)
        self.line18.Initialize2(self.line5.GetPoint2(),self.line7.GetPoint2())

        self.GenerateZlines()
        self.GenerateYlines()
        self.GenerateWlines()
        self.GenerateXlines()


        for i in range(len(self.Zlines)):
            for j in range(len(self.Zlines[0]) - 1):
                line = self.Line()
                line.Initialize2(self.Zlines[i][j].GetPoint2(),\
                                 self.Zlines[i][j+1].GetPoint2())
                line2 = self.Line()
                line2.Initialize2(self.Ylines[i][j].GetPoint2(),\
                                 self.Ylines[i][j+1].GetPoint2())
                line3 = self.Line()
                line3.Initialize2(self.Wlines[i][j].GetPoint2(),\
                                 self.Wlines[i][j+1].GetPoint2())

                line4 = self.Line()
                line4.Initialize2(self.Xlines[i][j].GetPoint2(),\
                                 self.Xlines[i][j+1].GetPoint2())
                
            


    def GenerateZlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line18)
        b = len(self.Zlist2) - 2

        for i in range(len(self.Zlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1])
                                    
            angleinc = -(180 - ((self.phi_v3 + self.theta3 + self.theta4) + sum_delta))
            anglelist1.append(angleinc)

            line = self.Line(label = "Z%d"%(b - i),outline = 0)
            line.Initialize5(self.line5.GetPoint2(),\
                     self.Zlist2[i+1],angleinc)
            templinelist.append(line)
            
        templinelist.append(self.line17)

        self.Zlines.append(templinelist)


    def GenerateYlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line16)
        for i in range(len(self.Ylist1) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1])
                                    
            angleinc = -(180  - ((self.theta3 + self.phi_u) + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "Y%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint1(),\
                     self.Ylist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line15)
        self.Ylines.append(templinelist)




    def GenerateWlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line14)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Wlist2) - 2):
            
            sum_delta += self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1])
                                    
            angleinc = -(180  - (self.phi_v + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "W%d"%(b - i),outline = 0)
            line.Initialize5(self.line1.GetPoint2(),\
                     self.Wlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line13)
        self.Wlines.append(templinelist)



        
    def GenerateXlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line11)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Xlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Xlist2[i],self.Xlist2[i+1])
                                    
            angleinc = -(self.theta1 + self.theta2 + self.phi_v4 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "X%d"%(b - i),outline = 0)

            line.Initialize5(self.line2.GetPoint2(),\
                     self.Xlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line12)
        self.Xlines.append(templinelist)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)

    def ReceiveInput(self):
        xoffset = 0#75 #float(raw_input("Enter the xoffset distance: "))
        yoffset = 0#75  #float(raw_input("Enter the yoffset distance: "))
        self.SetOffsetx(xoffset)
        self.SetOffsety(yoffset)
        self.dimensiondict["Diameter"] = self.diameter
        self.dimensiondict["Length"] = self.length
        self.dimensiondict["Breadth"] = self.breadth
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n
        
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetLength(values["Length"])
            if not self.stop:
                self.SetBreadth(values["Breadth"])
                if not self.stop:
                    self.SetHeight(values["Height"])
                    if not self.stop:
                        self.SetFacetNumber(values["Facet number"])
        

    def SetLength(self,value):
        if value:
            try:
                self.length = float(value)
                if self.length <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Length"""%value)
            else:
                self.stop = 0

        else:
            self.stop = 1
            self.ShowError("No Value in Length")
    def SetDiameter(self,value):
        if value:
            try:

                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Diameter"""%value)
            else:                
                self.stop = 0
                
        else:
            self.stop = 1
            self.ShowError("No Value in Diameter")


    def SetBreadth(self,value):
        if value:
            try:
                self.breadth = float(value)
                if self.breadth <= 0:
                    raise ValueError
                
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Breadth"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Breadth")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height"""%value)
            else:
                self.stop = 0
           
        else:
            self.stop = 1
            self.ShowError("No Value in Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Facet Number"""% value)
            else:
                    
                if value2 > 10 or value2 < 3:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Facet Number\n valid range 3 to 10"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Facet Number")

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)
            
    def SetOffsetx(self,offset):
        self.offsetx = offset
    def SetOffsety(self,offset):
        self.offsety = offset
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject

#RectToRoundClass end
##########################################################################################            

########################################################################
######################################################################## BEGINING OF INTERPENETRATION PIECE
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

#TJunctionClass begin
################################################################    
class TJunction:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.5
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Llines = []
        self.Mlines = []


        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle
        
        self.R = self.diameter1 / 2   # Intersected Pipe R         
        self.r = self.diameter2 / 2   # Intersecting Pipe r
        # calculate L values

        self.CalcM()
        self.CalcHValues()
        self.CalcL0()
        if not self.stop:
            self.CalcLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.stop = 0
        self.l0 = self.height
        
    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter2 / self.n)


    def CalcH(self,n):
        return self.R - math.sqrt(pow(self.R,2) - pow((self.r * Sin(n * self.circleangle)),2))

    def CalcHValues(self):
        self.Hlist1 = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH(i))
            else:
                h = Decimal(self.CalcH(0))
            self.Hlist1.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn"] = self.Hlist1

    def CalcLValues(self):
        self.Llist1 = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1


      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.GenerateMlines()
        self.GenerateLlines()
        self.GenerateCurve()

    def GenerateMlines(self):
        self.mlinelist = []
        line0 = self.Line(label = "M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelist.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "M%d"%(i+1))
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)

    def GenerateLlines(self):
        self.linelist = [] # stores all the L lines
        for i in range(0,self.n+1):
            line2 = self.Line(label = "L%d"%i)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],-90)
            self.linelist.append(line2)

                    
    def GenerateCurve(self):
        self.curvelist = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i - 1].GetPoint2(),self.linelist[i].GetPoint2())
            self.curvelist.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)



    def ReceiveInput(self):
        self.dimensiondict["Interpenetrating pipe Diameter"] = self.diameter2 #r
        self.dimensiondict["Interpenetrated pipe Diameter"] = self.diameter1 #R
        self.dimensiondict["Free Height of Interpenetrating pipe"] = self.height
        self.dimensiondict["Partition Number"] = self.n

    def SetInput(self,values):
        self.SetDiameter2(values ["Diameter2"])
        if not self.stop:
            self.SetDiameter1(values["Diameter1"])
            if not self.stop:
                self.SetHeight(values["Height"])
                if not self.stop:
                    self.SetFacetNumber(values["Number"])


    def SetDiameter1(self,value):
        if value:
            try:
                self.diameter1 = float(value)
                if self.diameter1 <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrated pipe Diameter"""%value)
            else:
                if self.diameter2 > self.diameter1:
                    self.stop = 1
                    self.ShowError(\
        """Interpenetrated pipe Diameter is small. It should be greater than the Interpenetrating pipe Diameter""")
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrated pipe Diameter")


    def SetDiameter2(self,value):
        if value:
            try:
                self.diameter2 = float(value)
                if self.diameter2 <= 0 :
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrating pipe Diameter"""%value)
            else:
               
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrating pipe Diameter")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height Interpenetrating pipe"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Free Height of Interpenetrating pipe")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 12:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 12"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Partition Number")






    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject
#TJunctionClass end
############################################



#SquareToCylinderClass begin
########################################################    
class SquareToCylinder:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.5
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Llines = []
        self.Mlines = []


        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle
        
        self.R = self.diameter1 / 2   # Intersected Pipe R         
        # calculate L values
        self.CalcM()
        self.CalcHValues()
        self.CalcL0()
        if not self.stop:
            self.CalcLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.stop = 0
        self.l0 = self.height

    def CalcM(self):
        self.M = Decimal(self.length / self.n)


    def CalcH(self,n):
        return self.R - math.sqrt(pow(self.R,2) - (0.5*pow((n * self.length/self.n),2)))

    def CalcHValues(self):
        self.Hlist1 = []
        self.Hlist2 = []
        for i in range(self.n+1):

            h = Decimal(self.CalcH(i))
            self.Hlist1.append(h)
        self.valuedict["N"] = range((self.n*4)+1)
        for i in range(1,self.n+1):
            self.Hlist2.append(self.Hlist1[-(i+1)])
        self.Hlist1 = self.Hlist1 + self.Hlist2[:]
        self.Hlist3 = self.Hlist1[1:(self.n*2)+1]
        self.Hlist1 = self.Hlist1 + self.Hlist3[:]
        self.Hlist2 = None
        self.Hlist3 = None
        self.valuedict["Hn"] = self.Hlist1

    def CalcLValues(self):
        self.Llist1 = []
        for i in range(len(self.Hlist1)):
            l = self.l0 + self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n*4):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1
      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.GenerateMlines()
        self.GenerateLlines()
        self.GenerateCurve()

    def GenerateMlines(self):
        self.mlinelist = []
        line0 = self.Line(label = "M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelist.append(line0)
        for i in range(len(self.Mlist1)-1):
            line1 = self.Line(label = "M%d"%(i+1))
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)
        

    def GenerateLlines(self):
        self.linelist = [] # stores all the L lines
        for i in range(len(self.Hlist1)):
            line2 = self.Line(label = "L%d"%i)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],-90)
            self.linelist.append(line2)

                    
    def GenerateCurve(self):
        self.curvelist = []
        for i in range(len(self.Hlist1)-1):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i].GetPoint2(),self.linelist[i+1].GetPoint2())
            self.curvelist.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Interpenetrating square pipe length"] = self.length #r
        self.dimensiondict["Interpenetrated pipe Diameter"] = self.diameter1 #R
        self.dimensiondict["Free Height of Interpenetrating pipe"] = self.height
        self.dimensiondict["Partition Number"] = self.n

    def SetInput(self,values):
        self.SetLength(values ["Length"])
        if not self.stop:
            self.SetDiameter1(values["Diameter1"])
            if not self.stop:
                self.SetHeight(values["Height"])
                if not self.stop:
                    self.SetFacetNumber(values["Number"])


    def SetDiameter1(self,value):
        if value:
            try:
                self.diameter1 = float(value)
                if self.diameter1 <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrated pipe Diameter"""%value)
            else:
                b = self.length * math.sqrt(2)
                if b > self.diameter1:
                    self.stop = 1
                    self.ShowError(\
        """Interpenetrated pipe Diameter is small. It should be greater than 1.4142 times the Interpenetrating pipe Diameter""")
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrated pipe Diameter")


    def SetLength(self,value):
        if value:
            try:
                self.length = float(value)
                if self.length <= 0 :
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrating square pipe Length"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrating square pipe Length")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height of Interpenetrating pipe"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Height of Interpenetrating pipe")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 2:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 2"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Partition Number")


    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject
#SquareToCylinderClass end
##############################################


#CylindricalPipeAtAnyAngle begin
##################################################    
class CylindricalPipeAtAnyAngle:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Llines = []
        self.Mlines = []


        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle
        
        self.diameter1m = self.diameter1 #+(self.thickness/2) # Intersected Pipe R         
        self.diameter2m = self.diameter2 #+ (self.thickness/2)# Intersecting Pipe r
        # calculate L values
        
        self.CalcM()
        self.CalcHValues()
        self.CalcL0()
        if not self.stop:
            self.CalcLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.l0 = self.height
        self.stop = 0

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter2m / self.n)


    def CalcH(self,n):
        return 0.5*(((self.diameter1m - \
            math.sqrt(pow(self.diameter1m,2) - pow((self.diameter2m * Sin(n * self.circleangle)),2)))*\
            Cosec(self.intersectionangle)) + (self.diameter2m * (1 - Cos(n* self.circleangle))*Cot(self.intersectionangle)))

    def CalcHValues(self):
        self.Hlist1 = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH(i))
            else:
                h = Decimal(self.CalcH(0))
            self.Hlist1.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn"] = self.Hlist1

    def CalcLValues(self):
        self.Llist1 = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1




            
      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.GenerateMlines()
        self.GenerateLlines()
        self.GenerateCurve()

    def GenerateMlines(self):
        self.mlinelist = []
        line0 = self.Line(label = "M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelist.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "M%d"%(i+1))
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)

    def GenerateLlines(self):
        self.linelist = [] # stores all the L lines
        for i in range(0,self.n+1):
            line2 = self.Line(label = "L%d"%i)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],-90)
            self.linelist.append(line2)

##        line2 = self.Line(label = "L%d"%(self.n))
##        line2.Initialize5(self.mlinelist[self.n - 1].GetPoint2(),self.Llist1[0],-90)
##        self.linelist.append(line2)

                    
    def GenerateCurve(self):
        self.curvelist = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i - 1].GetPoint2(),self.linelist[i].GetPoint2())
            self.curvelist.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)



    def ReceiveInput(self):
        self.dimensiondict["Interpenetrating pipe Diameter"] = self.diameter2 #r
        self.dimensiondict["Angle of Interpenetration"] = self.intersectionangle
        self.dimensiondict["Interpenetrated pipe Diameter"] = self.diameter1 #R
        self.dimensiondict["Free Height of Interpenetrating pipe"] = self.height
        self.dimensiondict["Partition Number"] = self.n

    def SetInput(self,values):
        self.SetDiameter2(values ["Diameter2"])
        if not self.stop:
            self.SetIntersectionAngle(values["Angle"])
            if not self.stop:
                self.SetDiameter1(values["Diameter1"])
                if not self.stop:
                    self.SetHeight(values["Height"])
                    if not self.stop:
                        self.SetFacetNumber(values["Number"])


    def SetDiameter1(self,value):
        if value:
            try:
                self.diameter1 = float(value)
                if self.diameter1 <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrated pipe Diameter"""%value)
            else:
                if self.diameter2 > self.diameter1:
                    self.stop = 1
                    self.ShowError(\
        """Interpenetrated pipe Diameter is small. It should be greater than the Interpenetrating pipe Diameter""")
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrated pipe Diameter")


    def SetDiameter2(self,value):
        if value:
            try:
                self.diameter2 = float(value)
                if self.diameter2 <= 0 :
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrating pipe Diameter"""%value)
            else:
               
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrating pipe Diameter")


    def SetIntersectionAngle(self,value):
        if value:
            try:
                self.intersectionangle = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Angle of Interpenetration"""%value)
            else:
                if self.intersectionangle <= 0 or self.intersectionangle > 90:
                    self.stop = 1
                    self.ShowError(\
"""Invalid input "%s" for Angle of Interpenetration.\nAngle of Interpenetration must be greater than 0 and less than or equal to 90 """%\
self.intersectionangle)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Angle of Interpenetration")






    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of Interpenetrating pipe"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Height of Free Height of Interpenetrating pipe")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 12:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 12"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Partition Number")






    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject

#CylindricalPipeAtAnyAngle end
##################################################    

#YJunctionPieceClass begin
##################################################    
class YJunctionPiece:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Llines = []
        self.Mlines = []


        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle
        
        self.diameter1m = self.diameter #+(self.thickness/2) # Intersected Pipe R
        self.R = self.diameter1m/2
        # calculate L values
        
        self.CalcM()
        self.CalcHValuesA()
        self.CalcHValuesB1()
        self.CalcHValuesB2()
        self.CalcL0()
        if not self.stop:
            self.CalcL1()
            if not self.stop:
                self.CalcL2()
                if not self.stop:                    
                    self.CalcLValuesA()
                    self.CalcLValuesB1()
                    self.CalcLValuesB2()
                    self.CalcMValues()

        
    def CalcL0(self):
        self.l0 = self.height0
        self.stop = 0

    def CalcL1(self):
        self.l1 = self.height1
        self.stop = 0

    def CalcL2(self):
        self.l2 = self.height2
        self.stop = 0
        
        

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter1m / self.n)


    def CalcH0(self,n):
        return self.R * (1 -  math.sqrt(pow(Cos(n * self.circleangle),2))) * Tan(self.intersectionangle1/2)

    def CalcH10(self,n): # B1 formular1 bwn 90<= theta <= 270
        return self.R * (Cot(self.intersectionangle1) - \
                         (math.sqrt(pow(Cos(n * self.circleangle),2)) *\
                         Tan(self.intersectionangle1/2)))
    
    def CalcH11(self,n):# B1 formular2 0 <= theta < 90 and 270< theta <= 360
        return self.R * (1 -  (Cos(n * self.circleangle))) * Cot(self.intersectionangle1)
##
    
    def CalcH20(self,n): #B2 formular1 90<= theta <= 270
        return self.R * (Cot(self.intersectionangle2) - \
                         (math.sqrt(pow(Cos(n * self.circleangle),2)) *\
                         Tan(self.intersectionangle2/2)))

    def CalcH21(self,n): #b2 formular2 90<=theta<=270
        return self.R * (1 -  (Cos(n * self.circleangle))) * Cot(self.intersectionangle2)
##

    def CalcHValuesA(self):
        self.Hlist1A = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH0(i))
            else:
                h = Decimal(self.CalcH0(0))
            self.Hlist1A.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn-A"] = self.Hlist1A

    def CalcHValuesB1(self):
        self.Hlist1B1 = []
        for i in range(self.n+1):
            b = i * self.circleangle
            if  b >= 90 and b <= 270 :
                h = Decimal(self.CalcH10(i))
            else:
                h = Decimal(self.CalcH11(i))
            self.Hlist1B1.append(h)
        self.valuedict["Hn-B1"] = self.Hlist1B1

    def CalcHValuesB2(self):
        self.Hlist1B2 = []
        for i in range(self.n+1):
            b = i * self.circleangle
            if  b >= 90 and b <= 270 :
                h = Decimal(self.CalcH20(i))
            else:
                h = Decimal(self.CalcH21(i))
            self.Hlist1B2.append(h)
        self.valuedict["Hn-B2"] = self.Hlist1B2


    def CalcLValuesA(self):
        self.Llist1A = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist1A[i]
            self.Llist1A.append(l)
        self.valuedict["Ln-A"] = self.Llist1A

    def CalcLValuesB1(self):
        self.Llist1B1 = []
        for i in range(self.n+1):
            l = self.l1 + self.Hlist1B1[i]
            self.Llist1B1.append(l)
        self.valuedict["Ln-B1"] = self.Llist1B1
        self.max_lvalue1 = max(self.Llist1B1)
        
    def CalcLValuesB2(self):
        self.Llist1B2 = []
        for i in range(self.n+1):
            l = self.l2 + self.Hlist1B2[i]
            self.Llist1B2.append(l)
        self.valuedict["Ln-B2"] = self.Llist1B2
        self.max_lvalue2 = max(self.Llist1B2)

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1


            
      

    def Draw(self):
        self.DrawMainLinesA()
        self.DrawMainLinesB1()
        self.DrawMainLinesB2()



    def DrawMainLinesA(self):
        self.GenerateMlinesA()
        self.GenerateLlinesA()
        self.GenerateCurveA()

    def DrawMainLinesB1(self):
        self.GenerateMlinesB1()
        self.GenerateLlinesB1()
        self.GenerateCurveB1()

    def DrawMainLinesB2(self):
        self.GenerateMlinesB2()
        self.GenerateLlinesB2()
        self.GenerateCurveB2()


    def GenerateMlinesA(self):
        self.mlinelistA = []
        line0 = self.Line(label = "A-M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelistA.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "A-M%d"%(i+1))
            line1.Initialize5(self.mlinelistA[i].GetPoint2(), self.M,0)
            self.mlinelistA.append(line1)

    def GenerateMlinesB1(self):
        self.mlinelistB1 = []
        line0 = self.Line(label = "B1-M0")
        line0.Initialize4((self.a0,self.a1 + self.max_lvalue1 + self.l1),0,0)
        self.mlinelistB1.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "B1-M%d"%(i+1))
            line1.Initialize5(self.mlinelistB1[i].GetPoint2(), self.M,0)
            self.mlinelistB1.append(line1)

    def GenerateMlinesB2(self):
        self.mlinelistB2 = []
        line0 = self.Line(label = "B2-M0")
        line0.Initialize4((self.mlinelistB1[0].Getx1(),self.mlinelistB1[0].Gety1() + self.max_lvalue2 + self.l2),0,0)
        self.mlinelistB2.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "B2-M%d"%(i+1))
            line1.Initialize5(self.mlinelistB2[i].GetPoint2(), self.M,0)
            self.mlinelistB2.append(line1)


    def GenerateLlinesA(self):
        self.linelistA = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0  
            else:
                outline = 1
            line2 = self.Line(label = "A-L%d"%i,outline = outline)
            line2.Initialize5(self.mlinelistA[i].GetPoint2(),self.Llist1A[i],-90)
            self.linelistA.append(line2)


    def GenerateLlinesB1(self):
        self.linelistB1 = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0  
            else:
                outline = 1
            line2 = self.Line(label = "B1-L%d"%i,outline = outline)
            line2.Initialize5(self.mlinelistB1[i].GetPoint2(),self.Llist1B1[i],-90)
            self.linelistB1.append(line2)

    def GenerateLlinesB2(self):
        self.linelistB2 = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0  
            else:
                outline = 1
            line2 = self.Line(label = "B2-L%d"%i,outline = outline)
            line2.Initialize5(self.mlinelistB2[i].GetPoint2(),self.Llist1B2[i],-90)
            self.linelistB2.append(line2)

                    
    def GenerateCurveA(self):
        self.curvelistA = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelistA[i - 1].GetPoint2(),self.linelistA[i].GetPoint2())
            self.curvelistA.append(line3)

    def GenerateCurveB1(self):
        self.curvelistB1 = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelistB1[i - 1].GetPoint2(),self.linelistB1[i].GetPoint2())
            self.curvelistB1.append(line3)

    def GenerateCurveB2(self):
        self.curvelistB2 = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelistB2[i - 1].GetPoint2(),self.linelistB2[i].GetPoint2())
            self.curvelistB2.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Junction Piece Diameter"] = self.diameter #R
        self.dimensiondict["Free Height of pipe A"] = self.height0
        self.dimensiondict["Angle of Intersection for pipe B1"] = self.intersectionangle1
        self.dimensiondict["Free Height of pipe B1"] = self.height1
        self.dimensiondict["Angle of Intersection for pipe B2"] = self.intersectionangle2
        self.dimensiondict["Free Height of pipe B2"] = self.height2
        self.dimensiondict["Partition Number"] = self.n

    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetHeight0(values['Height0'])
            if not self.stop:
                self.SetIntersectionAngleB1(values["Angle B1"])
                if not self.stop:
                    self.SetHeight1(values['Height1'])
                    if not self.stop:
                        self.SetIntersectionAngleB2(values["Angle B2"])
                        if not self.stop:
                            self.SetHeight2(values["Height2"])
                            if not self.stop:
                                self.SetFacetNumber(values["Number"])


    def SetDiameter(self,value):
        if value:
            try:
                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Junction Piece Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Junction Piece Diameter")



    def SetIntersectionAngleB1(self,value):
        if value:
            try:
                self.intersectionangle1 = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Angle of Intersection for pipe B1"""%value)
            else:
                if self.intersectionangle1 <= 0 or self.intersectionangle1 > 90:
                    self.stop = 1
                    self.ShowError(\
                                """Invalid input "%s" for Angle of Intersection for pipe B1.
                                   Angle of Intersection must be greater than 0
                                   and less than or equal to 90 """%\
                                               self.intersectionangle1)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Angle of Intersection")


    def SetIntersectionAngleB2(self,value):
        if value:
            try:
                self.intersectionangle2 = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Angle of Intersection for pipe B2"""%value)
            else:
                if self.intersectionangle2 <= 0 or self.intersectionangle2 > 90:
                    self.stop = 1
                    self.ShowError(\
                                """Invalid input "%s" for Angle of Intersection for pipe B2.
                                   Angle of Intersection must be greater than 0
                                   and less than or equal to 90 """%\
                                               self.intersectionangle2)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Angle of Intersection for pipe B2")



    def SetHeight0(self,value):
        if value:
            try:
                self.height0 = float(value)
                if self.height0 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of pipe A"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Free Height of pipe A")


    def SetHeight1(self,value):
        if value:
            try:
                self.height1 = float(value)
                if self.height1 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of pipe B1"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Free Height of pipe B1")


    def SetHeight2(self,value):
        if value:
            try:
                self.height2 = float(value)
                if self.height2 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of pipe B2"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Free Height of pipe B2")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 12:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 12"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Partition Number")






    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject

#YJunctionPieceClass end
##################################################################    


#CylinderCutAtAnyClass begin
##################################################    
class CylinderCutAtAny:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Llines = []
        self.Mlines = []


        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle
        
        self.diameterm = self.diameter #+(self.thickness/2) # Cylinder R         
        # calculate L values
        
        self.CalcM()
        self.CalcHValues()
        self.CalcL0()
        if not self.stop:
            self.CalcLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.stop = 0
        self.l0 = self.height 

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameterm / self.n)


    def CalcH(self,n):
        return (self.diameterm /2)*(1 - (Cos(n*self.circleangle)))*Tan(self.intersectionangle)

    def CalcHValues(self):
        self.Hlist1 = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH(i))
            else:
                h = Decimal(self.CalcH(0))
            self.Hlist1.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn"] = self.Hlist1

    def CalcLValues(self):
        self.Llist1 = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1

      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.GenerateMlines()
        self.GenerateLlines()
        self.GenerateCurve()

    def GenerateMlines(self):
        self.mlinelist = []
        line0 = self.Line(label = "M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelist.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "M%d"%(i+1))
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)

    def GenerateLlines(self):
        self.linelist = [] # stores all the L lines
        for i in range(0,self.n+1):
            line2 = self.Line(label = "L%d"%i)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],-90)
            self.linelist.append(line2)


                    
    def GenerateCurve(self):
        self.curvelist = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i - 1].GetPoint2(),self.linelist[i].GetPoint2())
            self.curvelist.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)



    def ReceiveInput(self):
        self.dimensiondict["Cylinder Diameter"] = self.diameter
        self.dimensiondict["Angle of Cut"] = self.intersectionangle
        self.dimensiondict["Cylinder Free Height"] = self.height
        self.dimensiondict["Partition Number"] = self.n                            
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetHeight(values["Height"])
            if not self.stop:
                self.SetIntersectionAngle(values["Angle"])
                if not self.stop:
                    self.SetFacetNumber(values["Number"])


    def SetDiameter(self,value):
        if value:
            try:
                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value Diameter")



    def SetIntersectionAngle(self,value):
        if value:
            try:
                self.intersectionangle = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Angle of Cut"""%value)
            else:
                if self.intersectionangle <= 0 or self.intersectionangle >= 90:
                    self.stop = 1
                    self.ShowError(\
"""Invalid input "%s" for Angle of Cut.\nAngle of Cut must be greater than 0 and less than 90 """%\
self.intersectionangle)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Angle of Cut")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Cylinder Free Height"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Cylinder Free Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 12:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 12"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Partition Number")






    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject
#CylinderCutAtAnyClass end
##############################################################

#Elbow Piece
##################################################
class ElbowPiece:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Llines = []
        self.Mlines = []


        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle
        
        self.diameterm = self.diameter #+(self.thickness/2) # Cylinder R         
        # calculate L values
        
        self.CalcM()
        self.CalcHValues()
        self.CalcL0()
        if not self.stop:
            self.CalcLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.l0 = self.height
        self.stop = 0
        

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameterm / self.n)


    def CalcH(self,n):
        return (self.diameterm /2)*(1 - (Cos(n*self.circleangle)))*Tan(self.intersectionangle)

    def CalcHValues(self):
        self.Hlist1 = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH(i))
            else:
                h = Decimal(self.CalcH(0))
            self.Hlist1.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn"] = self.Hlist1

    def CalcLValues(self):
        self.Llist1 = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1

      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.GenerateMlines()
        self.GenerateLlines()
        self.GenerateCurve()

    def GenerateMlines(self):
        self.mlinelist = []
        line0 = self.Line(label = "M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelist.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "M%d"%(i+1))
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)

    def GenerateLlines(self):
        self.linelist = [] # stores all the L lines
        for i in range(0,self.n+1):
            line2 = self.Line(label = "L%d"%i)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],-90)
            self.linelist.append(line2)


                    
    def GenerateCurve(self):
        self.curvelist = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i - 1].GetPoint2(),self.linelist[i].GetPoint2())
            self.curvelist.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)



    def ReceiveInput(self):
        self.dimensiondict["Elbow Diameter"] = self.diameter
        self.dimensiondict["Elbow Angle"] = self.intersectionangle
        self.dimensiondict["Elbow Free Height"] = self.height
        self.dimensiondict["Partition Number"] = self.n                            
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetHeight(values["Height"])
            if not self.stop:
                self.SetIntersectionAngle(values["Angle"])
                if not self.stop:
                    self.SetFacetNumber(values["Number"])


    def SetDiameter(self,value):
        if value:
            try:
                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Elbow Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value Elbow Diameter")



    def SetIntersectionAngle(self,value):
        if value:
            try:
                self.intersectionangle = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Elbow Angle"""%value)
            else:
                if self.intersectionangle <= 0 or self.intersectionangle >= 90:
                    self.stop = 1
                    self.ShowError(\
"""Invalid input "%s" for Elbow Angle.\nElbow Angle must be greater than 0 and less than 90 """%\
self.intersectionangle)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Elbow Angle")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Elbow Free Height"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Elbow Free Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 12:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 12"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Partition Number")






    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject
#ElbowPieceClass end
################################################################

#OffsetPieceClass begin
##############################################
class OffsetPiece:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Llines = []
        self.Mlines = []


        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []

        self.dimensiondict = {}
        self.valuedict = {}
        self.otherdict = {}

        self.lineslist = []


    def Run(self):
        
        if self.stop:
            pass
        else:
            self.InitialiseCalcData()
            self.ReceiveInput()
            self.Calculate()
            self.ShowResult1()

    def ShowResult1(self):
        if not self.stop:
            self.parent.ShowResult1(\
                self.dimensiondict,\
                self.valuedict,\
                self.otherdict)
        

    def Plot(self,frame):
        if self.stop:
            pass
        else:
            self.Gui.InitialisePlot(frame)
            self.Draw()

    def DestroyGui(self):
        self.Gui.Destroy()
    def Destroy(self):
        self.Gui.Destroy()


    def Calculate(self):
        self.circleangle = 360/float(self.n)  # facet angle
        
        self.diameterm = self.diameter #+(self.thickness/2) # Cylinder R         
        # calculate L values
        
        self.CalcM()
        self.CalcHValues0()
        self.CalcHValues1()
        self.CalcL0()
        self.CalcL1()
        if not self.stop:
            self.CalcLValues0()
            self.CalcLValues1()
            self.AddLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.stop = 0
        self.l0 = self.height0

    def CalcL1(self):
        self.stop = 0
        self.l1 = self.height1

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameterm / self.n)


    def CalcH0(self,n):
        return (self.diameterm /2)*(1 - (Cos(n*self.circleangle)))*Tan(self.intersectionangle0)

    def CalcH1(self,n):
        return (self.diameterm /2)*(1 - (Cos(n*self.circleangle)))*Tan(self.intersectionangle1)


    def CalcHValues0(self):
        self.Hlist0 = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH0(i))
            else:
                h = Decimal(self.CalcH0(0))
            self.Hlist0.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn-0"] = self.Hlist0


    def CalcHValues1(self):
        self.Hlist1 = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH1(i))
            else:
                h = Decimal(self.CalcH1(0))
            self.Hlist1.append(h)
        self.max_hvalue1 = max(self.Hlist1)
        self.valuedict["Hn-1"] = self.Hlist1

    def AddLValues(self):
        self.Laddlist = []
        for i in range(len(self.Llist0)):
            self.Laddlist.append(self.Llist0[i] + self.Llist1[i])
        self.valuedict["LT"] = self.Laddlist


    def CalcLValues0(self):
        self.Llist0 = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist0[i]
            self.Llist0.append(l)
        self.valuedict["Ln-0"] = self.Llist0

    def CalcLValues1(self):
        self.Llist1 = []
        for i in range(self.n+1):
            l = self.l1 +self.max_hvalue1 - self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln-1"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1

      

    def Draw(self):
        self.GenerateMlines()
        self.DrawMainLines0()
        self.DrawMainLines1()
        



    def DrawMainLines1(self):
        self.GenerateLlines1()
        self.GenerateCurve1()

    def DrawMainLines0(self):
        self.GenerateLlines0()
        self.GenerateCurve0()

    def GenerateMlines(self):
        self.mlinelist = []
        line0 = self.Line(label = "M0",outline = 0)
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelist.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "M%d"%(i+1),outline = 0)
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)

    def GenerateLlines0(self):
        self.linelist0 = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0
            else:
                outline = 1
            line2 = self.Line(label = "L0-%d"%i,outline = outline)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist0[i],-90)
            self.linelist0.append(line2)

    def GenerateLlines1(self):
        self.linelist1 = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0
            else:
                outline = 1
            line2 = self.Line(label = "L1-%d"%i,outline = outline)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],90)
            self.linelist1.append(line2)

                    
    def GenerateCurve0(self):
        self.curvelist0 = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelist0[i - 1].GetPoint2(),self.linelist0[i].GetPoint2())
            self.curvelist0.append(line3)


    def GenerateCurve1(self):
        self.curvelist1 = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelist1[i - 1].GetPoint2(),self.linelist1[i].GetPoint2())
            self.curvelist1.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)



    def ReceiveInput(self):
        self.dimensiondict["Offset Piece Diameter"] = self.diameter
        self.dimensiondict["Offset Piece Angle 1"] = self.intersectionangle0
        self.dimensiondict["Offset Piece Free Height 1"] = self.height0
        self.dimensiondict["Offset Piece Angle 2"] = self.intersectionangle1
        self.dimensiondict["Offset Piece Free Height 2"] = self.height1
        self.dimensiondict["Partition Number"] = self.n                            
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetIntersectionAngle0(values["Angle0"])
            if not self.stop:
                self.SetHeight0(values["Height0"])
                if not self.stop:
                    self.SetIntersectionAngle1(values["Angle1"])
                    if not self.stop:
                        self.SetHeight1(values["Height1"])
                        if not self.stop:
                            self.SetFacetNumber(values["Number"])


    def SetDiameter(self,value):
        if value:
            try:
                self.diameter = float(value)
                if self.diameter <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value Diameter")



    def SetIntersectionAngle0(self,value):
        if value:
            try:
                self.intersectionangle0 = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Offset Piece Angle 1"""%value)
            else:
                if self.intersectionangle0 <= 0 or self.intersectionangle0 >= 90:
                    self.stop = 1
                    self.ShowError(\
"""Invalid input "%s" for Offset Piece Angle 1.\nOffset Piece Angle 1 must be greater than 0 and less than 90 """%\
self.intersectionangle0)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Offset Piece Angle 1")


    def SetIntersectionAngle1(self,value):
        if value:
            try:
                self.intersectionangle1 = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Offset Piece Angle 1"""%value)
            else:
                if self.intersectionangle1 <= 0 or self.intersectionangle1 >= 90:
                    self.stop = 1
                    self.ShowError(\
"""Invalid input "%s" for Offset Piece Angle 2.\nOffset Piece Angle 2 must be greater than 0 and less than 90 """%\
self.intersectionangle1)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Offset Piece Angle 2")


    def SetHeight0(self,value):
        if value:
            try:
                self.height0 = float(value)
                if self.height0 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Offset Piece Free Height 1"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Offset Piece Free Height 1")


    def SetHeight1(self,value):
        if value:
            try:
                self.height1 = float(value)
                if self.height1 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Offset Piece Free Height 2"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Offset Piece Free Height 2")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 12:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 12"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Partition Number")






    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def SetScale(self):
        self.linkerobject.SetScale(2,2)

    def SetLinkerObject(self):
        self.linkerobject = LinkerObject()
    def SetLineClass(self):
        self.Line = self.linkerobject.GetLineClass().Line
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject






##################################################
class SaveDialog:
    def __init__(self,parent):
        self.name = None
        b = os.getcwd()
        defaultfilepath = os.path.join(b ,"SheetMetalWork")
        self.initialdir = defaultfilepath
        self.defaultext = ".cd"
        self.parent = parent
        self.filetypes = [('cdn','*.cd')]
        
        

    def SaveFile(self):
        filepath = asksaveasfilename(initialdir = self.initialdir,\
                                     defaultextension = self.defaultext,\
                                     parent = self.parent,filetypes = self.filetypes)
        
        if filepath:
            return str(filepath)
        else:
            return None
    def SetInitialDir(self,dirname):
        self.initialdir = dirname

class OpenDialog:
    def __init__(self,parent):
        self.name = None
        b = os.getcwd()
        defaultfilepath = b + "\\Examples"
        self.initialdir = defaultfilepath
        self.defaultext = ".cd"
        self.parent = parent
        self.filetypes = [('cdn','*.cd')]

    def OpenFile(self):
        filepath = askopenfilename(initialdir = self.initialdir,\
                                     defaultextension = self.defaultext,\
                                   parent = self.parent,filetypes = self.filetypes)
        
        if filepath:
            return str(filepath)
        else:
            return None


##############################################################
##############################################################

#TobeTopLevelClass begin 
##########################################################################################            
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
            self.wm_iconbitmap('SubFiles2\\Icon.ico')
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
#class TobeTopLevel end
####################################################



#class TobeTopLevel3 begin
##################################################################
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
            self.wm_iconbitmap('SubFiles2\\Icon.ico')
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






####################################
class WarningDialog:
    def __init__(self,parent):
        self.name = None
        self.parent = parent
                    
    def ShowErrorMessage(self,messagetitle,message):
        showinfo(messagetitle,message,parent = self.parent)



#DisplayResltClass begin
######################################################################################################################        
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


    
#DisplayResltClass end            
############################################################################################################
        

#InputPageClass begin
################################################################################
class InputPageClass:
    def __init__(self,parent,displaynames,inputnames,displaynames2 = None):
        self.parent = parent
        self.name = self.parent.name
        self.displayobj = DisplayResultClass(self,row = 0,column = 0,size = (900,500))
        self.SetDisplayNames(displaynames)
        self.SetInputNames(inputnames)
        self.SetDisplayNames2(displaynames2)

    def SetDisplayNames(self,displaynames):

        self.displaynames = displaynames

    def SetDisplayNames2(self,displaynames):
        self.displaynames2 = displaynames


    def SetInputNames(self,inputnames):
        self.inputnames = inputnames

    def SetName(self,name):
        self.name = name
        self.parent.SetName(name)

    def GetWindowRef(self):
        return self.master


    def CreateWindow(self,root):
        self.master = TobeTopLevel(root,self,self.CloseWindow,self.name,maximize = 1)
        self.master.CreateMenuBar2()
        
        self.master.geometry("980x450")
##        self.master.maxsize(width = 989,height = 455)
##        self.master.minsize(width = 979,height = 445)
        
        self.master.title(self.name)
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0,weight = 1)

        self.frame = Frame(self.master)
        self.frame.grid(sticky = W+E+N+S, row = 0, column = 0)
        self.frame.columnconfigure(0,weight = 1)
        self.count = 0

##        self.rowconfigure(0,weight = 1)
        self.frame.rowconfigure(1,weight = 1)
##        self.rowconfigure(2,weight = 1)
        self.frame.columnconfigure(1,weight = 1)
##        self.columnconfigure(2,weight = 1)

        self.frame1 = Frame(self.frame)
        self.frame1.grid(sticky = W+E+N+S, row = 1,rowspan = 3,column = 0,padx = 2,pady = 10)
        self.rowcount = 0
        for i in range(len(self.displaynames)):
            self.rowcount +=2
            self.frame1.rowconfigure(2*i,weight = 1)
            self.frame1.columnconfigure(2*(i+1) - 1, weight = 1)
            
        self.frame1.columnconfigure(0,weight = 0)
        self.frame1.columnconfigure(1,weight =0 )


        self.frame2 = Frame(self.frame)
        self.frame2.grid(sticky = W+E, row = 3, column = 0)
        self.frame2.columnconfigure(0,weight = 1)

        self.label = Label(self.frame2,text = "Dr. S. Gbeminiyi   ", font = "Arial 7")
        self.label.grid(sticky = W, row = 0,column = 0)

        self.label12 = Label(self.frame2,text = self.parent.category, font = "Arial 7")
        self.label12.grid(sticky = E, row = 0,column = 1)

        self.CreateDisplayLabels()
        self.CreateButtons()
        self.displayobj.CreateWindow(self.frame4)



        

    def CreateDisplayLabels(self):
        self.labellist  = []
        self.entrylist = []
        for i in range(len(self.displaynames)):
            label = Label(self.frame1,text = self.displaynames[i], font = "Arial 10")
            label.grid(sticky = E, row = 2*i,column = 0)
            entry = Entry(self.frame1)
            entry.grid(sticky = W,row = 2*i, column = 1)
            self.labellist.append(label)
            self.entrylist.append(entry)

    def HasEdited(self,event = None):
        self.master.SetHasEdited()



        
    def CreateButtons(self):
        self.frame3 = Frame(self.frame1)
        self.frame3.grid(sticky = W+E, row = self.rowcount,column = 0, columnspan = 2,pady = 10)
##        self.frame3.rowconfigure(0,weight = 1)
        self.frame3.columnconfigure(0,weight = 1)
        self.frame3.columnconfigure(1,weight = 1)
        self.frame3.columnconfigure(2,weight = 1)
        self.frame3.columnconfigure(3,weight = 1)
        self.frame3.columnconfigure(4,weight = 1)
        self.frame3.columnconfigure(5,weight = 1)
        self.frame3.columnconfigure(6,weight = 1)


        self.calcbutton = Button(self.frame3,text = "Calculate",command = self.Calculate)
        self.calcbutton.grid(sticky = W+E, row = 0,column = 2,columnspan = 2)


        self.plotbutton = Button(self.frame3,text = "Plot",command = self.Plot)
        self.plotbutton.grid(sticky = W+E, row = 0,column = 5,columnspan = 2)
        



        self.frame4 = Frame(self.frame)
        self.frame4.grid(sticky = W+E+N+S, row = 1,rowspan = 3,column = 1)
        self.frame4.rowconfigure(0,weight = 1)
        self.frame4.columnconfigure(0,weight = 1)
        self.count = 0


    def CloseWindow(self):
        self.parent.CloseWindow()

    def SetInputs(self,values):
        self.parent.SetInputs(values)


    def GetInputs(self):
        values = {}
        for i in range(len(self.inputnames)):
            values [self.inputnames[i]] = self.entrylist[i].get()
            
        self.SetInputs(values)
        
    def Close(self):
        self.master.destroy()


    def Calculate(self):
        self.HasEdited()
        self.GetInputs()
        self.parent.Calculate()

    def Plot(self):
        self.parent.Plot()
    def CloseCanvasWindow(self):
        self.parent.CloseCanvasWindow()

    def GetWindowReference(self):
        return self.master

    def ShowResult1(self,dimensiondict,valuedict,othersdict = None):
        self.displayobj.InsertData(dimensiondict,valuedict,othersdict = othersdict)

    def ShowResult2(self,valuedict):
        self.displayobj.InsertValue(valuedict)
    def GetDataToSave(self,fileobj):
        self.fileobj = fileobj
        self.fileobj['text'] = self.displayobj.GetDataToSave()
        self.parent.GetDataToSave(fileobj)

    def ReceiveDataToOpen(self,fileobj):
        self.fileobj = fileobj
        btext = self.fileobj['text']
        name = self.fileobj['name']
        valuedict = self.fileobj['input']
        filepath = self.fileobj['filepath']
        self.master.SetName(name)
        self.master.SetOpenDetails(filepath)
        self.PlaceInputs(valuedict)
        self.displayobj.ReceiveDataToOpen(btext)
       
       
    def PlaceInputs(self,valuedict):
        if valuedict:
            values = {}
            for i in range(len(self.displaynames)):
                self.entrylist[i].insert(INSERT,valuedict[self.displaynames2[i]])


        


        

#InputPageClass end
################################################################################


#PageTemplateClass begin
################################################################################
class PageTemplate:
    def __init__(self):
        self.nothing = 1
        self.name = ""
       
    def SetInputs(self,value):
        self.values = value

    def ShowResult1(self,dimensiondict,valuedict,othersdict = None):
        self.inputpageobj.ShowResult1(dimensiondict,valuedict,othersdict = othersdict)



    def CreateWindow(self,root):
        self.inputpageobj.CreateWindow(root)
        self.master = self.inputpageobj.GetWindowReference()
        self.count = 0

    def CloseWindow(self):
        self.parent.CloseOption(self.idnumber)
        self.brain.Destroy()
        



    def GetInputs(self):
        self.brain.SetInput(self.values)
    def Close(self):
        self.master.destroy()


    def Calculate(self):
        self.allow = 1

        self.brain.SetErrorDialog(WarningDialog(self.inputpageobj.master))
        self.GetInputs()
        self.brain.Run()

    def SetName(self,name):
        self.name = name
        self.brain.SetName(name)
        


    def Plot(self):
        if self.allow:
            if self.brain.stop:
                pass
            else:
                self.count +=1
                if self.count == 1:
                    self.SetupWindow()
                self.brain.Plot(self.top1)

    def CloseCanvasWindow(self):
        self.count = 0
        self.brain.DestroyGui()

    def SetupWindow(self):
        self.top1 = TobeTopLevel3(self.master,self,funcid = self.CloseCanvasWindow)

    def SetIdnumber(self,idnumber):
        self.idnumber = idnumber

    def GetDataToSave(self,fileobj):
        self.fileobj = fileobj
        self.fileobj['input'] = self.brain.GetDataToSave()
        self.fileobj['category'] = self.category
        self.fileobj['classname'] = self.classname

    def ReceiveDataToOpen(self,fileobj):
        self.fileobj = fileobj
        self.inputpageobj.ReceiveDataToOpen(self.fileobj)
        
        

#PageTemplateClass end
################################################################################




########################################################
####################################        
####################################
####################################
####################################
####################################
################################################################################


 

######################################################################################################################
######################################################################################################################
class RectToRoundPage(PageTemplate):
    Count = 0
    def __init__(self,parent):
        RectToRoundPage.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round Transition Piece"
        self.classname = "Transition Piece"
        
        self.name = "RectRoundPage Project %d"% RectToRoundPage.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height","Facet number"]
        self.displaynames = ["Diameter: ","Length: ","Breadth: ","Height: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Length","Breadth","Height","Facet Number"]
        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRound(self,self.name)

        

            
class RectToRoundOff1Page(PageTemplate):
    Count = 0
    def __init__(self,parent):
        RectToRoundOff1Page.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round One Way offset Transition Piece"
        self.classname = "Transition Piece"
        
        self.name = "Rectangular To Round One Way offset Project %d"% RectToRoundOff1Page.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height","Offset distance","Facet number"]
        self.displaynames = ["Diameter: ","Length: ","Breadth: ","Height: ","Offset distance: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Length","Breadth","Height","Offset distance","Facet Number"]
        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRoundOff1(self,self.name)
        
        

class RectToRoundOff2Page(PageTemplate):
    Count = 0
    def __init__(self,parent):
        RectToRoundOff2Page.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round Two Way offset Transition Piece"
        self.classname = "Transition Piece"
        
        self.name = "Rectangular To Round Two Way offset Project %d"% RectToRoundOff2Page.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height",\
                           "Offset distance x","Offset distance y","Facet number"]
        self.displaynames = ["Diameter: ","Length: ","Breadth: ","Height: ",\
                             "Offset distance x: ","Offset distance y: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Length","Breadth","Height",\
                             "Offset distance x","Offset distance y","Facet Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRoundOff2(self,self.name)



class RectToRoundObliquePage(PageTemplate):

    Count = 0
    def __init__(self,parent):
        RectToRoundObliquePage.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round Oblique Plane"
        self.classname = "Transition Piece"
        
        self.name = "Rectangular to Round Oblique plane Project %d"% RectToRoundObliquePage.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height",\
                           "Inclination","Facet number"]
        self.displaynames = ["Diameter: ","Bevel Length: ","Breadth: ","Height: ",\
                            "Vertical Inclination: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Bevel Length","Breadth","Height",\
                            "Vertical Inclination","Facet Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRoundOblique(self,self.name)


class ConicalFrustumPage(PageTemplate):

    Count = 0
    def __init__(self,parent):
        ConicalFrustumPage.Count +=1
        self.parent = parent
        self.category = "Conical Frustum"
        self.classname = "Transition Piece"
        self.name = "Conical Frustum Project %d"% ConicalFrustumPage.Count
        self.allow = 0
        self.inputnames = ["Top diameter","Base diameter","Height","Facet number"]
        self.displaynames = ["Top Diameter: ","Base Diameter: ","Height: ","Facet Number: "]
        self.displaynames2 = ["Top Diameter","Base Diameter","Height","Facet Number"]
        
        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = ConicalFrustum(self,self.name)






########################################################
####################################        
####################################
####################################
####################################
####################################
################################################################################

class TJunctionPage(PageTemplate):
    Count = 0
    def __init__(self,parent):
        TJunctionPage.Count +=1
        self.parent = parent
        self.category = "T-Junction Piece"
        self.classname = "Interpenetration Piece"
        
        self.name = "T-junction Interpenetration piece Project %d"% TJunctionPage.Count
        self.allow = 0
        self.inputnames = ["Diameter1","Diameter2","Height","Number"]
        self.displaynames = ["Interpenetrated\npipe Diameter ","Interpenetrating\npipe Diameter ",\
                             "Free Height of\nInterpenetrating pipe ","Partition Number "]
        self.displaynames2 = ["Interpenetrated pipe Diameter","Interpenetrating pipe Diameter",\
                              "Free Height of Interpenetrating pipe","Partition Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = TJunction(self,self.name)

#TJunctionPageClass end
############################################        

#SquareToCylinderPageClass begin
######################################################        
class SquareToCylinderPage(PageTemplate):
    Count = 0
    def __init__(self,parent):
        SquareToCylinderPage.Count +=1
        self.parent = parent
        self.category = "Square pipe Interpenetrating A Cylindrical pipe Vertically"
        self.classname = "Interpenetration Piece"
        self.name = "Square To Cylinder Interpenetration piece Project %d"% SquareToCylinderPage.Count
        self.allow = 0
        self.inputnames = ["Diameter1","Length","Height","Number"]#problem1
        self.displaynames = ["Interpenetrated\npipe Diameter: ","Interpenetrating\nsquare pipe length: ",\
                             "Free Height of\nInterpenetrating pipe: ","Partition Number: "]
        self.displaynames2 = ["Interpenetrated pipe Diameter","Interpenetrating square pipe length",\
                             "Free Height of Interpenetrating pipe","Partition Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = SquareToCylinder(self,self.name)

#SquareToCylinderPageClass end
##################################################

#CylindricalPipeAtAnyAnglePageClass begin
######################################################        
class CylindricalPipeAtAnyAnglePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        CylindricalPipeAtAnyAnglePage.Count +=1
        self.parent = parent
        self.category = "Interpenetration of Cylindrical Pipes At Any Angle"
        self.classname = "Interpenetration Piece"
        self.name = "Interpenetration of Cylindrical Pipe At Any Angle Project %d"% CylindricalPipeAtAnyAnglePage.Count
        self.allow = 0
        self.inputnames = ["Diameter1","Diameter2","Angle","Height","Number"]
        self.displaynames = ["Interpenetrated\npipe Diameter: ","Interpenetrating\npipe Diameter: ",\
                             "Angle of Interpenetration: ","Free Height of\nInterpenetrating pipe: ","Partition Number: "]

        self.displaynames2 = ["Interpenetrated pipe Diameter","Interpenetrating pipe Diameter",\
                              "Angle of Interpenetration","Free Height of Interpenetrating pipe",\
                              "Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = CylindricalPipeAtAnyAngle(self,self.name)


#CylindricalPipeAtAnyAnglePageClass end
####################################################        

#YJunctionPiecePageClass begin
################################################                                        
class YJunctionPiecePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        YJunctionPiecePage.Count +=1
        self.parent = parent
        self.category = "Y-Junction Piece"
        self.classname = "Interpenetration Piece"
        self.name = "Y-Junction Piece Project %d"% YJunctionPiecePage.Count
        self.allow = 0
        self.inputnames = ["Diameter",'Height0',"Angle B1",'Height1',"Angle B2","Height2","Number"]
        self.displaynames = ["Junction Piece Diameter: ","Free Height of pipe A: ",\
                             "Angle of Intersection\n for pipe B1:","Free Height of pipe B1: ",\
                             "Angle of Intersection\n for pipe B2:","Free Height of pipe B2: ",\
                             "Partition Number: "]

        self.displaynames2 = ["Junction Piece Diameter","Free Height of pipe A",\
                             "Angle of Intersection for pipe B1","Free Height of pipe B1",\
                             "Angle of Intersection for pipe B2","Free Height of pipe B2",\
                             "Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = YJunctionPiece(self,self.name)
#YJunctionPiecePageClass end
################################################################

#CylinderCutAtAnyPageClass begin
##########################################################################################

class CylinderCutAtAnyPage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        CylinderCutAtAnyPage.Count +=1
        self.parent = parent
        self.category = "Right Cylinder Cut Obliquely"
        self.classname = "Interpenetration Piece"
        self.name = "Right Cylinder Cut Obliquely Project %d"% CylinderCutAtAnyPage.Count
        self.allow = 0
        self.inputnames = ["Diameter",'Height',"Angle","Number"]
        self.displaynames = ["Cylinder Diameter: ","Cylinder Free Height: ",\
                             "Angle of Cut: ","Partition Number: "]

        self.displaynames2 = ["Cylinder Diameter","Cylinder Free Height",\
                             "Angle of Cut","Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = CylinderCutAtAny(self,self.name)

#CylinderCutAyAnyPageClass end
################################

#ElbowPieceClass begin
########################################################        
class ElbowPiecePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        ElbowPiecePage.Count +=1
        self.parent = parent
        self.category = "Elbow Piece"
        self.classname = "Interpenetration Piece"
        self.name = "Elbow Piece Project %d"% ElbowPiecePage.Count
        self.allow = 0
        self.inputnames = ["Diameter",'Height',"Angle","Number"]
        self.displaynames = ["Elbow Diameter: ","Elbow Free Height: ",\
                             "Elbow Angle: ","Partition Number: "]

        self.displaynames2 = ["Elbow Diameter","Elbow Free Height",\
                             "Elbow Angle","Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = ElbowPiece(self,self.name)

#ElbowPieceClass end
##########################################
    def ReceiveInput(self):
        self.dimensiondict["Offset Piece Diameter"] = self.diameter
        self.dimensiondict["Offset Piece Angle 1"] = self.intersectionangle0
        self.dimensiondict["Offset Piece Free Height 1"] = self.height0
        self.dimensiondict["Offset Piece Angle 2"] = self.intersectionangle1
        self.dimensiondict["Offset Piece Free Height 2"] = self.height1
        self.dimensiondict["Partition Number"] = self.n                            
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetIntersectionAngle0(values["Angle0"])
            if not self.stop:
                self.SetHeight0(values["Height0"])
                if not self.stop:
                    self.SetIntersectionAngle1(values["Angle1"])
                    if not self.stop:
                        self.SetHeight1(values["Height1"])
                        if not self.stop:
                            self.SetFacetNumber(values["Number"])




class OffsetPiecePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        OffsetPiecePage.Count +=1
        self.parent = parent
        self.category = "Offset Piece"
        self.classname = "Interpenetration Piece"
        self.name = "Offset Piece Project %d"% OffsetPiecePage.Count
        self.allow = 0
        self.inputnames = ["Diameter","Angle0","Height0","Angle1","Height1","Number"]
        self.displaynames = ["Offset Piece Diameter: ","Offset Piece Angle 1: ",\
                             "Offset Piece Free Height 1: ","Offset Piece Angle 2: ",\
                              "Offset Piece Free Height 2: ","Partition Number: "]

        self.displaynames2 = ["Offset Piece Diameter","Offset Piece Angle 1",\
                             "Offset Piece Free Height 1","Offset Piece Angle 2",\
                              "Offset Piece Free Height 2","Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = OffsetPiece(self,self.name)



        
#HomeScreenClass begin
##########################################################################################################        
class HomeScreen(Frame):
    def __init__(self):
        Frame.__init__(self)

        try:
            self.master.state(GetZoomedStateOption(sys.platform))
        except Exception:
            pass 
           

        self.master.protocol("WM_DELETE_WINDOW", self.CloseHomeScreen)
        self.master.title("SHEET METAL WORK")
        self.master.rowconfigure(0,weight = 1)
        try:
            self.master.wm_iconbitmap(os.path.join('SubFiles2','Icon.ico'))
##            self.master.iconmask('SubFiles2\\Icon.ico')
        except TclError:
            pass
            
        try:
            b = os.getcwd()
            defaultfilepath = os.path.join(b, "SheetMetalWork")
            os.mkdir(defaultfilepath)
        except Exception:
            pass
        
        self.master.columnconfigure(0,weight = 1)
        self.grid(sticky = W+E+N+S, row = 0, column = 0)
        self.wtext = "Chondochol Design"
        self.columnconfigure(0,weight = 1)

        self.transitionpiecepage =\
                            TransitionPiecePage(self)
        self.interpenetrationpage = InterpenetrationPiecePage(self)

        self.countinterpenetration = 0
        self.counttransition = 0
        

        self.rowconfigure(0,weight = 1)
        self.rowconfigure(2,weight = 1)

        self.frame1 = Frame(self)
        self.frame1.grid(sticky = W+E+N+S, row = 0,column = 0)
        self.frame1.rowconfigure(0,weight = 1)
        self.frame1.rowconfigure(1,weight = 1)
        self.frame1.columnconfigure(0,weight = 1)
        self.frame1.columnconfigure(1,weight = 1)

        self.frame2 = Frame(self)
        self.frame2.grid(sticky = N+W+E, row = 2, column = 0)
        self.frame2.rowconfigure(0,weight = 1)
        self.frame2.columnconfigure(0,weight = 1)
        self.frame2.columnconfigure(1,weight = 1)
        

        try:
            self.inter_file1 = PhotoImage(file = os.path.join("SubFiles","interfile1.tx"))
            self.trans_file1 = PhotoImage(file = os.path.join("SubFiles","transfile1.tx"))
        except Exception:
            self.button1 = Button(self.frame1,\
                                  text = "Interpenetration Piece",\
                                  command = self.StartInterpenetration)
            self.button2 = Button(self.frame1,\
                            text = "Transition Piece", command = self.StartTransitionPiece)

        else:

            self.button1 = Button(self.frame1,\
                                  image = self.inter_file1,\
                                  command = self.StartInterpenetration)

            self.button2 = Button(self.frame1,\
                               image = self.trans_file1, command = self.StartTransitionPiece)

        self.labelbutton1 = Label(self.frame1,text = "INTERPENETRATION PIECE",\
                                  font = "Arial 15 bold")
        self.labelbutton1.grid(sticky = W+E, row = 1,column = 0)
            
        self.labelbutton2 = Label(self.frame1,text = "TRANSITION PIECE", font = "Arial 15 bold")
        self.labelbutton2.grid(sticky = W+E, row = 1,column = 1)
       
        self.button1.grid(sticky = W+E+N+S, row = 0, column = 0,padx = 20)

        self.button2.grid(sticky = W+E+N+S, row = 0,column = 1,padx = 20)

        self.label = Label(self.frame2,text = "Dr. S. Gbeminiyi", font = "Arial 10 ")
        self.label.grid(sticky = NW, row = 0,column = 0)
        try:
            self.logofile = PhotoImage(file = os.path.join("SubFiles","transfile2.tx"))
        except Exception,message:
            self.labellogo = Label(self.frame2,text = self.wtext , font = "Arial 7 ")
            

        else:
            self.labellogo = Label(self.frame2,image = self.logofile)
            
        self.labellogo.grid(sticky = NE, row = 0,column = 1)



    def StartInterpenetration(self):
        self.countinterpenetration +=1
        if self.countinterpenetration == 1:
            self.interpenetrationpage.CreateWindow()

        else:
            self.interpenetrationpage.Lift()
    def StartTransitionPiece(self):
        self.counttransition +=1
        if self.counttransition == 1:
            self.transitionpiecepage.CreateWindow()
        else:
            self.transitionpiecepage.Lift()

    def Lower0(self):
        self.transitionpiecepage.Lower()
    def Lower1(self):
        self.interpenetrationpage.Lower()

    def CloseHomeScreen(self):
        if self.transitionpiecepage.AnyProject():
            answer = askyesnocancel("Quit","You Have Active Projects.\nDo you want to quit Anyway?")
        else:
            answer = 1
        if answer:
            self.master.destroy()

    def OpenOption(self,classname,fileobj):
        if classname == "Transition Piece":
            self.transitionpiecepage.ReceiveDataToOpen(fileobj)
        elif classname == "Interpenetration Piece":
            self.interpenetrationpage.ReceiveDataToOpen(fileobj)
        else:
            pass

    def ShowNext(self):
        self.rectpage.CreateWindow()

    def InitializeCount1(self):
        self.counttransition = 0
    def InitializeCount2(self):
        self.countinterpenetration = 0

#HomeScreenClass begin
##########################################################################################################        

#TobeTopLevel2Class begin
##########################################################################################################        
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
            self.fileobj2.close()
        except Exception:
            self.errordialog.ShowErrorMessage("file","Could not close file")


#TobeTopLevel2Class begin
##########################################################################################################        



#TransitionPiecePageClass begin
##########################################################################################################        
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

#TransitionPiecePageClass end
##########################################################################################################        




#InterpenetrationPiecePageClass begin
##########################################################################################################        

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




def main():
    HomeScreen().mainloop()
if __name__ == "__main__":
    main()
        
