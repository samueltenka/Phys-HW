from random import random
from Rational import Rational


def vdot(v, w):
    return sum(vi*wi for vi,wi in zip(v,w))
def vparallel_to(v, w):
    norm = vdot(v, w)/vdot(w, w)
    return [wi*norm for wi in w]
def vperp_to(v, w):
    vpar = vparallel_to(v, w)
    return [vi-vpari for vi,vpari in zip(v,vpar)]
def vnorm(v):
    return vdot(v,v)**0.5
def vnormalize(v):
    norm = vnorm(v)
    return [vi/norm for vi in v]

class Matrix:
    def __init__(self, rows, cols, entries):
        self.num_rows, self.num_cols = rows, cols
        self.entries = entries if entries else\
            [[0.0 for j in range(cols)] for i in range(rows)] ## list of rows
    def transpose(self):
        new_entries = [[self.entries[i][j]
                        for i in range(self.num_rows)]
                       for j in range(self.num_cols)]
        return Matrix(self.num_cols, self.num_rows, new_entries)
    def __mul__(self, other):
        if not isinstance(other, Matrix):
            new_entries = [[self.entries[i][j]*other
                            for j in range(self.num_cols)]
                           for i in range(self.num_rows)]
        elif self.num_cols==other.num_rows:
            tother = other.transpose()
            new_entries = [[vdot(self.entries[i], tother.entries[j])
                            for j in range(other.num_cols)]
                           for i in range(self.num_rows)]
        return Matrix(self.num_rows, other.num_cols, new_entries)
    def __add__(self, other):
        if self.num_rows==other.num_rows and \
           self.num_cols==other.num_cols:
            new_entries = [[self.entries[i][j] + other.entries[i][j]
                            for j in range(other.num_cols)]
                           for i in range(self.num_rows)]
            return Matrix(self.num_rows, other.num_cols, new_entries)
    def __str__(self):
        return ''.join(''.join(str(self.entries[i][j])+' '
                               for j in range(self.num_cols))+'\n'
                       for i in range(self.num_rows))
    def normalize(self):
        s = sum(self.entries[i][j]**2
                for j in range(self.num_cols)
                for i in range(self.num_rows))**0.5
        if s<1E-16: return
        self.entries = [[self.entries[i][j]/s
                         for j in range(self.num_cols)]
                        for i in range(self.num_rows)]
    def project_out_cols(self, vects):
        if not vects: return
        self.transpose()
        for v in vects:
            self.entries = [vperp_to(col, v) for col in self.entries] ## cols represent rows (thru transpose)
        self.transpose()
    def biggest_eigvect(self, other_eigvects=[]):
        A = self
        for i in range(100): ## raise matrix to power 1024^10 ~ 10^30
            A = A+A*A
            A.normalize()
            A.project_out_cols(other_eigvects)
        v = [[random()] for i in range(A.num_cols)]
        ev = [c[0] for c in (A*Matrix(A.num_cols, 1, v)).entries]
        if vnorm(ev)<1E-12:
            ev = [vi[0] for vi in v]
            for oev in other_eigvects:
                ev = vperp_to(ev, oev)
        return ev
    def all_eigvects(self):
        evs = []
        for n in range(self.num_rows):
            evs.append(vnormalize(self.biggest_eigvect(other_eigvects=evs)))
        return evs


'''
## testing:

def ratform(x):
    pq = Rational(flt=x)
    return str(pq)
def squareform(x):
    pq = Rational(flt=x*x)
    return ('-' if x<0 else '+') + 'sqrt('+str(pq)+')'
def best_display(x):
    ds = [str(x), ratform(x), squareform(x)]
    return min((len(d), d) for d in ds)[1]
def vstr(v):
    return ''.join(best_display(vi)+' ' for vi in v)

def test(M):
    print(M)
    for ev in M.all_eigvects():
        print('[ '+vstr(ev)+']')
    print()
    print()

test(Matrix(2, 2, [[2, 1],
                   [1, 2]]))

test(Matrix(3, 3, [[1, 0, 0],
                   [0, 1.1, 0],
                   [0, 0, 1.2]]))

test(Matrix(3, 3, [[0, 1, 0],
                   [1, 0, 1],
                   [0, 1, 0]]))
'''
