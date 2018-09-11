from PageTemplateClass import*

from RectToRoundClass import * 
from RectToRoundObliqueClass import * 
from RectToRoundOff1Class import * 
from RectToRoundOff2Class import * 
from ConicalFrustrumClass import * 
from InputPageClass import * 

class RectToRoundPage(PageTemplate):
    Count = 0
    def __init__(self,parent):
        RectToRoundPage.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round Transition Piece"
        self.classname = "Transition Piece"
        
        self.name = "RectRoundPage Project %d"% RectToRoundPage.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height","Facet number"]
        self.displaynames = ["Diameter: ","Length: ","Breadth: ","Height: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Length","Breadth","Height","Facet Number"]
        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRound(self,self.name)

        

            
class RectToRoundOff1Page(PageTemplate):
    Count = 0
    def __init__(self,parent):
        RectToRoundOff1Page.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round One Way offset Transition Piece"
        self.classname = "Transition Piece"
        
        self.name = "Rectangular To Round One Way offset Project %d"% RectToRoundOff1Page.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height","Offset distance","Facet number"]
        self.displaynames = ["Diameter: ","Length: ","Breadth: ","Height: ","Offset distance: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Length","Breadth","Height","Offset distance","Facet Number"]
        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRoundOff1(self,self.name)
        
        

class RectToRoundOff2Page(PageTemplate):
    Count = 0
    def __init__(self,parent):
        RectToRoundOff2Page.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round Two Way offset Transition Piece"
        self.classname = "Transition Piece"
        
        self.name = "Rectangular To Round Two Way offset Project %d"% RectToRoundOff2Page.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height",\
                           "Offset distance x","Offset distance y","Facet number"]
        self.displaynames = ["Diameter: ","Length: ","Breadth: ","Height: ",\
                             "Offset distance x: ","Offset distance y: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Length","Breadth","Height",\
                             "Offset distance x","Offset distance y","Facet Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRoundOff2(self,self.name)



class RectToRoundObliquePage(PageTemplate):

    Count = 0
    def __init__(self,parent):
        RectToRoundObliquePage.Count +=1
        self.parent = parent
        self.category = "Rectangular to Round Oblique Plane"
        self.classname = "Transition Piece"
        
        self.name = "Rectangular to Round Oblique plane Project %d"% RectToRoundObliquePage.Count
        self.allow = 0
        self.inputnames = ["Diameter","Length","Breadth","Height",\
                           "Inclination","Facet number"]
        self.displaynames = ["Diameter: ","Bevel Length: ","Breadth: ","Height: ",\
                            "Vertical Inclination: ","Facet Number: "]
        self.displaynames2 = ["Diameter","Bevel Length","Breadth","Height",\
                            "Vertical Inclination","Facet Number"]

        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = RectToRoundOblique(self,self.name)


class ConicalFrustumPage(PageTemplate):

    Count = 0
    def __init__(self,parent):
        ConicalFrustumPage.Count +=1
        self.parent = parent
        self.category = "Conical Frustum"
        self.classname = "Transition Piece"
        self.name = "Conical Frustum Project %d"% ConicalFrustumPage.Count
        self.allow = 0
        self.inputnames = ["Top diameter","Base diameter","Height","Facet number"]
        self.displaynames = ["Top Diameter: ","Base Diameter: ","Height: ","Facet Number: "]
        self.displaynames2 = ["Top Diameter","Base Diameter","Height","Facet Number"]
        
        self.inputpageobj = InputPageClass(self,self.displaynames,self.inputnames,self.displaynames2)
        self.brain = ConicalFrustum(self,self.name)



