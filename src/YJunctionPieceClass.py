from GraphGuiClass import* 
from MathUtils import* 
from LinkerClass import* 

import math 


class YJunctionPiece:
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
        
        self.diameter1m = self.diameter #+(self.thickness/2) # Intersected Pipe R
        self.R = self.diameter1m/2
        # calculate L values
        
        self.CalcM()
        self.CalcHValuesA()
        self.CalcHValuesB1()
        self.CalcHValuesB2()
        self.CalcL0()
        if not self.stop:
            self.CalcL1()
            if not self.stop:
                self.CalcL2()
                if not self.stop:                    
                    self.CalcLValuesA()
                    self.CalcLValuesB1()
                    self.CalcLValuesB2()
                    self.CalcMValues()

        
    def CalcL0(self):
        self.l0 = self.height0
        self.stop = 0

    def CalcL1(self):
        self.l1 = self.height1
        self.stop = 0

    def CalcL2(self):
        self.l2 = self.height2
        self.stop = 0
        
        

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter1m / self.n)


    def CalcH0(self,n):
        return self.R * (1 -  math.sqrt(pow(Cos(n * self.circleangle),2))) * Tan(self.intersectionangle1/2)

    def CalcH10(self,n): # B1 formular1 bwn 90<= theta <= 270
        return self.R * (Cot(self.intersectionangle1) - \
                         (math.sqrt(pow(Cos(n * self.circleangle),2)) *\
                         Tan(self.intersectionangle1/2)))
    
    def CalcH11(self,n):# B1 formular2 0 <= theta < 90 and 270< theta <= 360
        return self.R * (1 -  (Cos(n * self.circleangle))) * Cot(self.intersectionangle1)
##
    
    def CalcH20(self,n): #B2 formular1 90<= theta <= 270
        return self.R * (Cot(self.intersectionangle2) - \
                         (math.sqrt(pow(Cos(n * self.circleangle),2)) *\
                         Tan(self.intersectionangle2/2)))

    def CalcH21(self,n): #b2 formular2 90<=theta<=270
        return self.R * (1 -  (Cos(n * self.circleangle))) * Cot(self.intersectionangle2)
