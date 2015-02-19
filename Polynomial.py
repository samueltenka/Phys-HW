class Polynomial:
    def __init__(self, coeffs=[0]):
        if isinstance(coeffs, list): self.coeffs = coeffs
        elif isinstance(coeffs, Polynomial): self.coeffs = coeffs.coeffs[:]
    def degree(self):
        return len(self.coeffs)-1
    def get(self, i):
        return self.coeffs[i] if 0<=i<=self.degree() else 0.0
    def __add__(self, other):
        if not isinstance(other, Polynomial): return self+Polynomial([other])
        return Polynomial([self.get(i)+other.get(i)
                           for i in range(max(self.degree(), other.degree())+1)])
    def __sub__(self, other): return self + other*(-1)
    def __rsub__(self, other): return self*(-1) + other
    def __neg__(self): return self*(-1)
    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            return self*Polynomial([other])
        return Polynomial([sum(self.get(j)*other.get(i-j) for j in range(i+1))
                           for i in range(self.degree()+other.degree()+1)])
    def __truediv__(self, other):
        if not isinstance(other, Polynomial): return self*(1.0/other)
    def derivative(self):
        return Polynomial([self.get(i)*i for i in range(1, self.degree()+1)])
    def integrate(self, C):
        return Polynomial([C]+[self.get(i)/(i+1) for i in range(0, self.degree()+1)])
    def evaluate(self, x):
        return sum(self.get(i)*x**i for i in range(self.degree()+1))
    def __str__(self):
        return ''.join(str(self.get(i)) + \
                       ('' if i==0 else 'x' if i==1 else 'x^'+str(i)) + \
                       (' + ' if i!=0 else '') \
                       for i in range(self.degree(), -1, -1))

def integ(poly, a=0, b=1):
    I = poly.integrate(C=0)
    return I.evaluate(b)-I.evaluate(a)


'''
## test:
A = Polynomial([1])
for n in range(1000):
    A = A.integrate(1)
print(integ(A)) ## e-1 = 1.7182818284590...
'''
