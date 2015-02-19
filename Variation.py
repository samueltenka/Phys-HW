from Polynomial import Polynomial, integ
from Rational import Rational
from Matrix import Matrix
L = 1
m = 1
h = 1

x = Polynomial([0, 1])
f1 = x*(-x+L)
fs = {0:f1,
      1:f1*f1/(L*L),
      2:f1*(-x+L/2)/L,
      3:f1*f1*(-x+L/2)/(L*L*L)}

def fdot(a, b):
    return integ(a*b)
'''orthonormalize:'''
for i in range(4):
    print(i, fs[i])
    for j in range(i):
        fs[i] = fs[i] - fs[j]*fdot(fs[i], fs[j])/fdot(fs[j], fs[j])
    fs[i] = fs[i]/fdot(fs[i], fs[i])**0.5
    print(i, fs[i])

def Ham(poly):
    return poly.derivative().derivative()*(-h*h/(2*m))

H = [[fdot(fs[i], Ham(fs[j]))
      for j in range(4)] for i in range(4)]
S = [[fdot(fs[i], fs[j])
      for j in range(4)] for i in range(4)]
H = Matrix(4, 4, H)
S = Matrix(4, 4, S)

print(S)

for ev in (H.all_eigvects()):
    p = Polynomial([0])
    for i in range(4):
        p = p+fs[i]*ev[i]
    print("P", p)
