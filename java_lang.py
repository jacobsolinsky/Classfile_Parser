from collections import defaultdict
from numpy import array, ascontiguousarray
from typing import List, Union, NewType, Tuple
from byteconv import *
from classfileconsts import *
JType = NewType("Jtype", str)
ArrayType = NewType("ArrayType", Tuple[JType, int])
JTypeU = Union[JType, ArrayType]
MethodSignature = Tuple[List[JtypeU], Union[JtypeU, None]]

class ClassFile:
    magic = jhexbyte("CAFEBABE")
    def __init__(self, constants, methods, major = "0038", minor = "0000"):
        self.major = jhexbyte(major)
        self.minor = jhexbyte(minor)
        self.constant_pool: List[bytearray] = []
        self.Class_set = defaultdict()
        self.Fieldref_set = defaultdict()
        self.InterfaceMethodref_set = defaultdict()
        self.String_set = defaultdict()
        self.Integer_set =  defaultdict()
        self.Float_set = defaultdict()
        self.Long_set = defaultdict()
        self.Double_set = defaultdict()
        self.NameAndType_set = defaultdict()
        self.UtF8_set = defaultdict()
        self.MethodHandle_set = defaultdict()
        self.MethodType_set = defaultdict()
        self.InvokeDynamic_set = defaultdict()
    def create_const_Integer(self, value: int) -> int:
        tag = getconstant_pool_tag("Integer")
        value = jintbyte(value)
        self.constant_pool += tag + value
        return len(self.constant_pool) - 1
    def create_const_Long(self, value: int) -> int:
        tag = getconstant_pool_tag("Long")
        value = jlongbyte(value)
        self.constant_pool += tag + value
        retval = len(self.constant_pool) - 1
        self.constant_pool += [bytearray()]
        return retval
    def create_const_Float(self, value: float) -> int:
        tag = getconstant_pool_tag("Float")
        value = jfloatbyte(value)
        self.constant_pool += tag + value
        return len(self.constant_pool) - 1
    def create_const_Double(self, value: float) -> int:
        tag = getconstant_pool_tag("Double")
        value = jfloatbyte(value)
        self.constant_pool += tag + value
        retval =  len(self.constant_pool) - 1
        self.constantpool += [bytearray()]
        return retval
    def create_const_String(self, value: str) -> int:
        tag = getconstant_pool_tag("String")
        index = ju16byte(self.addUtf8(value))
        self.constant_pool += tag + index
        return len(self.constant_pool) - 1
    def create_const_Utf8(self, value: str):
        tag = getconstant_pool_tag("Utf8")
        stringbytes = jutf8byte(value)
        lengthbytes = ju16byte(len(stringbytes))
        self.constant_pool += tag + stringbytes + lengthbytes
        return len(self.constant_pool) - 1
    def create_const_Class(self, name: str) -> int:
        tag = getconstant_pool_tag("Class")
        name_index = ju16byte(self.addUtf8(name))
        self.constant_pool += tag + name_index
        return len(self.constant_pool) - 1
    def create_const_NameAndType(self, name: str, type_: JTypeU) -> int:
        tag = getconstant_pool_tag("Utf8")
        name_index = ju16byte(self.addUtf8(name))
        type_code = get_type_code(type_)
        descriptor_index = ju16byte(self.addUtf8(type_code))
        self.constant_pool += tag + name_index + descriptor_index
        return len(self.constant_pool) - 1
    def create_const_Fieldref(self, name: str, class_: str, type_: str) -> int:
        tag = getconstant_pool_tag("Fieldref")
        class_index = ju16byte(self.addClass(class_))
        name_and_type_index = ju16byte(self.addNameAndType(name, type_))
        self.constant_pool += tag + class_index + name_and_type_index
        return len(self.constant_pool) - 1
    def create_const_Methodref(self, name: str, class_:str) -> int:
        tag = getconstant_pool_tag("Methodref")
        class_index = ju16byte(self.addClass(class_))
        name_and_type_index = ju16byte(self.addNameAndType(name, type_))
        self.constant_pool += tag + class_index + name_and_type_index
        return len(self.constant_pool) - 1
    def create_const_InterfaceMethodref(self, name: str, class_:str) -> int:
        tag = getconstant_pool_tag("InterfaceMethodRef")
        class_index = ju16byte(self.addClass(class_))
        name_and_type_index = ju16byte(self.addNameAndType(name, type_))
        self.constant_pool += tag + class_index + name_and_type_index
        return len(self.constant_pool) - 1
    def create_const_MethodHandle(self,value) -> int:
        tag = getconstant_pool_tag("MethodHandle")

    def create_const_MethodType(self,value) -> int:
        tag = getconstant_pool_tag("MethodType")
        descriptor_code = get_method_code(value)
        descriptor_index = ju16byte(self.addUtf8(descriptor_code))
        self.constant_pool += tag + descriptor_index
        return len(self.constant_pool)-1
    def create_const_InvokeDynamic(self,value) -> int:
        tag = getconstant_pool_tag("InvokeDynamic")

    def addClass(self, classname) -> int:
    def addFieldref(self, fieldname, classname) -> int:
    def addMethodref(self, methodname, classname) -> int:

    def addInterfaceMethodref(self, value) -> int:
    def addString(self, value) -> int:

    def addInteger(self, value) -> int:
        return self.Integer_set[value]
    def addFloat(self, value) -> int:
    def addLong(self, value) -> int:
    def addDouble(self, value) -> int:
    def addNameAndType(self, value) -> int:
    def addUtf8(self, value) -> int:
        return self.Utf8_set[value]
    def addMethodHandle(self, value) -> int:
    def addMethodType(self, value) -> int:
    def addInvokeDynamic(self, value) -> int:


def makeclassstring(class_: str) -> str:
    if class_ in java_lang_classes:
        return "java/lang/" + class_

