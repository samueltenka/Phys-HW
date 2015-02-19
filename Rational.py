from math import ceil

def gcd(a, b): ## has sign of b
    while b!=0:
        a,b = b,a%b ## no interference
    return a

def goodness(n, d, flt):
    return abs(n/d - flt)*d*d
def approximate(flt, tol=0.05):
    if flt<0:
        n,d=approximate(-flt,tol)
        return -n,d
    int_part, flt_part = int(flt), flt-int(flt)
    nlow,dlow, nhigh,dhigh = 0,1, 1,1
    while True:
        if goodness(nlow, dlow, flt_part)<tol:
            return (nlow+dlow*int_part),dlow
        elif goodness(nhigh, dhigh, flt_part)<tol:
            return (nhigh+dhigh*int_part),dhigh
        nmed,dmed = nlow+nhigh, dlow+dhigh
        if flt_part<nmed/dmed: nhigh,dhigh = nmed,dmed
        else: nlow,dlow = nmed,dmed


class Rational:
    def __init__(self, num=None, den=None, flt=None):
        self.num, self.den = approximate(flt) if flt is not None else (num, den)
    def __float__(self):
        return self.num/self.den
    def standardize(self):
        g = gcd(self.num, self.den)
        self.num //= g
        self.den //= g
    def __add__(self, other):
        if not isinstance(other, Rational): return self+Rational(flt=other)
        return Rational(self.num*other.den + self.den*other.num,
                        self.den*other.den)
    def __neg__(self): return Rational(-self.num, self.den)
    def __radd__(self, other): return self + other
    def __rsub__(self, other): return self*(-1) + other
    def __sub__(self, other): return self + (-other)
    def __mul__(self, other):
        if not isinstance(other, Rational): return self*Rational(flt=other)
        return Rational(self.num*other.num,
                        self.den*other.den)
    def __rmul__(self, other): return self * other
    def __truediv__(self, other):
        if not isinstance(other, Rational): return self/Rational(flt=other)
        return Rational(self.num*other.den,
                        self.den*other.num)
    def __rtruediv__(self, other):
        return Rational(self.den, self.num)*other
    def __str__(self):
        return str(self.num)+('' if self.den==1 else '/'+str(self.den))


'''
## testing:
pq = Rational(20, 30)
print(pq-pq)

print(gcd(4, 5)) ## 1
print(gcd(40, 50)) ## 10
print(gcd(4, 6)) ## 2
print(gcd(4, 8)) ## 4
print(gcd(-4, 8)) ## 4
print(gcd(4, -8)) ## -4
print(gcd(-4, -8)) ## -4
print(gcd(4, 0)) ## 4
print(gcd(0, 8)) ## 8
'''
