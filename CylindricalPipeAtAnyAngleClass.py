from GraphGuiClass import* 
from MathUtils import* 
from LinkerClass import* 

import math 
  
class CylindricalPipeAtAnyAngle:
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
        
        self.diameter1m = self.diameter1 #+(self.thickness/2) # Intersected Pipe R         
        self.diameter2m = self.diameter2 #+ (self.thickness/2)# Intersecting Pipe r
        # calculate L values
        
        self.CalcM()
        self.CalcHValues()
        self.CalcL0()
        if not self.stop:
            self.CalcLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.l0 = self.height
        self.stop = 0

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter2m / self.n)


    def CalcH(self,n):
        return 0.5*(((self.diameter1m - \
            math.sqrt(pow(self.diameter1m,2) - pow((self.diameter2m * Sin(n * self.circleangle)),2)))*\
            Cosec(self.intersectionangle)) + (self.diameter2m * (1 - Cos(n* self.circleangle))*Cot(self.intersectionangle)))

    def CalcHValues(self):
        self.Hlist1 = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH(i))
            else:
                h = Decimal(self.CalcH(0))
            self.Hlist1.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn"] = self.Hlist1

    def CalcLValues(self):
        self.Llist1 = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1




            
      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.GenerateMlines()
        self.GenerateLlines()
        self.GenerateCurve()

    def GenerateMlines(self):
        self.mlinelist = []
        line0 = self.Line(label = "M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelist.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "M%d"%(i+1))
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)

    def GenerateLlines(self):
        self.linelist = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline2 = 0
            else:
                outline2 = 1             
            line2 = self.Line(label = "L%d"%i,outline = outline2)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],-90)
            self.linelist.append(line2)

##        line2 = self.Line(label = "L%d"%(self.n))
##        line2.Initialize5(self.mlinelist[self.n - 1].GetPoint2(),self.Llist1[0],-90)
##        self.linelist.append(line2)

                    
    def GenerateCurve(self):
        self.curvelist = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i - 1].GetPoint2(),self.linelist[i].GetPoint2())
            self.curvelist.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)



    def ReceiveInput(self):
        self.dimensiondict["Interpenetrating pipe Diameter"] = self.diameter2 #r
        self.dimensiondict["Angle of Interpenetration"] = self.intersectionangle
        self.dimensiondict["Interpenetrated pipe Diameter"] = self.diameter1 #R
        self.dimensiondict["Free Height of Interpenetrating pipe"] = self.height
        self.dimensiondict["Partition Number"] = self.n

    def SetInput(self,values):
        self.SetDiameter2(values ["Diameter2"])
        if not self.stop:
            self.SetIntersectionAngle(values["Angle"])
            if not self.stop:
                self.SetDiameter1(values["Diameter1"])
                if not self.stop:
                    self.SetHeight(values["Height"])
                    if not self.stop:
                        self.SetFacetNumber(values["Number"])


    def SetDiameter1(self,value):
        if value:
            try:
                self.diameter1 = float(value)
                if self.diameter1 <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrated pipe Diameter"""%value)
            else:
                if self.diameter2 > self.diameter1:
                    self.stop = 1
                    self.ShowError(\
        """Interpenetrated pipe Diameter is small. It should be greater than the Interpenetrating pipe Diameter""")
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrated pipe Diameter")


    def SetDiameter2(self,value):
        if value:
            try:
                self.diameter2 = float(value)
                if self.diameter2 <= 0 :
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrating pipe Diameter"""%value)
            else:
               
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrating pipe Diameter")


    def SetIntersectionAngle(self,value):
        if value:
            try:
                self.intersectionangle = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Angle of Interpenetration"""%value)
            else:
                if self.intersectionangle <= 0 or self.intersectionangle > 90:
                    self.stop = 1
                    self.ShowError(\
"""Invalid input "%s" for Angle of Interpenetration.\nAngle of Interpenetration must be greater than 0 and less than or equal to 90 """%\
self.intersectionangle)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Angle of Interpenetration")






    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of Interpenetrating pipe"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Height of Free Height of Interpenetrating pipe")

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
