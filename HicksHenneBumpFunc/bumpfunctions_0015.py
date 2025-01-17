import math

def f1(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.05))
    return pow(math.sin(t),4)

def f2(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.15))
    return pow(math.sin(t),4)

def f3(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.30))
    return pow(math.sin(t),4)

def f4(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.45))
    return pow(math.sin(t),4)

def f5(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.60))
    return pow(math.sin(t),4)

def f6(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.80))
    return pow(math.sin(t),4)

def f7(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.10))
    return pow(math.sin(t),4)

def f8(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.10))
    return pow(math.sin(t),4)

def f9(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.55))
    return pow(math.sin(t),4)

def f10(z):
    t=math.pi*pow(z,math.log(0.5)/math.log(0.80))
    return pow(math.sin(t),4)

class bumpfunc(object):
    def __init__(self):
        self.funcid=None

    def f(self,ind,z):
        if ind==0:
            return f1(z)
        if ind==1:
            return f2(z)
        if ind==2:
            return f3(z)
        if ind==3:
            return f4(z)
        if ind==4:
            return f5(z)
        if ind==5:
            return f6(z)
        if ind==6:
            return f7(z)
        if ind==7:
            return f8(z)
        if ind==8:
            return f9(z)
        if ind==9:
            return f10(z)
