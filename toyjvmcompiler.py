from byteconv import *
from numpy import float32   #,float64


class TNumber:
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
        if val < 2 * 8:
            return getopbyte("bipush", (val).to_bytes(1, "big"))
        if val < 2 * 16:
            return getopbyte("sipush", (val).to_bytes(2, "big"))
        else:
            return getopbyte("ldc", Consref_Integer(val))
        # return ipush(val)




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
        return getopbyte("ldc", Consref_Float(val))



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
        self.priority = 0
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

    @pos.setter
    def pos(self, pos):
        self.pos = pos

    def update(self, lterm=None, rterm=None):
        self.lterm = lterm
        self.rterm = rterm
        if lterm and rterm:
            self.termstack.push(Term(self, self.lterm, self.rterm))


class Term:
    def __init__(self, core, lterm=None, rterm=None, lop=None, rop=None):
        self.core = core
        self.lterm = lterm
        self.rterm = rterm
        self.lop = lop
        self.rop = rop
        if self.lterm and self.rterm:
            self.lop = self.lterm.lop
            self.rop = self.rterm.rop

    def eval(self):
        retval = ""
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


class Lexer:
    NUMSTARTS = "0123456789"
    VARSTARTS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    VARALL = VARSTARTS + NUMSTARTS
    WHITESPACE = " \t\r\f"
    SYMSTARTS = "+-*/%^=<>()[]{}!&\n"
    ASSIGNSYMS = "+-*/&^|!-=<>"

    def __init__(self, instring):
        self.instring = instring
        self.words = []
        self.i = 0
        self.words = self.run()
        print(self.__str__())

    @property
    def ic(self):
        try:
            return self.instring[self.i]
        except:
            return END

    @property
    def lf(self):
        try:
            return self.instring[self.i + 1]
        except:
            return END

    def run(self):
        while True:
            if econtains(self.ic, self.NUMSTARTS):
                self.words.append(self.findnum())
                print(self.ic)
            elif econtains(self.ic, self.VARSTARTS):
                self.words.append(self.findvar())
            elif econtains(self.ic, self.SYMSTARTS):
                self.words.append(self.findsym())
            if econtains(self.ic, self.WHITESPACE):
                self.advance()
                continue
            if self.ic is END:
                return self.words
            raise Exception("Lexer Error")

    def advance(self):
        self.i += 1
        return self.ic

    def findnum(self):
        left = []
        right = None
        left.append(self.ic)
        while econtains(self.advance(), self.NUMSTARTS):
            left.append(self.ic)
        if self.ic == ".":
            if econtains(self.lf, self.NUMSTARTS):
                while econtains(self.advance(), self.NUMSTARTS):
                    right.append(self.ic)
        if right is None:
            return Integer(left)
        else:
            return Float(left, right)

    def findvar(self):
        name = self.ic
        while econtains(self.advance(), self.VARALL):
            name += self.ic
        return VarName(name)

    def findsym(self):
        symbol = self.ic
        print("ic", self.ic)
        print("lf", self.lf)
        self.advance()
        if econtains(symbol, self.ASSIGNSYMS) and self.ic == "=":
            symbol += self.ic
            self.advance()
            return Operator(symbol)
        if symbol == "/" and self.ic == "/":
            symbol += self.ic
            self.advance()
            if self.ic == "=":
                symbol += self.ic
                self.advance()
            return Operator(symbol)
        if symbol == "<" and self.ic == "<":
            symbol += self.ic
            self.advance()
            if self.ic == "=":
                symbol += self.ic
                self.advance()
            return Operator(symbol)
        if symbol == ">" and self.ic == ">":
            symbol += self.ic
            self.advance()
            if self.ic == "=":
                symbol += self.ic
                self.advance()
            return Operator(symbol)
        return Operator(symbol)

    def __str__(self):
        retval = "["
        for word in self.words:
            retval += word.__str__() + ", \n"
        retval += "]"
        return retval
# if __name__ == "__main__":
#    lexation = Lexer(sys.argv[1])
#   print(lexation.words)
