
from PageTemplateClass import*
from InputPageClass import* 

from TJunctionClass import* 
from SquareToCylinderClass import* 
from CylindricalPipeAtAnyAngleClass import * 
from YJunctionPieceClass import * 
from  CylinderCutAtAnyClass import * 
from ElbowPieceClass import * 
from OffsetPieceClass import * 

class TJunctionPage(PageTemplate):
    Count = 0
    def __init__(self,parent):
        TJunctionPage.Count +=1
        self.parent = parent
        self.category = "T-Junction Piece"
        self.classname = "Interpenetration Piece"
        
        self.name = "T-junction Interpenetration piece Project %d"% TJunctionPage.Count
        self.allow = 0
        self.inputnames = ["Diameter1","Diameter2","Height","Number"]
        self.displaynames = ["Interpenetrated\npipe Diameter ","Interpenetrating\npipe Diameter ",\
                             "Free Height of\nInterpenetrating pipe ","Partition Number "]
        self.displaynames2 = ["Interpenetrated pipe Diameter","Interpenetrating pipe Diameter",\
                              "Free Height of Interpenetrating pipe","Partition Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = TJunction(self,self.name)

#TJunctionPageClass end
############################################        

#SquareToCylinderPageClass begin
######################################################        
class SquareToCylinderPage(PageTemplate):
    Count = 0
    def __init__(self,parent):
        SquareToCylinderPage.Count +=1
        self.parent = parent
        self.category = "Square pipe Interpenetrating A Cylindrical pipe Vertically"
        self.classname = "Interpenetration Piece"
        self.name = "Square To Cylinder Interpenetration piece Project %d"% SquareToCylinderPage.Count
        self.allow = 0
        self.inputnames = ["Diameter1","Length","Height","Number"]#problem1
        self.displaynames = ["Interpenetrated\npipe Diameter: ","Interpenetrating\nsquare pipe length: ",\
                             "Free Height of\nInterpenetrating pipe: ","Partition Number: "]
        self.displaynames2 = ["Interpenetrated pipe Diameter","Interpenetrating square pipe length",\
                             "Free Height of Interpenetrating pipe","Partition Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = SquareToCylinder(self,self.name)

#SquareToCylinderPageClass end
##################################################

#CylindricalPipeAtAnyAnglePageClass begin
######################################################        
class CylindricalPipeAtAnyAnglePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        CylindricalPipeAtAnyAnglePage.Count +=1
        self.parent = parent
        self.category = "Interpenetration of Cylindrical Pipes At Any Angle"
        self.classname = "Interpenetration Piece"
        self.name = "Interpenetration of Cylindrical Pipe At Any Angle Project %d"% CylindricalPipeAtAnyAnglePage.Count
        self.allow = 0
        self.inputnames = ["Diameter1","Diameter2","Angle","Height","Number"]
        self.displaynames = ["Interpenetrated\npipe Diameter: ","Interpenetrating\npipe Diameter: ",\
                             "Angle of Interpenetration: ","Free Height of\nInterpenetrating pipe: ","Partition Number: "]

        self.displaynames2 = ["Interpenetrated pipe Diameter","Interpenetrating pipe Diameter",\
                              "Angle of Interpenetration","Free Height of Interpenetrating pipe",\
                              "Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = CylindricalPipeAtAnyAngle(self,self.name)


#CylindricalPipeAtAnyAnglePageClass end
####################################################        

#YJunctionPiecePageClass begin
################################################                                        
class YJunctionPiecePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        YJunctionPiecePage.Count +=1
        self.parent = parent
        self.category = "Y-Junction Piece"
        self.classname = "Interpenetration Piece"
        self.name = "Y-Junction Piece Project %d"% YJunctionPiecePage.Count
        self.allow = 0
        self.inputnames = ["Diameter",'Height0',"Angle B1",'Height1',"Angle B2","Height2","Number"]
        self.displaynames = ["Junction Piece Diameter: ","Free Height of pipe A: ",\
                             "Angle of Intersection\n for pipe B1:","Free Height of pipe B1: ",\
                             "Angle of Intersection\n for pipe B2:","Free Height of pipe B2: ",\
                             "Partition Number: "]

        self.displaynames2 = ["Junction Piece Diameter","Free Height of pipe A",\
                             "Angle of Intersection for pipe B1","Free Height of pipe B1",\
                             "Angle of Intersection for pipe B2","Free Height of pipe B2",\
                             "Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = YJunctionPiece(self,self.name)
#YJunctionPiecePageClass end
################################################################

#CylinderCutAtAnyPageClass begin
##########################################################################################

class CylinderCutAtAnyPage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        CylinderCutAtAnyPage.Count +=1
        self.parent = parent
        self.category = "Right Cylinder Cut Obliquely"
        self.classname = "Interpenetration Piece"
        self.name = "Right Cylinder Cut Obliquely Project %d"% CylinderCutAtAnyPage.Count
        self.allow = 0
        self.inputnames = ["Diameter",'Height',"Angle","Number"]
        self.displaynames = ["Cylinder Diameter: ","Cylinder Free Height: ",\
                             "Angle of Cut: ","Partition Number: "]

        self.displaynames2 = ["Cylinder Diameter","Cylinder Free Height",\
                             "Angle of Cut","Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = CylinderCutAtAny(self,self.name)

#CylinderCutAyAnyPageClass end
################################

#ElbowPieceClass begin
########################################################        
class ElbowPiecePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        ElbowPiecePage.Count +=1
        self.parent = parent
        self.category = "Elbow Piece"
        self.classname = "Interpenetration Piece"
        self.name = "Elbow Piece Project %d"% ElbowPiecePage.Count
        self.allow = 0
        self.inputnames = ["Diameter",'Height',"Angle","Number"]
        self.displaynames = ["Elbow Diameter: ","Elbow Free Height: ",\
                             "Elbow Angle: ","Partition Number: "]

        self.displaynames2 = ["Elbow Diameter","Elbow Free Height",\
                             "Elbow Angle","Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = ElbowPiece(self,self.name)

#ElbowPieceClass end
##########################################
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




class OffsetPiecePage(PageTemplate): 
    Count = 0
    def __init__(self,parent):
        OffsetPiecePage.Count +=1
        self.parent = parent
        self.category = "Offset Piece"
        self.classname = "Interpenetration Piece"
        self.name = "Offset Piece Project %d"% OffsetPiecePage.Count
        self.allow = 0
        self.inputnames = ["Diameter","Angle0","Height0","Angle1","Height1","Number"]
        self.displaynames = ["Offset Piece Diameter: ","Offset Piece Angle 1: ",\
                             "Offset Piece Free Height 1: ","Offset Piece Angle 2: ",\
                              "Offset Piece Free Height 2: ","Partition Number: "]

        self.displaynames2 = ["Offset Piece Diameter","Offset Piece Angle 1",\
                             "Offset Piece Free Height 1","Offset Piece Angle 2",\
                              "Offset Piece Free Height 2","Partition Number"]


        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = OffsetPiece(self,self.name)

