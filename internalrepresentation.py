#The internal representation uses only ints, floats, and utf-8 strings as its atoms.
from byteconv import *
from classfileconsts import *
class Constant(object):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.constant_pool = None
        return instance
    def valinit(self, value, pos):
        self.value = value
        self.pos = pos
    def refinit(self, rcindex, pos):
        self.rcindex = cindex
        sel.pos = pos
    def refbytes(self):
        return ju16byte(self.rcindex)
    def refrefinit(self, rcindex1, rcindex2, pos):
        self.rcindex1 = rcindex1
        self.rcindex2 = rcindex2
        self.pos = pos

    def refrefbytes(self):
        return ju16byte(self.rcindex1) + ju16byte(self.rcindex2)
    def valrefinit(self, value, rcindex):
        self.value = value,
        self.rcindex = rcindex


    @property
    def tag(self):
        return type(self).__name__[9:]
    def tobytes(self):
        return getconstant_pool_tag(self.tag)

class CONSTANT_Class(Constant):
    def __init__(self, name_index):
        super().refinit(name_index)
    def tobytes(self):
        return super().tobytes() + super().refbytes()
class CONSTANT_Fieldref(Constant):
    def __init__(self, class_index, name_and_type_index):
        super().refrefinit(class_index, name_and_type_index)
    def tobytes(self):
        return super().tobytes() + super().refrefbytes()
class CONSTANT_Methodref(Constant):
    def __init__(self, class_index, name_and_type_index):
        super().refrefinit(class_index, name_and_type_index)
    def tobytes(self):
        return super().tobytes() + super().refrefbytes()
class CONSTANT_InterfaceMethodref(Constant):
    def __init__(self, class_index, name_and_type_index):
        super().refrefinit(class_index, name_and_type_index)
    def tobytes(self):
        return super().tobytes() + super().refrefbytes()
class CONSTANT_String(Constant):
    def __init__(self, stringindex):
        super().refinit(stringindex)
    def tobytes(self):
        return super().tobytes() + super().refbytes()

class CONSTANT_Integer(Constant):
    def __init__(self, value):
        super().valinit(value)
    def tobytes(self):
        return super().tobytes() + jintbyte(self.value)
class CONSTANT_Float(Constant):
    def __init__(self, value):
        super().valinit(value)
    def tobytes(self):
        return super().tobytes() + jfloatbyte(self.value)
class CONSTANT_Long(Constant):
    def __init__(self, value):
        super().valinit(value)
    def tobytes(self):
        return super().tobytes() + jlongbyte(self.value)
class CONSTANT_Double(Constant):
    def __init__(self, value):
        super().valinit(value)
    def tobytes(self):
        return super().tobytes() + jdoublebyte(self.value)
class CONSTANT_NameAndType(Constant):
    def __init__(self, name_index, descriptor_index):
        super().refrefinit()
    def tobytes(self):
        return super().tobytes() + super().refrefbytes()
class CONSTANT_Utf8(Constant):
    def __init__(self, length, value):
        self.length = length
        self.value = value
    def tobytes(self):
        return super().tobytes() + ju16byte(self.length) + jutf8byte(self.value)
class CONSTANT_MethodHandle(Constant):
    def __init__(self, reference_kind, reference_index):
        self.reference_kind = reference_kind
        self.reference_index = reference_index
    def tobytes(self):
        return super().tobytes + ju8byte(self.reference_kind) + ju16byte(self.reference_index)


class CONSTANT_MethodType(Constant):
    def __init__(self, descriptor_index):
        super().refinit(descriptor_index)
    def tobytes(self):
        return super().tobytes() + super().refbytes()
class CONSTANT_InvokeDynamic(Constant):
    def __init__(self), bootstrap_method_attribute_index, name_and_type_index:
        super().refrefinit(bootstrap_method_attribute_index, name_and_type_index)
    def tobytes(self):
        return super().tobytes() + super().refrefbytes()





class Opcode:
    def __init__(self, mnemonic):
        self.mnemonic = mnemonic
        self.pos = None
    def __str__(self):
        return "{:<15}".format(self.mnemonic)
    def addpos(self, pos):
        """This function is to be called once an operation's position in a method's code has been defined"""
        self.pos = pos
    def tobytes(self):
        return bytearray(getopbyte(self.mnemonic))
class LindexOp(Opcode):
    def __init__(self, mnemonic, lindex):
        super.__init__(mnemonic)
        self.lindex = lindex
    def __str__(self):
        return super().__str__() + f"{self.lindex}"
    def tobytes(self):
        return super().tobytes() + ju8byte(self.lindex)

