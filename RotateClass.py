from Tkinter import * 

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


