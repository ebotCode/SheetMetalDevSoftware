from GraphGuiClass import* 
from MathUtils import* 
from LinkerClass import* 

import math 

class SquareToCylinder:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 100
        self.a1 = 100

        self.thickness = 1.5
        
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
        
        self.R = self.diameter1 / 2   # Intersected Pipe R         
        # calculate L values
        self.CalcM()
        self.CalcHValues()
        self.CalcL0()
        if not self.stop:
            self.CalcLValues()
            self.CalcMValues()

        
    def CalcL0(self):
        self.stop = 0
        self.l0 = self.height

    def CalcM(self):
        self.M = Decimal(self.length / self.n)


    def CalcH(self,n):
        return self.R - math.sqrt(pow(self.R,2) - (0.5*pow((n * self.length/self.n),2)))

    def CalcHValues(self):
        self.Hlist1 = []
        self.Hlist2 = []
        for i in range(self.n+1):

            h = Decimal(self.CalcH(i))
            self.Hlist1.append(h)
        self.valuedict["N"] = range((self.n*4)+1)
        for i in range(1,self.n+1):
            self.Hlist2.append(self.Hlist1[-(i+1)])
        self.Hlist1 = self.Hlist1 + self.Hlist2[:]
        self.Hlist3 = self.Hlist1[1:(self.n*2)+1]
        self.Hlist1 = self.Hlist1 + self.Hlist3[:]
        self.Hlist2 = None
        self.Hlist3 = None
        self.valuedict["Hn"] = self.Hlist1

    def CalcLValues(self):
        self.Llist1 = []
        for i in range(len(self.Hlist1)):
            l = self.l0 + self.Hlist1[i]
            self.Llist1.append(l)
        self.valuedict["Ln"] = self.Llist1
        

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n*4):
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
        for i in range(len(self.Mlist1)-1):
            line1 = self.Line(label = "M%d"%(i+1))
            line1.Initialize5(self.mlinelist[i].GetPoint2(), self.M,0)
            self.mlinelist.append(line1)
        

    def GenerateLlines(self):
        self.linelist = [] # stores all the L lines
        N = len(self.Hlist1)
        for i in range(N):
            if i > 0 and i < (N-1):
                outline2 = 0
            else:
                outline2 = 1             
            line2 = self.Line(label = "L%d"%i, outline = outline2)
            line2.Initialize5(self.mlinelist[i].GetPoint2(),self.Llist1[i],-90)
            self.linelist.append(line2)

                    
    def GenerateCurve(self):
        self.curvelist = []
        for i in range(len(self.Hlist1)-1):
            line3 = self.Line()
            line3.Initialize2(self.linelist[i].GetPoint2(),self.linelist[i+1].GetPoint2())
            self.curvelist.append(line3)

    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Interpenetrating square pipe length"] = self.length #r
        self.dimensiondict["Interpenetrated pipe Diameter"] = self.diameter1 #R
        self.dimensiondict["Free Height of Interpenetrating pipe"] = self.height
        self.dimensiondict["Partition Number"] = self.n

    def SetInput(self,values):
        self.SetLength(values ["Length"])
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
                b = self.length * math.sqrt(2)
                if b > self.diameter1:
                    self.stop = 1
                    self.ShowError(\
        """Interpenetrated pipe Diameter is small. It should be greater than 1.4142 times the Interpenetrating Square length""")
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrated pipe Diameter")


    def SetLength(self,value):
        if value:
            try:
                self.length = float(value)
                if self.length <= 0 :
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Interpenetrating Square pipe Length"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Interpenetrating square pipe Length")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height of Interpenetrating pipe"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Height of Interpenetrating pipe")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Partition Number"""% value)
            else:
                    
                if  value2 < 2:
                    self.stop = 1
                    self.ShowError(\
            """Invalid Input "%s" for Partition Number\n must be greater or equal to 2"""% str(value2))
                    
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
