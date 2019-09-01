from lexclass import Binop
from byteconv import getopbyte
def Plus_(type_):
    return getopbyte("iadd")
def Minus(type_):
    return getopbyte("isub")
def Times(type_):
    return getopbyte("imul")
def Truediv(type_):
    return getopbyte("fdiv")
def Intdiv(type_):
    return getopbyte("idiv")
def Power(type_):
    pass
def Xor(type_):
    return getopbyte("ixor")
def And_(type_):
    return getopbyte("iand")
def Or_(type_):
    return getopbyte("ior")
def Shleft(type_):
    return getopbyte("ishl")
def Shright(type_):
    return getopbyte("ishr")
def Lthan(type_):
    return getopbyte("if_icmplt", (4).to_bytes(2, "big")) + \
           getopbyte("iconst_1") + \
           getopbyte("goto", (1).to_bytes(2, "big")) + \
           getopbyte("iconst_0")
def Gthan(type_):
    return getopbyte("if_icmpgt", (4).to_bytes(2, "big")) + \
           getopbyte("iconst_1") + \
           getopbyte("goto", (1).to_bytes(2, "big")) + \
           getopbyte("iconst_0")
def Lthaneq(type_):
    return getopbyte("if_icmple", (4).to_bytes(2, "big")) + \
           getopbyte("iconst_1") + \
           getopbyte("goto", (1).to_bytes(2, "big")) + \
           getopbyte("iconst_0")
def Gthaneq(type_):
    return getopbyte("if_icmpge", (4).to_bytes(2, "big")) + \
           getopbyte("iconst_1") + \
           getopbyte("goto", (1).to_bytes(2, "big")) + \
           getopbyte("iconst_0")
def Eq(type_):
    return getopbyte("if_icmpeq", (4).to_bytes(2, "big")) + \
           getopbyte("iconst_1") + \
           getopbyte("goto", (1).to_bytes(2, "big")) + \
           getopbyte("iconst_0")
def Noteq(type_):
    return getopbyte("if_icmpne", (4).to_bytes(2, "big")) + \
           getopbyte("iconst_1") + \
           getopbyte("goto", (1).to_bytes(2, "big")) + \
           getopbyte("iconst_0")
binopstable = {"+":Plus_,
"-":Minus,
"*":Times,
"/":Truediv,
"//":Intdiv,
"**":Power,
"^":Xor,
"&":And_,
"|":Or_,
">>":Shleft,
"<<":Shright,
"<":Lthan,
">":Gthan,
"<=":Lthaneq,
">=":Gthaneq,
"==":Eq,
"!=":Noteq,
}
class Employee(object):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.salary = 3000
        print(instance)
        print(instance.salary)
        return instance
class LowEmployee(Employee, object):
    def __init__(self, name):
        self.name = name
        
import types
def editf(a, b):
    c = 5
    d = 6
    return a + b + c + d       



class kwargint:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
