#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 19:16:35 2019

@author: jacobsolinsky
"""
from byteconv import getopbyte, getopname
from commonutilities import invdict
from byteconv import javabyteparsedict
from collections import OrderedDict
registeredclasses = {}
import codeprinter
import struct
import functools

class EXEC:
    def __init__(self, string):
        self.string = string
class CHOOSE: pass
class Trackspos:
    def __init__(self, file):
        self.file = file
        self.pos = 0
    def read(self, amount):
        self.pos += amount
        return self.file.read(amount)
    def write(self, value):
        self.pos += len(value)
        self.file.write(value)
class M(type):
    """This metaclass assumes a flat namespace"""
    def __new__(meta, classname, bases, classDict):
        for name in ["__init__", "parse", "writebytes", "increment", "__getattribute__", "setonup"]:
            addname(name, classname, classDict, bases)
        if bases:
            if bases[0].__dict__.get("construction") and classDict.get("construction"):
                if bases[0].construction.chooseable:
                    olddict = bases[0].construction.components.copy()
                    for key, value in classDict["construction"].components.items():
                        olddict[key] = value
                    classDict["construction"].components = olddict
        if classname in codeprinter.printableclasses:
            classDict["__str__"] = codeprinter.printableclasses[classname].__str__
            if classname[0:9] == "CONSTANT_":
                classDict["ministr"] = codeprinter.printableclasses[classname].ministr
        thing = type.__new__(meta, classname, bases, classDict)
        registeredclasses[thing.__name__] = thing
        return thing
def addname(name, classname, classDict, bases):
        if name =="parse" and classname[0:3] == "op_" and "parse" not in classDict:
            classDict[name] =  eval(name)
        if not (any([name in base.__dict__ for base in bases]) or (name in classDict)):
            classDict[name] = eval(name)
def increment(self):
        self.setonup("_i", self._i + 1)
        
def __init__(self, container):
        self.container = container

def parse(self):
        """This function is used to implement declarative byte parsing"""
        for key, value in self.construction.statements.items():
            if type(value) == CHOOSE:
                thing = self.choose()(self)
                return thing.parse()
            if type(value) == EXEC:
                exec(value.string)
                continue
            if type(value) == str:
                value = registeredclasses[value]
            startpos = self.file.pos
            self.__dict__[key] = value(self).parse()
            endpos = self.file.pos
            if not (hasattr(value, "atomic") and value.atomic):
                self.__dict__[key].startpos = startpos
                self.__dict__[key].endpos = endpos
        return self



def writebytes(self):
        """each bytes method itself writes to the file being written"""
        for key, value in self.construction.components.items():
            if type(value) == str:
                value = registeredclasses[value]
            if hasattr(value, "atomic") and value.atomic:
                value(self).writebytes(self.__getattribute__(key))
            else:
                self.__getattribute__(key).wstartpos = self.outputfile.pos
                self.__getattribute__(key).writebytes()
                self.__getattribute__(key).wendpos = self.outputfile.pos
def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except:
            return object.__getattribute__(object.__getattribute__(self, "container"), "__getattribute__")(item)

def setonup(self, item, value):
        try:
            v = self.__dict__[item]
            self.__dict__[item] = value
        except KeyError:
            try:
                self.__dict__[item]
            except:
                pass
            self.container.setonup(item, value)

def nullparse(self):
        return self

class ConstructionMeta(type):
    def __new__(meta, classname, bases, classDict):
        components = OrderedDict()
        statements = OrderedDict()
        classDict["chooseable"] = False

        for key, value in classDict.items():
            if key in ("__module__", "__qualname__", "__main__", "chooseable"):
                continue
            if type(value == str):
                pass
                #value = registeredclasses[value]
            if type(value) not in (EXEC, CHOOSE):
                components[key] = value
            if type(value) == CHOOSE:
                classDict["chooseable"] = True
            statements[key] = value
        classDict["components"] = components
        classDict["statements"] = statements
        return type.__new__(meta, classname, bases, classDict)
class Array(metaclass = M):
    def __new__(cls, dype, length, _i = 0):
        return M("ArrayKind", (), {"parse": cls.parse,
                                  "dype": dype,
                                  "_length": length,
                                  "setonup":setonup,
                                  "__getattribute__":cls.__getattribute__,
                                  "__init__":cls.subinit,
                                  "_i":_i,
                                  "writebytes":cls.writebytes,
                                  "atomic":True})
    def subinit(self, container):
            self.container = container
            self._i = self._i
            if type(self.dype) == str:
                self.dype = registeredclasses[self.dype]
            self.length = eval(self._length)
        
    def parse(self):
            retval = {}
            while self._i < self.length:
                self.startpos = self.file.pos
                parsed = self.dype(self).parse()
                self.endpos = self.file.pos
                thisindex = self._i
                parsed.increment()
                retval[thisindex] = parsed
            return retval
    def writebytes(self, values):
            for value in values.values():
                value.writebytes()
class ThreeWayDict(metaclass = M):
    atomic = True
    def __init__(self, container):
        self.container = container
    def parse(self):
        value = self.dype(self).parse()
        return self.bytes2internal(value)
    def writebytes(self, key):
        self.dype(self).writebytes(self.internal2bytes(key))
    @classmethod
    def __str__(cls, key):
        return cls.internal2string(key)
    @property
    def internal2bytedict(self):
        try:
            return self.__dict__["_internal2bytedict"]
        except AttributeError:
            self._internal2bytedict = invdict(self.byte2internaldict)
            return self._internal2bytedict
    @property
    def internal2stringdict(self):
        try:
            return self.__dict__["_internal2stringdict"]
        except AttributeError:
            self._internal2stringdict = invdict(self.string2internaldict)
            return self._internal2stringdict
    def bytes2internal(self, key):
        return self.bytes2internaldict[key]
    def internal2bytes(self, key):
        try:
            return self.__dict__["internal2bytedict"][key]
        except KeyError:
            self.__dict__["internal2bytedict"] = invdict(self.bytes2internaldict)
            return self.__dict__["internal2bytedict"][key]
    def internal2string(self, key):
        return self.internal2stringdict[key]
    def string2internal(self, key):
        return self.string2byteinternaldict[key]
class ClassFile(metaclass = M):
    class fixedwidth(metaclass = M):
        atomic = True
        def parse(self):
            return struct.unpack(self._dtype, self.file.read(self._width))[0]
        def writebytes(self, value):
            self.outputfile.write(struct.pack(self._dtype, value))
        @staticmethod
        def __str__(value):
            return str(value)
        
    def __init__(self, filepath = None):
        if filepath:
            with open(filepath, "rb") as f:
                self.file = Trackspos(f)
                self.filepath = filepath
                self.parse()
                del self.file
    def writetofile(self, filepath):
        with open(filepath, "wb+") as f:
            self.outputfile = Trackspos(f)
            self.outputfilepath = filepath
            self.writebytes()
    @staticmethod
    def addprinters():
        codeprinter.S.addstr()
        
    class Flags(metaclass = M):
        atomic = True
        @classmethod
        def __init__(self, container):
            self.container = container
        def returnsetbits(cls, bitfield: int):
            retval = []
            for power in range(0, cls.dype._width * 8):
                comp = 2 ** power
                if comp & bitfield:
                    retval.append(power)
            return retval
        def parse(self):
            bitfield = self.dype(self).parse()
            flagnumbers = self.returnsetbits(bitfield)
            retval = []
            for flagnumber in flagnumbers:
                retval.append(self.num2internaldict[flagnumber])
            return retval
        @property
        def internal2numdict(self):
            try:
                return self.__dict__["_internal2numdict"]
            except KeyError:
                self._internal2numdict = invdict(self.num2internaldict)
                return self._internal2numdict
        def writebytes(self, keys):
            flagnumbers = [self.internal2numdict[key] for key in keys]
            retval = 0
            for flagnumber in flagnumbers:
                retval += 2 ** flagnumber
            self.dype(self).writebytes(retval)

    class u1(fixedwidth, metaclass = M):
        _dtype = ">B"
        _width = 1

    class u2(fixedwidth, metaclass = M):
        _dtype = ">H"
        _width = 2

    class u4(fixedwidth, metaclass = M):
        _dtype = ">I"
        _width = 4

    class byte(fixedwidth, metaclass = M):
        _dtype = ">b"
        _width = 1

    class short(fixedwidth, metaclass = M):
        _dtype = ">h"
        _width = 2

    class int(fixedwidth, metaclass = M):
        _dtype = ">i"
        _width = 4

    class long(fixedwidth, metaclass = M):
        _dtype = ">q"
        _width = 8

    class float(fixedwidth, metaclass = M):
        _dtype = ">f"
        _width = 4


    class double(fixedwidth, metaclass = M):
        _dtype = ">d"
        _width = 8

    class utf8(metaclass = M):
        atomic = True
        def parse(self):
            return self.file.read(self.length).decode("utf-8")
        @staticmethod
        def __str__(arg):
            return str(arg)
        def writebytes(self, arg):
            self.outputfile.write(arg.encode('utf8'))

    class tag(ThreeWayDict, metaclass = M):
        dype = registeredclasses["u1"]
        bytes2internaldict = {
            7: "Class",
            9: "Fieldref",
            10: "Methodref",
            11: "InterfaceMethodref",
            8: "String",
            3: "Integer",
            4: "Float",
            5: "Long",
            6: "Double",
            12: "NameAndType",
            1: "Utf8",
            15: "MethodHandle",
            16: "MethodType",
            18: "InvokeDynamic"
        }
    class cp_info(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            tag = "tag"
            _ = CHOOSE()
        def choose(self):
            return registeredclasses["CONSTANT_" + self.tag + "_info"]
        def increment(self):
            self.setonup("_i", self._i + 1)
        
    class constant_index(u2, metaclass = M):
        atomic = False
        class construction(metaclass = ConstructionMeta):
            index = "u2"


        @property
        def value(self):
            return self.constant_pool[self.index]
        

    class CONSTANT_Class_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            name_index = "constant_index"


    class CONSTANT_Fieldref_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            class_index = "constant_index"
            name_and_type_index = "constant_index"


    class CONSTANT_Methodref_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            class_index = "constant_index"
            name_and_type_index = "constant_index"


    class CONSTANT_InterfaceMethodref_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            class_index = "constant_index"
            name_and_type_index = "constant_index"

        
    class CONSTANT_String_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            string_index = "constant_index"


    class CONSTANT_Integer_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            int = "int"

        
    class CONSTANT_Float_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            float = "float"

    class CONSTANT_Long_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            long = "long"
        def increment(self):
            self.setonup("_i", self._i + 2)



    class CONSTANT_Double_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
             double = "double"
        def increment(self):
            self.setonup("_i", self._i + 2)

        
    class CONSTANT_NameAndType_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            name_index = "constant_index"
            descriptor_index = "constant_index"


    class CONSTANT_Utf8_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            length = "u2"
            utf8 = "utf8"

    class reference_kind(metaclass = M):
        dype = registeredclasses["u1"]
        bytes2internaldict = {
            1: "REF_getField",
            2: "REF_getStatic",
            3:  "REF_putField",
            4:  "REF_putStatic",
            5: "REF_invokeVirtual",
            6: "REF_invokeStatic",
            7: "REF_invokeSpecial",
            8:"REF_newInvokeSpecial",
            9: "REF_invokeInterface"
        }

    class CONSTANT_MethodHandle_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            reference_kind = "reference_kind"
            reference_index = "constant_index"


    class CONSTANT_MethodType_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            descriptor_index = "constant_index"


    class CONSTANT_InvokeDynamic_info(cp_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            bootstrap_method_attr_index ="attribute_index"
            name_and_type_index = "constant_index"


    class class_or_interface_access_flags(Flags, metaclass = M):
        dype = registeredclasses["u2"]
        num2internaldict = {
            0:"PUBLIC",
            4:"FINAL",
            5:"SUPER",
            9:"INTERFACE",
            10:"ABSTRACT",
            12:"SYNTHETIC",
            13:"ANNOTATION",
            14:"ENUM"
        }

    class field_access_flags(Flags, metaclass = M):
        dype = registeredclasses["u2"]
        num2internaldict = {
            0:"PUBLIC",
            1:"PRIVATE",
            2:"PROTECTED",
            3:"STATIC",
            4:"FINAL",
            6:"VOLATILE",
            7:"TRANSIENT",
            12:"SYNTHETIC",
            14:"ENUM"
        }
    class method_access_flags(Flags, metaclass = M):
        dype = registeredclasses["u2"]
        num2internaldict = {
            0:"PUBLIC",
            1:"PRIVATE",
            2:"PROTECTED",
            3:"STATIC",
            4:"FINAL",
            5:"SYNCHRONIZED",
            6:"BRIDGE",
            7:"VARARGS",
            8:"NATIVE",
            10:"ABSTRACT",
            11:"STRICT",
            12:"SYNTHETIC",
        }
    class inner_class_access_flags(Flags, metaclass = M):
        dype = registeredclasses["u2"]
        num2internaldict = {
            0: "PUBLIC",
            1: "PRIVATE",
            2: "PROTECTED",
            3: "STATIC",
            4: "FINAL",
            9:"INTERFACE",
            10:"ABSTRACT",
            12:"SYNTHETIC",
            13:"ANNOTATION",
            14:"ENUM"
        }
    class construction(metaclass = ConstructionMeta):
        magic = 'u4'
        minor_version = 'u2'
        major_version = 'u2'
        constant_pool_count = 'u2'
        constant_pool = Array("cp_info", "self.constant_pool_count", 1)
        access_flags = "class_or_interface_access_flags"
        this_class = "constant_index"
        super_class = "constant_index"
        interfaces_count = "u2"
        interfaces = Array("constant_index", "self.interfaces_count")
        fields_count = "u2"
        fields = Array("field_info", "self.fields_count")
        methods_count = "u2"
        methods = Array("method_info", "self.methods_count")
        attributes_count = "u2"
        attribute_info = Array("attribute", "self.attributes_count")
        
    class attribute(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            attribute_name_index = "constant_index"
            attribute_length = "u4"
            _ = CHOOSE()
        def choose(self):
            return registeredclasses[self.attribute_name_index.value.utf8 + "_attribute"]
    
    @property
    @functools.lru_cache
    def method_name_list(self):
        retval = []
        for method in self.methods:
            retval.append(method.name_index.value.utf8)
        return retval
    
    @property
    @functools.lru_cache
    def field_name_list(self):
        retval = []
        for field in self.fields:
            retval.append(field.name_index.value.utf8)
        return retval
    
    @property
    @functools.lru_cache
    def attribute_name_list(self):
        retval = []
        for attribute in self.attribute_info:
            retval.append(attribute.attribute_name_index.value.utf8)
        return retval
    
    def getattribute(self, attributename):
        try:
            return self.attribute_info[self.attribute_name_list.index(attributename)]
        except ValueError:
            pass
    
    class field_info(metaclass = M):
        def increment(self):
            self.setonup("_i", self._i + 1)
        class construction(metaclass = ConstructionMeta):
            access_flags = "field_access_flags"
            name_index = "constant_index"
            descriptor_index = "constant_index"
            attributes_count = "u2"
            attributes = Array("attribute", "self.attributes_count")
            
    class method_info(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            access_flags = "method_access_flags"
            name_index = "constant_index"
            descriptor_index = "constant_index"
            attributes_count = "u2"
            attributes = Array("attribute", "self.attributes_count")
            
        class exception_table_entry(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                start_pc = "operation_index"
                end_pc = "operation_index"
                handler_pc = "operation_index"
                catch_type = "constant_index"
            
    class StackMapTable_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            number_of_entries = "u2"
            stackmaptable = Array("stack_map_frame", "self.number_of_entries")
        
    class stack_map_frame(metaclass=M):
        _offset = "u2"
        class construction(metaclass = ConstructionMeta):
            frame_type = "u1"
            _ = CHOOSE()
        def choose(self):
            ft = self.frame_type
            if ft <= 63:
                return registeredclasses["same_frame"]
            elif ft <=127:
                return registeredclasses["same_locals_1_stack_item_frame"]
            elif ft <247:
                raise Exception("invalid stack map frame type")
            elif ft == 247:
                return registeredclasses["same_locals_1_stack_item_frame_extended"]
            elif ft <= 250:
                return registeredclasses["chop_frame"]
            elif ft == 251:
                return registeredclasses["same_frame_extended"]
            elif ft <= 254:
                return registeredclasses["append_frame"]
            elif ft ==  255:
                return registeredclasses["full_frame"]
    class same_frame(stack_map_frame, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            _ = EXEC("self.offset_delta = self.frame_type")

    class same_locals_1_stack_item_frame(stack_map_frame, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            _ = EXEC("self.offset_delta = self.frame_type - 64")
            stack = Array("verification_type_info", "1")

            
    class same_locals_1_stack_item_frame_extended(stack_map_frame, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            offset_delta = "u2"
            stack = Array("verification_type_info", "1")
    
    class chop_frame(stack_map_frame, metaclass=M):
        class construction(metaclass = ConstructionMeta):
            offset_delta = "u2"
            
    class same_frame_extended(stack_map_frame, metaclass=M):
        class construction(metaclass = ConstructionMeta):
            offset_delta = "u2"
            
    class append_frame(stack_map_frame, metaclass=M):
        class construction(metaclass = ConstructionMeta):
            offset_delta = "u2"
            locals = Array("verification_type_info", "self.frame_type-251")

    class full_frame(stack_map_frame, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            offset_delta = "u2"
            number_of_locals = "u2"
            locals = Array("verification_type_info", "self.number_of_locals")
            number_of_stack_items = "u2"
            stack = Array("verification_type_info", "self.number_of_stack_items")
    class verification_type_info_tag(ThreeWayDict, metaclass = M):
        dype = registeredclasses["u1"]
        bytes2internaldict ={0:"Top",
                 1:"Integer",
                 2:"Float",
                 3:"Long",
                 4:"Double",
                 5:"Null",
                 6:"UninitializedThis",
                 7:"Object",
                 8:"Uninitialized"
                 }
    class verification_type_info(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            itemtag = "verification_type_info_tag"
            _3 = CHOOSE()
        def choose(self):
            return registeredclasses[self.itemtag + "_variable_info"]
    class Top_variable_info(verification_type_info, metaclass = M): 
        def parse(self):
            return self
    class Integer_variable_info(verification_type_info, metaclass = M): 
        def parse(self):
            return self
    class Float_variable_info(verification_type_info, metaclass = M): 
        def parse(self):
            return self
    class Long_variable_info(verification_type_info, metaclass = M): 
        def parse(self):
            return self
    class Double_variable_info(verification_type_info, metaclass = M): 
        def parse(self):
            return self
    class Null_variable_info(verification_type_info, metaclass = M): 
        def parse(self):
            return self
    class UninitializedThis_variable_info(verification_type_info, metaclass = M): 
        def parse(self):
            return self
    class Object_variable_info(verification_type_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            cpool_index = "constant_index"
    class Uninitialized_variable_info(verification_type_info, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            offset = "u2"
    class ConstantValue_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            constantvalue_index = "constant_index"
    class codearr(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            _ = EXEC("self.startbyte = self.file.pos")
            codearr = Array("operation", "self.code_length")
        def writebytes(self):
            self.wstartbyte = self.outputfile.pos
            writebytes(self)
    class Code_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            max_stack = "u2"
            max_locals = "u2"
            code_length = "u4"
            code = "codearr"
            exception_table_length = "u2"
            exception_table = Array("exception_table_entry", "self.exception_table_length")
            attributes_count = "u2"
            attributes = Array("attribute", "self.attributes_count")
    class Exceptions_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            number_of_exceptions = "u2"
            exception_index_table = Array("constant_index", "self.number_of_exceptions")
    
    class InnerClasses_attribute(attribute, metaclass=M):
        class inner_class_info(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                inner_class_info_index = "constant_index"
                outer_class_info_index = "constant_index"
                inner_name_index = "constant_index"
                inner_class_access_flags = "inner_class_access_flags"
        class construction(metaclass = ConstructionMeta):
            number_of_classes = "u2"
            classes = Array("inner_class_info", "self.number_of_classes")
    class EnclosingMethod_attribute(attribute, metaclass=M):
        class construction(metaclass = ConstructionMeta):
            class_index = "constant_index"
            method_index = "constant_index"
    class Synthetic_attribute(attribute, metaclass = M):
        def parse(self):
            return self
    
    class Signature_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            signature_index = "constant_index"
    
    class SourceFile_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            signature_index = "constant_index"
    
    class SourceDebugExtension_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            _ = EXEC("self.length = self.attribute_length")
            debug_extension = "utf8"
    class operation_index(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            operation_index = "u2"
    class LineNumberTable_attribute(attribute, metaclass = M):
        class line_number_table_entry(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                start_pc = "operation_index"
                line_number = "u2"
        class construction(metaclass = ConstructionMeta):
            line_number_table_length = "u2"
            line_number_table = Array("line_number_table_entry", "self.line_number_table_length")
    class LocalVariableTable_attribute(attribute, metaclass = M):
        class local_variable_table_entry(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                start_pc = "operation_index"
                length = "u2"
                name_index = "constant_index"
                descriptor_index = "constant_index"
                index = "local_index_wide"
        class construction(metaclass = ConstructionMeta):
            local_variable_table_length = "u2"
            local_variable_table = Array("local_variable_table_entry", "self.local_variable_table_length")
    class local_index_wide(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            index = "u2"
    class local_index(metaclass = M):
        class construction(metaclass = ConstructionMeta):
            index = "u1"
    class LocalVariableTypeTable_attribute(attribute, metaclass = M):
        class local_variable_type_table_entry(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                start_pc = "operation_index"
                length = "u2"
                name_index = "constant_index"
                signature_index = "constant_index"
                index = "local_index_wide"
        class construction(metaclass = ConstructionMeta):
            local_variable_type_table_length = "u2"
            local_variable_type_table = Array("local_variable_type_table_entry", "self.local_variable_type_table_length")
    
    class Deprecated_attribute(attribute, metaclass = M): 
        def parse(self):
            return self
    
    class RuntimeVisibleAnnotations_attribute(attribute, metaclass = M):
        class annotations(metaclass = M):
            class element_value_pair(metaclass = M):
                class element_value_tag(ThreeWayDict, metaclass = M):
                    dype = "utf8"
                    bytes2internaldict = {"byte":"B",
                             "char":"C",
                             "double":"D",
                             "float":"F",
                             "int":"I",
                             "long":"J",
                             "short":"S",
                             "boolean":"Z",
                             "String":"s",
                             "enum constant":"e",
                             "class":"c",
                             "annotation type":"@",
                             "[]":"["
                    }
                    
                    def parse(self):
                        self.length = 1
                        self.code = registeredclasses["utf8"](self).parse()
                        return self.code
                    def writebytes(self, value):
                        self.length = 1
                        registeredclasses["utf8"](self).writebytes(value)
                class ann_value(metaclass = M):
                    class construction(metaclass = ConstructionMeta):
                        tag = "element_value_tag"
                        _ = CHOOSE()
                    def choose(self):
                        if self.tag in "BCDFIJSZs":
                            return self.const_value_index
                        elif self.tag == "e":
                            return self.enum_const_value
                        elif self.tag == "@":
                            return self.annotation_type
                        elif self.tag == "c":
                            return self.class_info_index
                        elif self.tag == "[":
                            return self.array_value
    
                class const_value_index(ann_value, metaclass=M):
                    class construction(metaclass = ConstructionMeta):
                        const_value_index = "constant_index"

                class enum_const_value(ann_value, metaclass=M):
                    class construction(metaclass = ConstructionMeta):
                        type_name_index = "constant_index"
                        const_name_index = "constant_index"

                class class_info_index(ann_value, metaclass=M):
                    class construction(metaclass = ConstructionMeta):
                        class_info_index = "constant_index"

                class annotation_value(ann_value, metaclass=M): 
                    def parse(self):
                        return self

                class array_value(ann_value, metaclass=M):
                    class construction(metaclass = ConstructionMeta):
                        num_values = "u2"
                        values = Array("ann_value", "self.num_values")
                class construction(metaclass = ConstructionMeta):
                    element_name_index = "constant_index"
                    value = "ann_value"
            class construction(metaclass = ConstructionMeta):
                type_index = "constant_index"
                num_element_value_pairs = "u2"
                element_value_pairs = Array("element_value_pair", "self.num_element_value_pairs")
        class construction(metaclass = ConstructionMeta):
            num_annotations = "u2"
            annotation = Array("annotations", "self.num_annotations")

    class RuntimeInvsibleAnnotations_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            num_annotations = "u2"
            annotation = Array("annotations", "self.num_annotations")

    class RuntimeVisibleParameterAnnotations_attribute(attribute, metaclass = M):
        class parameter_annotations(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                num_annotations = "u2"
                annotation = Array("annotations", "self.num_annotations")
        class construction(metaclass = ConstructionMeta):
            num_parameters = "u2"
            parameter_annotation = Array("parameter_annotations", "self.num_parameters")

    class RuntimeInvisibleParameterAnnotations_attribute(attribute, metaclass = M):
        class parameter_annotations(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                num_annotations = "u2"
                annotation = Array("annotations", "self.num_annotations")
        class construction(metaclass = ConstructionMeta):
            num_parameters = "u2"
            parameter_annotation = Array("parameter_annotations", "self.num_parameters")
    class AnnotationDefault_attribute(attribute, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            default_value = "element_value"
    
    class BootstrapMethods_attribute(attribute, metaclass = M):
        class bootstrap_method(metaclass = M):
            class construction(metaclass = ConstructionMeta):
                bootstrap_method_ref = "constant_index"
                num_bootstrap_arguments = "u2"
                bootstrap_arguments = Array("constant_index", "self.num_bootstrap_arguments")
        class construction(metaclass = ConstructionMeta):
            num_bootstrap_methods = "u2"
            bootstrap_methods = Array("bootstrap_method", "self.num_bootstrap_methods")
    
    class operation(metaclass = M):
        def increment(self):
            incamount = self.endpos - self.startpos
            self.setonup("_i", self._i + incamount)
        def parse(self):
            self.rpos = self.file.pos - self.startbyte
            self.op = getopname(self.file.read(1))
            kind = registeredclasses["op_" + javabyteparsedict[self.op]]
            return kind(self).parse()
        def writebytes(self):
            self.outputfile.write(getopbyte(self.op))
            writebytes(self)
            

    class op_0(operation):
        def writebytes(self):
            self.outputfile.write(getopbyte(self.op))
        def parse(self):
            return self
    class op_indexanddim(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            cindex = "constant_index"
            dim = "u1"
    class op_lindex(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            lindex = "local_index"

    class op_cindex(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            cindex = "constant_index"

    class op_branch(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            offset = "short"

    class op_wbranch(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            offset = "int"

    class op_lindexandbyte(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            lindex = "local_index"
            incint = "byte"

    class op_byte(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            int = "byte"

    class op_short(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            int = "short"

    class op_atype(operation, metaclass = M):
        class atype_code(ThreeWayDict, metaclass = M):
            dype = registeredclasses["u1"]
            bytes2internaldict = {
            8:"byte",
            9:"short",
            10:"int",
            11:"long",
            6:"float",
            7:"double",
            4:"boolean",
            5:"char"
            }
        class construction(metaclass = ConstructionMeta):
            atype = "atype_code"

    class short_constant_index(constant_index, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            index = "u1"
        @property
        def value(self):
            return self.constant_pool[self.index]
    class op_lcindex(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            cindex = "short_constant_index"

    
    class op_wide(operation, metaclass = M):
        _validwideops = ["iload", "fload", "aload", "lload", "dload", "istore", "fstore", "astore", "lstore", "dstore",
                        "ret", "iinc"]
        class construction(metaclass = ConstructionMeta):
            private_opname = "u1"
            _1 = EXEC('self.op2 = getopname(self.private_opname.to_bytes(1, "big"))')
            _2 = CHOOSE()

        def choose(self):
            assert self.op2 in self._validwideops, f"Invalid opcode after wide: {self.op2} at position {self.file.pos}"
            if self.op2 == "iinc":
                self.op2 += "_w"
                return registeredclasses["op_iinc_w"]
            else:
                self.op2 += "_w"
                return registeredclasses["op_other_w"]
    class op_iinc_w(op_wide, metaclass = M):
            class construction(metaclass = ConstructionMeta):
                lindex = "local_index_wide"
                incint = "short"

    class op_other_w(op_wide, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            lindex = "local_index_wide"

    class op_cindexdyn(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            cindex = "constant_index"
            zero = "u2"
            _2 = EXEC('assert self.zero == 0, f"bytes 3 and 4 of invokedynamic operands must be 0 at position {self.pos}"')

    class op_cindexint(operation, metaclass = M):
        class construction(metaclass = ConstructionMeta):
            cindex = "constant_index"
            count = "u1"
            zero = "u1"
            _2 = EXEC('assert self.zero == 0, f"byte 4 of invokeinterface operands must be 0 at position {self.pos}"')

    class op_lookupswitch(operation, metaclass = M):
        class pairswitchpairjump( metaclass = M):
            class construction(metaclass = ConstructionMeta):
                value = "int"
                offset = "int"
        def parse(self):
            self.alignment = (self.rpos + 1) % 4
            if self.alignment != 0:
                self.file.read(4 - self.alignment)
            self.default = registeredclasses["u4"](self).parse()
            self.branchno = registeredclasses["u4"](self).parse()
            self.switchtable = Array("pairswitchpairjump", "self.branchno")(self).parse()
            return self
        def writebytes(self):
            self.alignment = (self.outputfile.pos - self.wstartbyte + 1) % 4
            self.outputfile.write(getopbyte(self.op))
            if self.alignment != 0:
                self.outputfile.write(b'\x00'*(4-self.alignment))
            for i in self.default, self.branchno:
                registeredclasses["u4"](self).writebytes(i)
            for value in self.switchtable.values():
                value.writebytes()

    class op_tableswitch(operation, metaclass = M):
        def parse(self):
            self.alignment = (self.rpos + 1) % 4
            if self.alignment != 0:
                self.file.read(4 - self.alignment)
            self.default = registeredclasses["u4"](self).parse()
            self.low = registeredclasses["u4"](self).parse()
            self.high = registeredclasses["u4"](self).parse()
            self.branchno = 1 + self.high - self.low
            self.switchtable = [registeredclasses["u4"](self).parse() for i in range(self.branchno)]
            return self
        def writebytes(self):
            self.alignment = (self.outputfile.pos - self.wstartbyte + 1) % 4
            self.outputfile.write(getopbyte(self.op))
            if self.alignment != 0:
                self.outputfile.write(b'\x00'*(4-self.alignment))
            for i in self.default, self.low, self.high:
                registeredclasses["u4"](self).writebytes(i)
            for i in self.switchtable:
                registeredclasses["u4"](self).writebytes(i)


