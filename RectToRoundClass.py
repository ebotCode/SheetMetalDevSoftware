from GraphGuiClass import* 
from MathUtils import* 
from LinkerClass import* 

import math 

class RectToRound:
    def __init__(self,parent,name):
        self.name = name
        self.parent = parent
        self.InitialiseCalcData()

        self.a0 = 400
        self.a1 = 500
        

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
        self.circleangle = 90.0/float(self.n)

        self.v = self.length/2
        self.u = self.breadth/2
        self.r = self.diameter/2 #+ (self.thickness/2)
        # calculate L values
        self.CalcL1()
        self.CalcL2()
        self.CalcL3()
        self.CalcL4()
        

        
        self.CalcPhi_U()
        self.CalcPhi_U2()
        self.CalcPhi_U3()
        self.CalcPhi_U4()
        self.CalcPhi_V()
        self.CalcPhi_V2()
        self.CalcPhi_V3()
        self.CalcPhi_V4()

        self.CalcMValues()
        self.CalcZValues()
        self.CalcYValues()
        self.CalcWValues()
        self.CalcXValues()

        self.CalcTheta1()
        self.CalcTheta2()
        self.CalcTheta3()
        self.CalcTheta4()

    def CalcM(self):
        self.M = Decimal(math.pi * self.diameter / (4*self.n),2)
        


        
    def CalcL1(self):
        self.l1 = Decimal(math.sqrt(pow((self.u + self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L1"] = self.l1

    def CalcL2(self):
        self.l2 = Decimal(math.sqrt(pow((self.v - self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L2"] = self.l2
    def CalcL3(self):
        self.l3 = Decimal(math.sqrt(pow((self.v + self.offsetx - self.r),2) + pow((self.height),2)))
        self.otherdict["L3"] = self.l3

    def CalcL4(self):
        self.l4 = Decimal(math.sqrt(pow((self.u - self.offsety - self.r),2) + pow((self.height),2)))
        self.otherdict["L4"] = self.l4



    def CalcPhi_V(self):
        self.phi_v = Atan(self.l1/(self.v + self.offsetx))


    def CalcPhi_V2(self):
        self.phi_v2 = Atan(self.l1/(self.v - self.offsetx))

    def CalcPhi_V3(self):
        self.phi_v3 = Atan(self.l4/(self.v - self.offsetx))

    def CalcPhi_V4(self):
        self.phi_v4 = Atan(self.l4/(self.v + self.offsetx))

        
    def CalcPhi_U(self):
        self.phi_u =  Atan(self.l2/(self.u + self.offsety))

    def CalcPhi_U2(self):
        self.phi_u2 =  Atan(self.l2/(self.u - self.offsety))

    def CalcPhi_U3(self):
        self.phi_u3 =  Atan(self.l3/(self.u + self.offsety))

    def CalcPhi_U4(self):
        self.phi_u4 =  Atan(self.l3/(self.u - self.offsety))


        
    def CalcZ(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcY(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v - self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))

    def CalcW(self,n):
        return Decimal(math.sqrt( pow((self.u + self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))
    def CalcX(self,n):
        return Decimal(math.sqrt( pow((self.u - self.offsety - (self.r* Sin(n * self.circleangle))),2) +\
                                  pow((self.v + self.offsetx - (self.r * Cos(n *self.circleangle))),2) +\
                                  pow((self.height),2)))


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
        self.Wlist1 = []
        self.Wlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcW(i))
            self.Wlist1.append(z)
        for i in range(self.n+1):
            self.Wlist2.append(self.Wlist1[-(i+1)])
        self.valuedict["W"] = self.Wlist1

    def CalcXValues(self):
        self.Xlist1 = []
        self.Xlist2 = []
        for i in range(self.n+1):
            z = Decimal(self.CalcX(i))
            self.Xlist1.append(z)
        for i in range(self.n+1):
            self.Xlist2.append(self.Xlist1[-(i+1)])
        self.valuedict["X"] = self.Xlist1


            

    def CalcDeltaAlpha(self,z1,z2):
        return   Acos(((pow(z1,2)) + \
                             (pow(z2,2)) - (pow((2*self.r*Sin(self.circleangle/2)),2)))/\
                             (2*z1*z2))


    def CalcTheta1(self):
        sum_delta = 0
        for i in range(len(self.Xlist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Xlist1[i],self.Xlist1[i+1]),2)
        
        self.theta1 = 180 - Decimal((self.phi_u4 + sum_delta + self.phi_v4),2)

                            
            

    def CalcTheta2(self):
        sum_delta = 0
        for i in range(len(self.Wlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1]),2)
        
        self.theta2 = 180 - Decimal((self.phi_v + sum_delta + self.phi_u3),2)


    def CalcTheta3(self):
        sum_delta = 0
        for i in range(len(self.Ylist1) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1]),2)
        
        self.theta3 = 180 - Decimal((self.phi_u + sum_delta + self.phi_v2),2)


    def CalcTheta4(self):
        sum_delta = 0
        for i in range(len(self.Zlist2) - 1):
            sum_delta += Decimal(self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1]),2)
        
        self.theta4 = 180 - Decimal((self.phi_v3 + sum_delta + self.phi_u2),2)


        

    def Draw(self):
        self.DrawMainLines()



    def DrawMainLines(self):
        self.line1 = self.Line(label = "length")
        self.line1.Initialize4((self.a0,self.a1),self.length,0)
        
        
        self.line2 = self.Line(label = "breadth")
        self.line2.Initialize5(self.line1.GetPoint2(),self.breadth,-self.theta2)

        
        self.line3 = self.Line()
        self.line3.Initialize5(self.line2.GetPoint2(),\
                  self.v + self.offsetx,-(self.theta1 + self.theta2))


        

        self.line4 = self.Line(label = "L4")
        self.line4.Initialize5(self.line3.GetPoint2(),\
                        self.l4,-(90 + self.theta1 + self.theta2))
        

        self.line5 = self.Line()
        self.line5.Initialize5(self.line1.GetPoint1(),\
                            self.breadth,180 + self.theta3)

        self.line6 = self.Line()
        self.line6.Initialize5(self.line5.GetPoint2(),\
                        self.v - self.offsetx, 180 + self.theta3 + self.theta4)

        
        self.line7 = self.Line(label = "L4")
        self.line7.Initialize5(self.line6.GetPoint2(),\
                     self.l4,270 + self.theta3 + self.theta4)


        self.line8 = self.Line(label = "L2")
        self.line8.Initialize4(\
            self.line5.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l2,270 + self.theta3) 



        self.line9= self.Line(label = "L1")
        self.line9.Initialize4((self.line1.Getx1()+self.v - self.offsetx,self.line1.Gety1()),\
                          self.l1,270)        

        self.line10= self.Line()
        self.line10.Initialize4(\
            self.line2.GetDividePoint(self.u + self.offsety,self.u - self.offsety),\
                          self.l3,-(90+self.theta2))        

        self.line11= self.Line(label = "X%d"%(self.n),outline = 0)
        self.line11.Initialize2(self.line2.GetPoint2(),self.line4.GetPoint2())

        self.line12= self.Line(label = "X0",outline = 0)
        self.line12.Initialize2(self.line2.GetPoint2(),self.line10.GetPoint2())       
##
        self.line13 = self.Line(label = "W0",outline = 0)
        self.line13.Initialize2(self.line1.GetPoint2(),self.line10.GetPoint2())

        self.line14 = self.Line(label = "W%d"%(self.n),outline = 0)
        self.line14.Initialize2(self.line1.GetPoint2(),self.line9.GetPoint2())


        self.line15 = self.Line(label = "Y%d"%(self.n),outline = 0)
        self.line15.Initialize2(self.line1.GetPoint1(),self.line9.GetPoint2())
        
        
        self.line16 = self.Line(label = "Y0",outline = 0)
        self.line16.Initialize2(self.line1.GetPoint1(),self.line8.GetPoint2())
        

        
        self.line17 = self.Line(label = "Z0",outline = 0)
        self.line17.Initialize2(self.line5.GetPoint2(),self.line8.GetPoint2())


        self.line18 = self.Line(label = "Z%d"%(self.n),outline = 0)
        self.line18.Initialize2(self.line5.GetPoint2(),self.line7.GetPoint2())

        self.GenerateZlines()
        self.GenerateYlines()
        self.GenerateWlines()
        self.GenerateXlines()


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
        templinelist.append(self.line18)
        b = len(self.Zlist2) - 2

        for i in range(len(self.Zlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Zlist2[i],self.Zlist2[i+1])
                                    
            angleinc = -(180 - ((self.phi_v3 + self.theta3 + self.theta4) + sum_delta))
            anglelist1.append(angleinc)

            line = self.Line(label = "Z%d"%(b - i),outline = 0)
            line.Initialize5(self.line5.GetPoint2(),\
                     self.Zlist2[i+1],angleinc)
            templinelist.append(line)
            
        templinelist.append(self.line17)

        self.Zlines.append(templinelist)


    def GenerateYlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line16)
        for i in range(len(self.Ylist1) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Ylist1[i],self.Ylist1[i+1])
                                    
            angleinc = -(180  - ((self.theta3 + self.phi_u) + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "Y%d"%(i+1),outline = 0)
            line.Initialize5(self.line1.GetPoint1(),\
                     self.Ylist1[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line15)
        self.Ylines.append(templinelist)




    def GenerateWlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line14)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Wlist2) - 2):
            
            sum_delta += self.CalcDeltaAlpha(self.Wlist2[i],self.Wlist2[i+1])
                                    
            angleinc = -(180  - (self.phi_v + sum_delta))
            anglelist1.append(angleinc)
            
            line = self.Line(label = "W%d"%(b - i),outline = 0)
            line.Initialize5(self.line1.GetPoint2(),\
                     self.Wlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line13)
        self.Wlines.append(templinelist)



        
    def GenerateXlines(self):
        sum_delta = 0
        anglelist1 = []
        templinelist = []
        templinelist.append(self.line11)
        b = len(self.Zlist2) - 2
        for i in range(len(self.Xlist2) - 2):
            sum_delta += self.CalcDeltaAlpha(self.Xlist2[i],self.Xlist2[i+1])
                                    
            angleinc = -(self.theta1 + self.theta2 + self.phi_v4 + sum_delta)
            anglelist1.append(angleinc)
            
            line = self.Line(label = "X%d"%(b - i),outline = 0)

            line.Initialize5(self.line2.GetPoint2(),\
                     self.Xlist2[i+1],angleinc)

            templinelist.append(line)
            
        templinelist.append(self.line12)
        self.Xlines.append(templinelist)


    def GetDataToSave(self):
        return self.dimensiondict

    def SetName(self,name):
        self.name = name
        self.Gui.SetName(self.name)

    def ReceiveInput(self):
        xoffset = 0#75 #float(raw_input("Enter the xoffset distance: "))
        yoffset = 0#75  #float(raw_input("Enter the yoffset distance: "))
        self.SetOffsetx(xoffset)
        self.SetOffsety(yoffset)
        self.dimensiondict["Diameter"] = self.diameter
        self.dimensiondict["Length"] = self.length
        self.dimensiondict["Breadth"] = self.breadth
        self.dimensiondict["Height"] = self.height
        self.dimensiondict["Facet Number"] = self.n
        
    def SetInput(self,values):
        self.SetDiameter(values ["Diameter"])
        if not self.stop:
            self.SetLength(values["Length"])
            if not self.stop:
                self.SetBreadth(values["Breadth"])
                if not self.stop:
                    self.SetHeight(values["Height"])
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
                self.ShowError("""Wrong Input "%s" for Length"""%value)
            else:
                self.stop = 0

        else:
            self.stop = 1
            self.ShowError("No Value in Length")
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
                self.stop = 1
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

    def ShowError(self,message):
        messagetitle = "Input Error!! @ "+ self.name
        self.errordialog.ShowErrorMessage(messagetitle,message)
            
    def SetOffsetx(self,offset):
        self.offsetx = offset
    def SetOffsety(self,offset):
        self.offsety = offset
    def SetErrorDialog(self,reference):
        self.errordialog = reference
    
    def GetLinkerObject(self):
        return self.linkerobject
