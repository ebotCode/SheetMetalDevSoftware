from MathUtils import * 

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

