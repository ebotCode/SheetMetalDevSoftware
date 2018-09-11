from Tkinter import * 

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
    