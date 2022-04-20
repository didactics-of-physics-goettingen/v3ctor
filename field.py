from math import sqrt
import sympy as sy
from sympy.calculus.singularities import singularities
import scipy as sc
import scipy.integrate as sc_int
import math

class VectorField2d():

    def  __init__(self,fieldstring1,fieldstring2):
        if fieldstring1== '':
            fieldstring1 = '0'
        if fieldstring2== '':
            fieldstring2 = '0'
        self.Fx = sy.S(fieldstring1)
        self.Fy = sy.S(fieldstring2)
        self.F = (self.Fx,self.Fy)
        self.x, self.y = sy.symbols(('x','y'))

    def __str__(self):
        return f"F(x,y)=({self.Fx}, {self.Fy})"

    def __repr__(self):
        return str(self)

    def divergence(self):
        return sy.diff(self.Fx,self.x)+sy.diff(self.Fy,self.y)

    def divergence_at(self,x,y):
        return self.divergence().evalf(5, subs={self.x : x, self.y : y})

    def flux(self,x0,x1,y0,y1):
        div_func = sy.lambdify([self.x,self.y],self.divergence())
        return sc_int.nquad(div_func, [[x0,x1],[y0,y1]], opts=[self.singularities(),{},{},{}])[0]

    def curl(self):
        return sy.diff(self.Fy,self.x)-sy.diff(self.Fx,self.y)

    def curl_at(self,x,y):
       return self.curl().evalf(5, subs={self.x : x, self.y : y})

    def induction(self,x0,x1,y0,y1):
        curl_func = sy.lambdify([self.x,self.y],self.curl())
        result = sc_int.nquad(curl_func, [[x0,x1],[y0,y1]], opts=[self.singularities(),{},{},{}])
        return result[0] 

    def length(self,x,y):
        try:
            leng = math.sqrt((self.Fx.evalf(5, subs={self.x : x, self.y : y}))**2+(self.Fy.evalf(5, subs={self.x : x, self.y : y}))**2)
        except ZeroDivisionError:
            leng = 0
        return leng

    def singularities(self):
        return {'x': list(singularities(self.Fx,self.x)) + list(singularities(self.Fy,self.x)),
                'y': list(singularities(self.Fy,self.y)) + list(singularities(self.Fx,self.y))
                }

    def point_in_singularity(self,x1,y1):
        for s_x in self.singularities()['x']:
            if x1 == s_x.evalf(5, subs={self.x:x1, self.y:y1}):
                return True
        for s_y in self.singularities()['y']:
            if x1 == s_y.evalf(5, subs={self.x:x1, self.y:y1}):
                return True
        return False
    

# if __name__ == "__main__":
#     Field = VectorField2d('x/(x**2+y**2)**(1/2)','y/(x**2+y**2)**(1/2)')
#     print(Field)
#     print(Field.length(3,3))
#     print(Field.divergence())
#     print(Field.singularities())
#     print(Field.flux(0,0,1,1))
#     Field2 = VectorField2d('1/(x+y)','y')
#     print(Field2.singularities())
#     print(Field2.point_in_singularity(3,-3))

    