from LineClass import* 
from PointClass import * 


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
     