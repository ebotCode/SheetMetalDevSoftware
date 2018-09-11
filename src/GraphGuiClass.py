from ChartScaleClass import * 
from ChartScreenClass import * 
from DisplayLabelClass import * 
from ToolBarClass import * 
from DisplayResultClass import * 

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

            self.frame2.columnconfigure(1,weight = 1)
            self.frame2.rowconfigure(0,weight = 1)
            self.frame2.grid(sticky = W+E+N+S, row = 1, column = 0)

            self.SetFrames()
            self.master.SetZoomObject(self.toollabel.zoombutton)
            self.cleargraph = 1
            
        else:
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
