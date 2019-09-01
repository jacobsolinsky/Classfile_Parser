from byteconv import *
from numpy import float32, float64

class TNumber():
    def eval(self):
        pass
class Integer(TNumber):
    def __init__(self, left):
        self.left = left
    def __str__(self):
        return f"Integer ({self.left})"
    def cast(self, type):
        if type == Float:
            return Float(self.left, "0")
    def eval(self):
        val = int(self.left)
        if val < 2*8:
            return getopbyte("bipush", (val).to_bytes(1, "big"))
        if val < 2*16:
            return getopbyte("bipush", (val).to_bytes(2, "big"))
        return ipush(val)
class Float(TNumber):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return f"Float ({self.left}.{self.right})"
    def cast(self, type):
        if type == Integer:
            return Integer(self.left)
    def eval(self):
        val = float32(self.left + "." + self.right)
        #check float format
        return (lpush(val))
class VarName:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"VarName ({self.name})"
class Operator:
    def __init__(self, symbol):
        self.symbol = symbol
    def __str__(self):
        return f"operator ({self.symbol})"
class Binop:
    def __init__(self):
        self.lterm = None
        self.rterm = None
        self.priority= 0
        self.termstack = None
        self.pos = None
    @property
    def termstack(self):
        return self.termstack
    @termstack.setter
    def termstack(self, termstack):
        self.termstack = termstack
    @property
    def pos(self):
        return self.pos
    @termstack.setter
    def pos(self, pos):
        self.pos = pos
    def update(self, left = None, right = None):
        self.lterm = left
        self.rterm = right
        if lterm and rterm:
            self.termstack.push(Term(self, self.lterm, self.rterm))
class Term:
    def __init__(self, core, lterm = None, rterm = None):
        self.core = core
        self.lterm = lterm
        self.rterm = rterm
        self.lop = lop
        self.rop = rop
        if self.lterm and self.rterm:
            self.lop = self.lterm.lop
            self.rop = self.rterm.rop
    def eval(self):
        retval =""
        if self.lterm and self.rterm:
            retval += self.lop.eval()
            retval += self.rop.eval()
        return retval + self.core.eval()
def econtains(a, b):
    if a == END:
        return a == b
    else:
        return a in b

class END:
    pass
