import math 

def DegtoRad(x):
    return math.pi* x/ 180
def RadtoDeg(x):
    return x * 180/ math.pi

def Cos(x):
    return math.cos(DegtoRad(x))

def Sin(x):
    return math.sin(DegtoRad(x))

def Cosec(x):
    return (1 / (Sin(x)))
def Cot(x):
    return (Cos(x)/Sin(x))
def Tan(x):
    return (Sin(x)/Cos(x))

def Atan(x):
    return RadtoDeg(math.atan(x))

def Acos(x):
    return RadtoDeg(math.acos(x))
def Asin(x):
    return RadtoDeg(math.asin(x))


def Decimal(x,place= 3):
    astring = "%."
    bstring = "%d"%place
    template = astring + bstring + "f"
    return float(template%x)


def CosineAngle(x,y,z):
    return   Acos(((pow(y,2)) + (pow(z,2)) - (pow(x,2)))/(2*y*z))
