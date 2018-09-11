
class ChartScale:
    """
    ChartScale handles the scaling of Charts generated.

    """
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