##

    def CalcHValuesA(self):
        self.Hlist1A = []
        for i in range(self.n+1):
            if i != self.n:
                h = Decimal(self.CalcH0(i))
            else:
                h = Decimal(self.CalcH0(0))
            self.Hlist1A.append(h)
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Hn-A"] = self.Hlist1A

    def CalcHValuesB1(self):
        self.Hlist1B1 = []
        for i in range(self.n+1):
            b = i * self.circleangle
            if  b >= 90 and b <= 270 :
                h = Decimal(self.CalcH10(i))
            else:
                h = Decimal(self.CalcH11(i))
            self.Hlist1B1.append(h)
        self.valuedict["Hn-B1"] = self.Hlist1B1

    def CalcHValuesB2(self):
        self.Hlist1B2 = []
        for i in range(self.n+1):
            b = i * self.circleangle
            if  b >= 90 and b <= 270 :
                h = Decimal(self.CalcH20(i))
            else:
                h = Decimal(self.CalcH21(i))
            self.Hlist1B2.append(h)
        self.valuedict["Hn-B2"] = self.Hlist1B2


    def CalcLValuesA(self):
        self.Llist1A = []
        for i in range(self.n+1):
            l = self.l0 + self.Hlist1A[i]
            self.Llist1A.append(l)
        self.valuedict["Ln-A"] = self.Llist1A

    def CalcLValuesB1(self):
        self.Llist1B1 = []
        for i in range(self.n+1):
            l = self.l1 + self.Hlist1B1[i]
            self.Llist1B1.append(l)
        self.valuedict["Ln-B1"] = self.Llist1B1
        self.max_lvalue1 = max(self.Llist1B1)
        
    def CalcLValuesB2(self):
        self.Llist1B2 = []
        for i in range(self.n+1):
            l = self.l2 + self.Hlist1B2[i]
            self.Llist1B2.append(l)
        self.valuedict["Ln-B2"] = self.Llist1B2
        self.max_lvalue2 = max(self.Llist1B2)

    def CalcMValues(self):
        self.Mlist1 = [0]
        for i in range(self.n):
            self.Mlist1.append(self.M)
        self.valuedict["Mn"] = self.Mlist1


            
      

    def Draw(self):
        self.DrawMainLinesA()
        self.DrawMainLinesB1()
        self.DrawMainLinesB2()



    def DrawMainLinesA(self):
        self.GenerateMlinesA()
        self.GenerateLlinesA()
        self.GenerateCurveA()

    def DrawMainLinesB1(self):
        self.GenerateMlinesB1()
        self.GenerateLlinesB1()
        self.GenerateCurveB1()

    def DrawMainLinesB2(self):
        self.GenerateMlinesB2()
        self.GenerateLlinesB2()
        self.GenerateCurveB2()


    def GenerateMlinesA(self):
        self.mlinelistA = []
        line0 = self.Line(label = "A-M0")
        line0.Initialize4((self.a0,self.a1),0,0)
        self.mlinelistA.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "A-M%d"%(i+1))
            line1.Initialize5(self.mlinelistA[i].GetPoint2(), self.M,0)
            self.mlinelistA.append(line1)

    def GenerateMlinesB1(self):
        self.mlinelistB1 = []
        line0 = self.Line(label = "B1-M0")
        line0.Initialize4((self.a0,self.a1 + self.max_lvalue1 + self.l1),0,0)
        self.mlinelistB1.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "B1-M%d"%(i+1))
            line1.Initialize5(self.mlinelistB1[i].GetPoint2(), self.M,0)
            self.mlinelistB1.append(line1)

    def GenerateMlinesB2(self):
        self.mlinelistB2 = []
        line0 = self.Line(label = "B2-M0")
        line0.Initialize4((self.mlinelistB1[0].Getx1(),self.mlinelistB1[0].Gety1() + self.max_lvalue2 + self.l2),0,0)
        self.mlinelistB2.append(line0)
        for i in range(self.n):
            line1 = self.Line(label = "B2-M%d"%(i+1))
            line1.Initialize5(self.mlinelistB2[i].GetPoint2(), self.M,0)
            self.mlinelistB2.append(line1)


    def GenerateLlinesA(self):
        self.linelistA = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0  
            else:
                outline = 1
            line2 = self.Line(label = "A-L%d"%i,outline = outline)
            line2.Initialize5(self.mlinelistA[i].GetPoint2(),self.Llist1A[i],-90)
            self.linelistA.append(line2)


    def GenerateLlinesB1(self):
        self.linelistB1 = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0  
            else:
                outline = 1
            line2 = self.Line(label = "B1-L%d"%i,outline = outline)
            line2.Initialize5(self.mlinelistB1[i].GetPoint2(),self.Llist1B1[i],-90)
            self.linelistB1.append(line2)

    def GenerateLlinesB2(self):
        self.linelistB2 = [] # stores all the L lines
        for i in range(0,self.n+1):
            if i > 0 and i < self.n:
                outline = 0  
            else:
                outline = 1
            line2 = self.Line(label = "B2-L%d"%i,outline = outline)
            line2.Initialize5(self.mlinelistB2[i].GetPoint2(),self.Llist1B2[i],-90)
            self.linelistB2.append(line2)

                    
    def GenerateCurveA(self):
        self.curvelistA = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelistA[i - 1].GetPoint2(),self.linelistA[i].GetPoint2())
            self.curvelistA.append(line3)

    def GenerateCurveB1(self):
        self.curvelistB1 = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelistB1[i - 1].GetPoint2(),self.linelistB1[i].GetPoint2())
            self.curvelistB1.append(line3)

    def GenerateCurveB2(self):
        self.curvelistB2 = []
        for i in range(1,self.n+1):
            line3 = self.Line()
            line3.Initialize2(self.linelistB2[i - 1].GetPoint2(),self.linelistB2[i].GetPoint2())
            self.curvelistB2.append(line3)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Junction Piece Diameter"] = self.diameter #R
        self.dimensiondict["Free Height of pipe A"] = self.height0
        self.dimensiondict["Angle of Intersection for pipe B1"] = self.intersectionangle1
        self.dimensiondict["Free Height of pipe B1"] = self.height1
        self.dimensiondict["Angle of Intersection for pipe B2"] = self.intersectionangle2
        self.dimensiondict["Free Height of pipe B2"] = self.height2
        self.dimensiondict["Partition Number"] = self.n

    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetHeight0(values['Height0'])
            if not self.stop:
                self.SetIntersectionAngleB1(values["Angle B1"])
                if not self.stop:
                    self.SetHeight1(values['Height1'])
                    if not self.stop:
                        self.SetIntersectionAngleB2(values["Angle B2"])
                        if not self.stop:
                            self.SetHeight2(values["Height2"])
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
                self.ShowError("""Wrong Input "%s" for Junction Piece Diameter"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Junction Piece Diameter")



    def SetIntersectionAngleB1(self,value):
        if value:
            try:
                self.intersectionangle1 = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Angle of Intersection for pipe B1"""%value)
            else:
                if self.intersectionangle1 <= 0 or self.intersectionangle1 > 90:
                    self.stop = 1
                    self.ShowError(\
                                """Invalid input "%s" for Angle of Intersection for pipe B1.
                                   Angle of Intersection must be greater than 0
                                   and less than or equal to 90 """%\
                                               self.intersectionangle1)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Angle of Intersection")


    def SetIntersectionAngleB2(self,value):
        if value:
            try:
                self.intersectionangle2 = float(value)
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Angle of Intersection for pipe B2"""%value)
            else:
                if self.intersectionangle2 <= 0 or self.intersectionangle2 > 90:
                    self.stop = 1
                    self.ShowError(\
                                """Invalid input "%s" for Angle of Intersection for pipe B2.
                                   Angle of Intersection must be greater than 0
                                   and less than or equal to 90 """%\
                                               self.intersectionangle2)
                else:
                    self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Angle of Intersection for pipe B2")



    def SetHeight0(self,value):
        if value:
            try:
                self.height0 = float(value)
                if self.height0 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of pipe A"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Free Height of pipe A")


    def SetHeight1(self,value):
        if value:
            try:
                self.height1 = float(value)
                if self.height1 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of pipe B1"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Free Height of pipe B1")


    def SetHeight2(self,value):
        if value:
            try:
                self.height2 = float(value)
                if self.height2 <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Free Height of pipe B2"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Free Height of pipe B2")

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
