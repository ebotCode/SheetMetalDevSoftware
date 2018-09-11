from GraphGuiClass import* 
from MathUtils import* 
from LinkerClass import* 

import math 

class ConicalFrustum:
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

        self.topdiameter = self.diameter1 - self.thickness # mean diameter
        self.basediameter = self.diameter2 - self.thickness # mean diameter
        self.topradius = self.topdiameter / 2
        self.baseradius = self.basediameter / 2
        # calculate L values
        self.CalcL1()
        self.CalcRp()
        self.CalcRc()
        self.CalcThetaPattern()
        self.CalcZ()

        
    def CalcL1(self):
        self.l1 = Decimal(math.sqrt(pow((self.baseradius - self.topradius),2) + pow((self.height),2)))
        self.otherdict["L1"] = self.l1
    def CalcRp(self):
        self.rp = Decimal((self.basediameter / (2 * (self.basediameter - self.topdiameter)))*\
                          math.sqrt(pow((self.basediameter - self.topdiameter),2) + (4*pow((self.height),2))))
        self.otherdict["Pattern Radius Rp"] = self.rp
        
    def CalcRc(self):
        self.rc = Decimal((self.topdiameter / (2 * (self.basediameter - self.topdiameter)))*\
                          math.sqrt(pow((self.basediameter - self.topdiameter),2) + (4*pow((self.height),2))))
        self.otherdict["Cut Radius Rc"] = self.rc

    def CalcThetaPattern(self):
        self.thetapattern = Decimal((360 * (self.basediameter - self.topdiameter)/\
                          math.sqrt(pow((self.basediameter - self.topdiameter),2) + (4*pow((self.height),2)))))
        self.deltatheta_pattern = self.thetapattern / self.n
        self.otherdict["Pattern Angle"] = self.thetapattern

    def CalcZ(self):
        self.z =  Decimal(math.sqrt( pow((-self.topradius  + (self.baseradius* Cos(self.circleangle))),2) +\
                                  pow((self.baseradius*Sin(self.circleangle)),2) +\
                                  pow((self.height),2)))

        self.otherdict["Z"] = self.z

    def CalcThetaN(self,n):
        return self.thetapattern * n

    def CalcPoint1(self,n):
        line2coordx1 = self.a0 + (self.rp*(1 - Cos(n *self.deltatheta_pattern)))
        line2coordy1 = self.a1 + (self.rp*Sin(n *self.deltatheta_pattern))
        return (line2coordx1, line2coordy1)

    def CalcPoint2(self,n):
        line2coordx2 = self.a0 + (self.rp - ((self.rp - self.l1) * Cos(n* self.deltatheta_pattern)))
        line2coordy2 = self.a1 + ((self.rp - self.l1)*Sin(n * self.deltatheta_pattern))
        return (line2coordx2, line2coordy2)
                            
            
      

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.linelist = []
        self.line1 = self.Line(label = "Z")
        self.line1.Initialize4((self.a0,self.a1),self.l1,0)
        self.linelist.append(self.line1)

        for i in range(self.n):
            if i == self.n-1:
                outline2 = 1
            else:
                outline2 = 0
            line2 = self.Line(label = "Z",outline = outline2)
            line2.Initialize1(self.CalcPoint1(i+1),self.CalcPoint2(i+1))
            self.linelist.append(line2)


        for i in range(self.n):

            line3 = self.Line()  # curve outline 
            line3.Initialize2(self.linelist[i].GetPoint1(),\
                              self.linelist[i+1].GetPoint1())
            
            line4 = self.Line()  # Inner curve outline 
            line4.Initialize2(self.linelist[i].GetPoint2(),\
                              self.linelist[i+1].GetPoint2())

            outline2 = 0 
            line6 = self.Line(outline = outline2)
            line6.Initialize2(self.linelist[i].GetPoint2(),\
                              self.linelist[i+1].GetPoint1())



    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Top Diameter"] = self.diameter1
        self.dimensiondict["Base Diameter"] = self.diameter2
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n

    def SetInput(self,values):
        self.SetDiameterTop(values ["Top diameter"])
        if not self.stop:
            self.SetDiameterBase(values["Base diameter"])
            if not self.stop:
                self.SetHeight(values["Height"])
                if not self.stop:
                    self.SetFacetNumber(values["Facet number"])


    def SetDiameterTop(self,value):
        if value:
            try:

                self.diameter1 = float(value)
                if self.diameter1 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Top Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Top Diameter")


    def SetDiameterBase(self,value):
        if value:
            try:
                self.diameter2 = float(value)
                if self.diameter2 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Base Diameter"""%value)
            else:
                if self.diameter1 == self.diameter2:
                    self.ShowError("""Cannot have base diameter and top diameter\nto be the same""")
                    self.stop = 1
                else:           
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Base Diameter")


    def SetHeight(self,value):
        if value:
            try:
                self.height = float(value)
                if self.height <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Height"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Height")

    def SetFacetNumber(self,value):
        if value:
            try:
                value2 = int(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Invalid Input "%s" for Facet Number"""% value)
            else:
                    
                if value2 > 18 or value2 < 6:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Facet Number\n valid range 6 to 18"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.n = value2
        else:
            self.stop = 1
            self.ShowError("No value for Facet Number")

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