class OpLine:
    def __init__(self, lineno: int, opcode: Opcode):
        self.lineno = lineno
        self.opcode = opcode
    def __str__(self):
        return f"{self.lineno}:  {self.opcode}"

class CindexOp(Opcode):
    def __init__(self, mnemonic, constant):
        super().__init__(mnemonic)
        self.constant = constant
    def __str__(self):
        return super().__str__() + f"{'#{:<15}'.format(self.constant.cindex)}" + f"//{self.constant}"
    def tobytes(self):
        return super().tobytes() + ju16byte(self.cindex)


class LCindexOp(CindexOp):
    def tobytes(self) -> bytes:
        super().tobytes() + ju8byte(self.cindex)
class BranchOp(CindexOp):
    def __init__(self, mnemonic, offset):
        super().__init(mnemonic)
        self.offset = offset
        self.absolute = None
    def addpos(self, pos):
        super().addpos(pos)
        self.absolute = self.offset + pos
    def __str__(self):
        return super().__str__() + f"{self.absolute}"
    def tobytes(self):
        return super().tobytes() +  jshortbyte(self.offset)
class WBranchOp(BranchOp):
    def __str__(self):
        return "{:<15}".format("wide " + self.mnemonic) + f"{self.absolute}"
    def tobytes(self):
        return super().super().tobytes() +  jintbyte(self.offset)
class LindexAndByteOp(LindexOp):
    def __init__(self, mnemonic, lindex, incint):
        super().__init__(mnemonic, lindex)
        self.incint = incint
    def __str__(self):
        return super().__str__ + f", {self.incint}"
    def tobytes(self):
        return super().tobytes() + ju8byte(self.incint)
class WLindexAndByteOp(LindexAndByteOp):
    def __str__(self):
        return "{:<15}".format("wide " + self.mnemonic) + f"{self.lindex}, {self.incint}"
    def tobytes(self):
        return super().super().tobytes() + ju16byte(self.lindex) + ju16byte(self.incint)
class WLindexOp(LindexOp):
    def __str__(self):
        return "{:<15}".format("wide " + self.mnemonic) + f"{self.lindex}"
    def tobytes(self):
        return super().super().tobytes() + ju16byte(self.lindex)
class ATypeOp:
    def __init__(self, mnemonic, atype):
        super().__init__(mnemonic)
        self.atype = atype
    def __str__(self):
        return super().__str__() + self.atype
    def tobytes(self) -> bytearray:
        return super().tobytes() + bytes.fromhex(primitivetypehex[self.atype])
class TableSwitchOp(Opcode):
    def __init__(self, mnemonic, default, min, max, offsets):
        super().__init__(mnemonic)
        self.default = default
        self.min = min
        self.max = max
        self.offsets = offsets
    def __str__(self):
        return super().__str__() + "{\n" + \
               "{:>15}".format("default: ") + str(self.default) + "\n" + \
               "{:>15}".format("min: ") + str(self.min) + "\n" + \
               "{:>15}".format("max: ") + str(self.max) + "\n" + \
               "".join(["{:>15}".format(str(self.min + i) + ": ") + str(self.offsets[i]) + "\n" for i in range(1 + self.max-self.min)]) + "}\n"
    def tobytes(self):
        offsetbytearr = bytearray()
        for offset in self.offsets:
            offsetbytearr += jintbyte(offset)
        return super().tobytes() + jintbyte(self.default) + jintbyte(self.min) + jintbyte(self.max) + offsetbytearr
class LookupSwitchOp(Opcode):
    def __init__(self, mnemonic, default, number, offsetpairs):
        super().__init__(mnemonic)
        self.default = default
        self.number = number
        self.offsetpairs = offsetpairs
    def __str__(self):
        return super().__str__() + "{" + r"\\" + str(self.number) + "\n" + \
               "".join(["{:>15}".format(str(offsetpair[0]) + ": ")  + str(offsetpair[1]) + "\n" for offsetpair in self.offsetpairs]) +\
                "{:>15}".format("default: ") + str(self.default)+ "\n}\n"
    def tobytes(self):
        offsetbytearr = bytearray()
        for match, offset in self.offsetpairs:
            offsetbytearr += jintbyte(match) + jintbyte(offset)
        return super().tobytes() + jintbyte(self.default) + ju32byte(self.count) +  offsetbytearr
