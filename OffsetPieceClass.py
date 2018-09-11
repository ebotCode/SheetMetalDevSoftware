from GraphGuiClass import * 
from LinkerClass import * 
from MathUtils import * 

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

