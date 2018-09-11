from Tkinter import * 


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



    def ZoomWheel(self,value):
        if self.ingraph:
            self.chartscale.ScaleZoom3(value)
        else:
            pass
