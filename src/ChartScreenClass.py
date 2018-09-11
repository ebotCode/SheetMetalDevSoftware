
from Tkinter import*
import Pmw
Pmw.initialise()

class ChartScreen:
    """
    GUi screen that displays Sheet Metal Charts. 
    """
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
        
