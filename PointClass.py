from MathUtils import * 

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

    
        