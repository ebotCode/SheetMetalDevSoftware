from GraphGuiClass import* 
from MathUtils import* 
from LinkerClass import* 

import math 
class RectToRoundOblique:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()
        
        self.a0 = 150
        self.a1 = 700

        self.thickness = 1.0
        
        self.SetLinkerObject()
        self.SetLineClass()
        self.Gui = GraphGui(self)

    def InitialiseCalcData(self):
        self.stop = 0
        self.Zlines = []
        self.Ylines = []
        self.Wlines = []
        self.Xlines = []
        self.Zulines = []

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
        self.circleangle = 90.0/float(self.n)

        self.v = (self.length/2)
        self.vprime = (self.length/2)*Sin(self.inclination)
        self.hprime = self.height - (self.length*Cos(self.inclination))
        self.u = self.breadth/2
        self.r = self.diameter/2 #+ (self.thickness/2)
        # calculate L values. Only compute L5

        self.CalcL3()
        self.CalcL5()

        self.CalcMValues()
        self.CalcZValues()
        self.CalcYValues()
        self.CalcWValues()
        self.CalcXValues()

        
        self.CalcPhi_U()
        self.CalcPhi_U2()
        self.CalcPhi_U3()
        self.CalcPhi_U4()
        self.CalcPhi_V()
        self.CalcPhi_V2()
        self.CalcPhi_V3()
        self.CalcPhi_V4()
        self.CalcPhi_V5()


        self.CalcTheta1()
        self.CalcTheta2()
        self.CalcTheta3()
        self.CalcTheta4()
        
    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter / (4*self.n),2)
        self.otherdict["M"] = self.M


    def CalcL3(self):
        self.l3 = Decimal(math.sqrt(pow((self.vprime - self.r),2) + pow((self.hprime),2)))
        self.otherdict["L3"] = self.l3


    def CalcL5(self):
        self.l5 = Decimal(math.sqrt(pow((self.vprime - self.r),2) + pow((self.height),2)))
        self.otherdict["L5"] = self.l5


    def CalcPhi_V(self):
        self.phi_v = CosineAngle(self.Ylist1[-1],self.Zlist1[-1],2*self.v)
        

    def CalcPhi_V2(self):
        self.phi_v2 = CosineAngle(self.Zlist1[-1],self.Ylist1[-1],2*self.v)

    def CalcPhi_V3(self):
        self.phi_v3 = self.phi_v2

    def CalcPhi_V4(self):
        self.phi_v4 = self.phi_v


    def CalcPhi_V5(self):
        self.phi_v5 = CosineAngle(2*self.v,self.Ylist1[-1],self.Zlist1[-1])


        
    def CalcPhi_U(self):
        self.phi_u =  Atan(self.l5/self.u)


    def CalcPhi_U2(self):
        self.phi_u2 =  Atan(self.l3/self.u)


    def CalcPhi_U3(self):
        self.phi_u3 =  self.phi_u2

    def CalcPhi_U4(self):
        self.phi_u4 =  self.phi_u


        
    def CalcZ(self,n):
        return Decimal(math.sqrt( pow((self.u - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.vprime - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcY(self,n):
        return Decimal(math.sqrt( pow((self.u - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.vprime - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.hprime),2)))

    def CalcW(self,n):
        return self.CalcY(n)        #Since Yn  = Wn
    
    def CalcX(self,n):
        return self.CalcZ(n)        # since Zn = Xn


    def CalcMValues(self):
        self.CalcM()
        self.Mlist1  = []
        self.Mlist2 = []
        m = 0
        for i in range(self.n+1):
            if i == 0:
                m = 0
            else:
                m += self.M
            self.Mlist1.append(m)
        for i in range(self.n+1):
            self.Mlist2.append(self.Mlist1[-(i+1)])
        self.valuedict["M"] = self.Mlist1


    def CalcZValues(self):
        self.Zlist1 = []
        self.Zlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcZ(i))
            self.Zlist1.append(z)
        for i in range(self.n+1):
            self.Zlist2.append(self.Zlist1[-(i+1)])
        self.valuedict["N"] = range(self.n+1)
        self.valuedict["Z"] = self.Zlist1


    def CalcYValues(self):
        self.Ylist1 = []
        self.Ylist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcY(i))
            self.Ylist1.append(z)
        for i in range(self.n+1):
            self.Ylist2.append(self.Ylist1[-(i+1)])
        self.valuedict["Y"] = self.Ylist1


    def CalcWValues(self):
        self.Wlist1 = self.Ylist1
        self.Wlist2 = self.Ylist2
        self.valuedict["W"] = self.Wlist1


    def CalcXValues(self):
        self.Xlist1 = self.Zlist1
        self.Xlist2 = self.Zlist2
        self.valuedict["X"] = self.Xlist1


            

    def CalcDeltaAlpha(self,z1,z2):
        return   Acos(((pow(z1,2)) + \
                             (pow(z2,2)) - (pow((2*self.r*Sin(self.circleangle/2)),2)))/\
                             (2*z1*z2))
    


    def CalcTheta1(self):
        sum_delta = 0
        for i in range(len(self.Xlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1]),2)
        
        self.theta1 = 180 - Decimal((self.phi_v4 + sum_delta + self.phi_u4),2)

                            
            

    def CalcTheta2(self):
        sum_delta = 0
        for i in range(len(self.Wlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Wlist1[i],self.Wlist1[i+1]),2)
        
        self.theta2 = 180 - Decimal((self.phi_v3 + sum_delta + self.phi_u3),2)



    def CalcTheta3(self):
        sum_delta = 0
        for i in range(len(self.Ylist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Ylist2[i],self.Ylist2[i+1]),2)
        
        self.theta3 = 180 - Decimal((self.phi_v2 + sum_delta + self.phi_u2),2)



    def CalcTheta4(self):
        sum_delta = 0
        for i in range(len(self.Zlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Zlist1[i],self.Zlist1[i+1]),2)
        
        self.theta4 = 180 - Decimal((self.phi_v + sum_delta + self.phi_u),2)



        

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.line1 = self.Line()
        self.line1.Initialize4((self.a0,self.a1),self.length,0)
        
        
        self.line2 = self.Line()
        self.line2.Initialize5(self.line1.GetPoint2(),self.breadth,-self.theta3)

        self.line3 = self.Line()
        self.line3.Initialize5(self.line2.GetPoint2(),\
                  self.length,-(self.theta2 + self.theta3))


        self.line4 = self.Line()
        self.line4.Initialize5(self.line3.GetPoint2(),\
                        self.u,-(self.theta3 + self.theta1 + self.theta2))
##        
##
        self.line5 = self.Line()
        self.line5.Initialize5(self.line4.GetPoint2(),\
                            self.l5,-(90 + self.theta3 + self.theta2 + self.theta1))
##
        self.line6 = self.Line()
        self.line6.Initialize5(self.line1.GetPoint1(),\
                        self.u, -(180 - self.theta4))
##
##        
        self.line7 = self.Line()
        self.line7.Initialize5(self.line6.GetPoint2(),\
                     self.l5,270 + self.theta4)
##
##
##
##
####
##
##
        self.line9= self.Line()
        self.line9.Initialize5(self.line2.GetPoint2(),\
                     self.Wlist1[-1],-(self.phi_v3 + self.theta2 + self.theta3))       
##
        self.line11= self.Line()
        self.line11.Initialize5(self.line1.GetPoint2(),\
                     self.Ylist1[0],-(self.theta2 + self.phi_u2))      
##
        self.line13= self.Line()
        self.line13.Initialize5(self.line1.GetPoint1(),\
                     self.Zlist1[-1],-self.phi_v)
##
        self.line14= self.Line()
        self.line14.Initialize5(self.line1.GetPoint1(),\
                     self.Zlist1[0],-(180-(self.theta4 + self.phi_u)))      
##
        self.line15= self.Line()
        self.line15.Initialize5(self.line3.GetPoint2(),\
                     self.Xlist1[0],-(self.phi_u4 +self.theta1 + self.theta2 + self.theta3))     
##        
##
        self.line8= self.Line()
        self.line8.Initialize2(self.line3.GetPoint2(),self.line9.GetPoint2())


        self.line10= self.Line()
        self.line10.Initialize2(self.line2.GetPoint2(),self.line11.GetPoint2())

        self.line12= self.Line()
        self.line12.Initialize2(self.line1.GetPoint2(),self.line13.GetPoint2())       
####
##        

        

##        # all main lines end here. from here we begin lines that
##        #may vary in number
        self.GenerateZlines()
        self.GenerateYlines()
        self.GenerateWlines()
        self.GenerateXlines()
##
        for i in range(len(self.Zlines)):
            for j in range(len(self.Zlines[0]) - 1):
                line = self.Line()
                line.Initialize2(self.Zlines[i][j].GetPoint2(),\
                                 self.Zlines[i][j+1].GetPoint2())
                line2 = self.Line()
                line2.Initialize2(self.Ylines[i][j].GetPoint2(),\
                                 self.Ylines[i][j+1].GetPoint2())
                line3 = self.Line()
                line3.Initialize2(self.Wlines[i][j].GetPoint2(),\
                                 self.Wlines[i][j+1].GetPoint2())

                line4 = self.Line()
                line4.Initialize2(self.Xlines[i][j].GetPoint2(),\
                                 self.Xlines[i][j+1].GetPoint2())
                
            


    def GenerateZlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line14)

        for i in range(len(self.Zlist1) - 1):
            sum_delta += self.CalcDeltaAlpha(self.Zlist1[i],self.Zlist1[i+1])
                                    
            angleinc = -(180 - (self.phi_u + self.theta4 + sum_delta))
            anglelist1.append(angleinc)

            line = self.Line(label = "Z%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint1(),\
                     self.Zlist1[i+1],angleinc)
            templinelist.append(line)
            
        templinelist.append(self.line13)

        self.Zlines.append(templinelist)


    def GenerateYlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line11)
        for i in range(len(self.Ylist1) - 1):
            sum_delta += self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1])
                                    
            angleinc =  - (self.theta3 +self.phi_u2 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "Y%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint2(),\
                     self.Ylist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line12)
        self.Ylines.append(templinelist)




    def GenerateWlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line9)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Wlist2) - 1):
            
            sum_delta += self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1])
                                    
            angleinc = - (self.phi_v3 + self.theta2 + self.theta3+sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "W%d"%(b - i),outline = 0)
            line.Initialize5(self.line2.GetPoint2(),\
                     self.Wlist2[i+1],angleinc)


            templinelist.append(line)
            
        templinelist.append(self.line10)
        self.Wlines.append(templinelist)



        
    def GenerateXlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line15)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Xlist1) - 1):
            sum_delta += self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1])
                                    
            angleinc = -(self.theta1 + self.theta2 + self.theta3 + self.phi_u4 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "X%d"%(b - i),outline = 0)

            line.Initialize5(self.line3.GetPoint2(),\
                     self.Xlist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line8)
        self.Xlines.append(templinelist)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)


    def ReceiveInput(self):
        self.dimensiondict["Diameter"] = self.diameter
        self.dimensiondict["Bevel Length"] = self.length
        self.dimensiondict["Breadth"] = self.breadth
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n
        self.dimensiondict["Vertical Inclination"] = self.inclination
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetLength(values["Length"])
            if not self.stop:
                self.SetBreadth(values["Breadth"])
                if not self.stop:
                    self.SetHeight(values["Height"])
                    if not self.stop:
                        self.SetInclination(values["Inclination"])
                        if not self.stop:
                            self.SetFacetNumber(values["Facet number"])
            
    def SetLength(self,value):
        if value:
            try:
                self.length = float(value)
                if self.length <= 0:
                    raise ValueError

            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Bevel Length"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Bevel Length")
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
            self.ShowError("No Value in Diameter")


    def SetBreadth(self,value):
        if value:
            try:
                self.breadth = float(value)
                if self.breadth <= 0:
                    raise ValueError
            except ValueError:
                self.stop = 1
                self.ShowError("""Wrong Input "%s" for Breadth"""%value)
            else:
                self.stop = 0
        else:
            self.stop = 1
            self.ShowError("No Value in Breadth")


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
                self.ShowError("""Invalid Input "%s" for Facet Number"""% value)
            else:
                    
                if value2 > 10 or value2 < 3:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Facet Number\n valid range 3 to 10"""% str(value2))
                    
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
    def SetInclination(self,value):
        if value:
            try:
                value2 = float(value)
            except ValueError:
                self.ShowError("""Invalid Input "%s" for Inclination to the vertical"""% value)
            else:
                    
                if abs(value2) > 90 or value2 <= 0:
                    self.stop = 1
                    self.ShowError("""Invalid Input "%s" for Vertical Inclination\n valid range +0 to +90"""% str(value2))
                    
                else:
                    self.stop = 0
                    self.inclination = value2
        else:
            self.stop = 1
            self.ShowError("No value for Vertical Inclination")

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)


    def GetLinkerObject(self):
        return self.linkerobject
    def SetScale(self):
        self.linkerobject.SetScale(4,4)
    def SetErrorDialog(self,reference):
        self.errordialog = reference
