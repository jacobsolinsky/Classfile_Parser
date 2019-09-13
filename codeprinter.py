#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 12:42:42 2019

@author: jacobsolinsky
"""
printableclasses = {}
class S(type):
    def __new__(meta, classname, bases, classDict):
        thing = type.__new__(meta, classname, bases, classDict)
        printableclasses[thing.__name__] = thing
        return thing
    
def parseclass(stri):
        retval = ""
        char1 = next(stri)
        while char1 != ";":
            retval += char1
            char1 = next(stri)
        return retval
    
typedict = {
            "B": lambda x: "byte",
            "C": lambda x: "char",
            "D": lambda x: "double",
            "F": lambda x: "float",
            "I": lambda x: "int",
            "J": lambda x: "long",
            "L": parseclass,
            "S": lambda x: "short",
            "Z": lambda x: "boolean",
            }
def parsemethodtypestring(tstr):
    tstri = iter(tstr)
    assert next(tstri) == "(", Exception(f"Invalid Method type string: {tstr}")
    argsig = []
    retsig = ""
    numarr = 0
    for char in tstri:
        if char == ")":
            break
        if char == "[":
            argsig.append("[]")
            numarr += 1
            continue
        [argsig.pop() for i in range(numarr)]
        argsig.append(typedict[char](tstri) + "[]" * numarr)
        numarr = 0
    for char in tstri:
        if char == "[":
            numarr += 1
            continue
        if char == "V":
            retsig = "void"
            break
        retsig = typedict[char](tstri) + "[]" * numarr
    return (argsig, retsig)
def parsefieldtypestring(tstr):
        tstri = iter(tstr)
        numarr = 0
        for char in tstri:
            if char == "[":
                numarr += 1
                continue
            sig = typedict[char](tstri) + "[]" * numarr
        return sig
    
    
class constant_pool_s:
    def __str__(self, value):
        retval = ""
        for key, constant in value.items():
                retval += f"{'#' + str(key): >7} = " + constant.__str__() + "\n"
        return retval
    
class fields_s:
    slots = {
             "access":["PUBLIC", "PRIVATE", "PROTECTED"],
             "static":["STATIC"],
             "duration":["FINAL", "TRANSIENT"],
             "transient":["TRANSIENT"],
            }
    def __str__(self, value):
        retval = ""
        for key, field in value.items():
            thisslots = {key:"" for key in self.slots}
            for flag in field.access_flags:
                for subkey, item in self.slots.items():
                    if flag in item:
                        thisslots[subkey] = flag.lower()
            modifiers = ""
            for item in thisslots.values():
                if item != "":
                    modifiers += item + " "
            ret = parsefieldtypestring(field.descriptor_index.value.utf8)
            ret += " "
            firstline = f"  {modifiers}{ret}{field.name_index.value.utf8};" +"\n"
            secondline = f"    descriptor: {field.descriptor_index.value.utf8}" + "\n"
            thirdline = f"    flags: {', '.join(['ACC_' + flag for flag in field.access_flags])}" + "\n"
            retval += firstline + secondline + thirdline
        return retval
class ConstantValue_attribute(metaclass = S):
    def __str__(self):
        value = self.constantvalue_index.value
        fieldtype = self.descriptor_index.value.utf8
        return {
            "B": lambda x: "byte " + str(x.byte),
            "C": lambda x: "char" + str(x.char),
            "D": lambda x: "double " + str(x.double),
            "F": lambda x: "float " + str(x.float),
            "I": lambda x: "int " + str(x.int),
            "J": lambda x: "long" + str(x.long),
            "Ljava/lang/String;": lambda x: "string " + x.value.string_index.value.utf8,
            "S": lambda x: "short " + str(x.short),
            "Z": lambda x: "boolean " + str(x.boolean)
            }[fieldtype](value)
    
class methods_s:
    slots = {"abstract":["ABSTRACT"],
             "access":["PUBLIC", "PRIVATE", "PROTECTED"],
             "static":["STATIC"],
             "final":["FINAL"],
             "synchronized":["SYNCHRONIZED"],
             "compiletype":["NATIVE", "STRICT"]
            }
    def __str__(self, value):
        retval = ""
        for key, method in value.items():
            thisslots = {key:"" for key in self.slots}
            for flag in method.access_flags:
                for subkey, item in self.slots.items():
                    if flag in item:
                        if flag == "STRICT":
                            flag = "strictfp"
                        thisslots[subkey] = flag.lower()
            modifiers = ""
            for item in thisslots.values():
                if item != "":
                    modifiers += item + " "
            args, ret = parsemethodtypestring(method.descriptor_index.value.utf8)
            ret += " "
            if ret == "void ":
                ret = ""
            argit = iter(args)
            try:
                argstr = next(argit)
            except StopIteration:
                argstr = ""
            for arg in argit:
                argstr += ", " + arg
            firstline = f"  {modifiers}{ret}{method.name_index.value.utf8}({argstr});" +"\n"
            secondline = f"    descriptor: {method.descriptor_index.value.utf8}" + "\n"
            thirdline = f"    flags: {', '.join(['ACC_' + flag for flag in method.access_flags])}" + "\n"
            fourthline = f"    code:" + "\n"
            mcode = method.attributes[0].code
            fifthline = f"      stack={mcode.max_stack}, locals={mcode.max_locals}, args_size={len(args)}" +"\n"
            codestr = mcode.__str__()
            retval += firstline + secondline + thirdline + fourthline + fifthline + codestr
        return retval
            
         
class CONSTANT_Class_info(metaclass = S):
        def ministr(self):
            return "class " + self.name_index.value.utf8
        def __str__(self):
            firstpart = f"{'Fieldref': <20}"
            secondpart = f"#{self.name_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.name_index.value.utf8}"
            return firstpart + secondpart + thirdpart
        
class CONSTANT_Fieldref_info(metaclass = S):
        def ministr(self):
            return f"Field {self.class_index.value.name_index.value.utf8}.{self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
        def __str__(self):
            firstpart = f"{'Fieldref': <20}"
            secondpart = f"#{self.class_index.index}.#{self.name_and_type_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
            return firstpart + secondpart + thirdpart
            
class CONSTANT_Methodref_info(metaclass = S):
        def ministr(self):
            return f"Method {self.class_index.value.name_index.value.utf8}.{self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
        def __str__(self):
            firstpart = f"{'Methodref': <20}"
            secondpart = f"#{self.class_index.index}.#{self.name_and_type_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
            return firstpart + secondpart + thirdpart
class CONSTANT_InterfaceMethodref_info(metaclass = S):
        def ministr(self):
            return f"InterfaceMethod {self.class_index.value.name_index.value.utf8}.{self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
        def __str__(self):
            firstpart = f"{'Interfaceref': <20}"
            secondpart = f"#{self.class_index.index}.#{self.name_and_type_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
            return firstpart + secondpart + thirdpart
        
class CONSTANT_String_info(metaclass = S):
    def ministr(self):
            return "String " + self.string_index.value.utf8
    def __str__(self):
            firstpart = f"{'String': <20}"
            secondpart = f"#{self.string_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.string_index.value.utf8}"
            return firstpart + secondpart + thirdpart

class CONSTANT_Integer_info(metaclass = S):
    def ministr(self):
            return "Integer " + str(self.int)
    def __str__(self):
            firstpart = f"{'Integer': <20}"
            secondpart = f"{self.int}"
            secondpart = f"{secondpart: <13}"
            return firstpart + secondpart
  
class CONSTANT_Float_info(metaclass = S):
        def ministr(self):
            return "Float " + str(self.float)
        def __str__(self):
            firstpart = f"{'Float': <20}"
            secondpart = f"{self.float}f"
            secondpart = f"{secondpart: <13}"
            return firstpart + secondpart

class CONSTANT_Long_info(metaclass = S):
    def ministr(self):
            return "Long " + str(self.long)
    def __str__(self):
            firstpart = f"{'Long': <20}"
            secondpart = f"{self.long}l"
            secondpart = f"{secondpart: <13}"
            return firstpart + secondpart

class CONSTANT_Double_info(metaclass = S):
    def ministr(self):
            return "Double " + str(self.double)
    def __str__(self):
            firstpart = f"{'Long': <20}"
            secondpart = f"{self.long}l"
            secondpart = f"{secondpart: <13}"
            return firstpart + secondpart

        
class CONSTANT_NameAndType_info(metaclass = S):
        def ministr(self):
            return f"NameAndType {self.name_index.value.utf8:self.descriptor_index.value.utf8}"
        def __str__(self):
            firstpart = f"{'NameAndType': <20}"
            secondpart = f"#{self.name_index.index}.#{self.descriptor_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.name_index.value.utf8}:{self.descriptor_index.value.utf8}"
            return firstpart + secondpart + thirdpart

class CONSTANT_Utf8_info(metaclass = S):
    def ministr(self):
            return "Utf8 " + self.utf8
    def __str__(self):
            firstpart = f"{'Utf8': <20}"
            secondpart = f"{self.utf8}"
            secondpart = f"{secondpart: <13}"
            return firstpart + secondpart


class CONSTANT_MethodHandle_info(metaclass = S):
        def ministr(self):
            return f"MethodHandle {self.reference_kind}:{self.reference_index.value.ministr()}"
        def __str__(self):
            firstpart = f"{'MethodHandle': <20}"
            secondpart = f"#{self.reference_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.reference_kind}:{self.reference_index.value.ministr()}"
            return firstpart + secondpart + thirdpart   


class CONSTANT_MethodType_info(metaclass = S):
        def ministr(self):
            return f"MethodType {self.descriptor_index.value.utf8}"
        def __str__(self):
            firstpart = f"{'MethodType': <20}"
            secondpart = f"#{self.descriptor_index.index}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.descriptor_index.value.utf8}"
            return firstpart + secondpart + thirdpart


class CONSTANT_InvokeDynamic_info(metaclass = S):
    def ministr(self):
            return f"InvokeDynamic {self.bootstrap_method_index}:{self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
    def __str__(self):
            firstpart = f"{'MethodType': <20}"
            secondpart = f"#{self.bootstrap_method_index.index}.#{self.name_and_type_index.value}"
            secondpart = f"{secondpart: <13}"
            thirdpart = f"// {self.bootstrap_method_index}:{self.name_and_type_index.value.name_index.value.utf8}:{self.name_and_type_index.value.descriptor_index.value.utf8}"
            return firstpart + secondpart + thirdpart

class codearr(metaclass = S):
    def __str__(self):
        retval = ""
        for key, value in self.codearr.items():
            valuename = value.__class__.__name__
            #colon is in column 11, 16 spots for argname
            firstpos = f"{key: >10}: "
            if valuename == "op_wide":
                secondpos = f"{value.op2: <18}"
            else:
                secondpos = f"{value.op: <18}"
            #firstarg in column 27, 20 spots for firstarg
            thirdpos = ""
            fourthpos = ""
            if valuename == "op_lookupswitch":
                thirdpos = f"{{ // {value.branchno}" + '\n'
                for branch in value.switchtable.values():
                    thirdpos += f"{branch.value: >23}: {branch.offset + key}" + "\n"
                thirdpos += f"{'default': >23}: {value.default + key}" + "\n"
                thirdpos += "}\n"
                retval += firstpos + secondpos + thirdpos
                continue
            
            if valuename == "op_tableswitch":
                thirdpos = f"{{ // {value.low} to {value.high}" + '\n'
                for i, no in enumerate(value.switchtable):
                    thirdpos += f"{i + value.low: >23}: {no + key}" + "\n"
                thirdpos += f"{'default': >23}: {value.default + key}" + "\n"
                thirdpos += "}\n"
                retval += firstpos + secondpos + thirdpos
                continue
            if valuename in [ "op_"+i for i in ("lindex", "other_w")]:
                thirdpos = str(value.lindex.index)
            elif valuename in ["op_"+i for i in ("cindex", "lcindex", "cindexint", "indexanddim")]:
                thirdpos = "#" + str(value.cindex.index)
                fourthpos = "// " + value.cindex.value.ministr()
            elif valuename in ["op_" + i for i in ("branch", "wbranch")]:
                thirdpos = str(key + value.offset)
            elif valuename == "op_atype":
                thirdpos = str(value.atype)
            if valuename  in ["op_" + i for i in ("lindexandbyte", "iinc_w")]:
                thirdpos += f", {value.incint}"
            elif valuename == "op_indexanddim":
                thirdpos += f", {value.dim}"
            elif valuename == "op_cindexint":
                thirdpos += f", {value.count}"
            elif valuename  in ["op_"+i for i in ("byte", "short")]:
                thirdpos += f"{value.int}"
            thirdpos = f"{thirdpos: <20}"
            retval += firstpos + secondpos + thirdpos + fourthpos + "\n"
            continue
        return retval
            #slashslasharg in column 47

class LineNumberTable_attribute(metaclass = S):
    def __str__(self):
        firstline = "      LineNumberTable:\n"
        for value in self.line_number_table.values():
            firstline += f"        line {value.line_number}: {value.start_pc.operation_index}" + "\n"
        return firstline

class LocalVariableTable_attribute(metaclass = S):
    def __str__(self):
        firstline = "      LocalVariableTable:\n"
        secondline = f"{'Start': >13}{'Length': >8}{'Slot': >6} {'Name': >5}   Signature" + "\n"
        for value in self.local_variable_table.values():
            signature = parsefieldtypestring(value.descriptor_index.value.utf8)
            secondline += f"{value.start_pc.operation_index: >13}{value.length: >8}{value.index.index: >6} {value.name_index.value.utf8: >5}   {signature}" + "\n"
        return firstline + secondline

class StackMapTable_attribute(metaclass = S):
    def __str__(self):
        firstline = "      StackMapTable:\n"
        otherlines = ''.join([value.__str__() for value in self.stackmaptable.values()])
        return firstline + otherlines

class same_frame(metaclass=S):
    def __str__(self):
        return f"        frame_type = {self.frame_type} /* {self.__class__.__name__[:-6]} */" +"\n"

class same_locals_1_stack_item_frame(metaclass=S):
    def __str__(self):
        frame_type = f"        frame_type = {self.frame_type} /* {self.__class__.__name__[:-6]} */" +"\n"
        offset_delta = f"          offset_delta = {self.offset_delta}" +"\n"
        stack = f"         stack = [ {', '.join([ vi.__str__() for vi in self.stack.values()])} ]" +"\n"
        return frame_type + offset_delta +stack

            
class same_locals_1_stack_item_frame_extended(metaclass=S):
    def __str__(self):
        frame_type = f"        frame_type = {self.frame_type} /* {self.__class__.__name__} */" +"\n"
        offset_delta = f"          offset_delta = {self.offset_delta}" +"\n"
        stack = f"         stack = [ {', '.join([ vi.__str__() for vi in self.stack.values()])} ]" +"\n"
        return frame_type + offset_delta +stack
    
class chop_frame(metaclass=S):
    def __str__(self):
        frame_type = f"        frame_type = {self.frame_type} /* {self.__class__.__name__[:-6]} */" +"\n"
        offset_delta = f"          offset_delta = {self.offset_delta}" +"\n"
        return frame_type + offset_delta
    
class same_frame_extended(metaclass=S):
    def __str__(self):
        frame_type = f"        frame_type = {self.frame_type} /* {self.__class__.__name__[:-6]} */" +"\n"
        offset_delta = f"          offset_delta = {self.offset_delta}" +"\n"
        return frame_type + offset_delta    
    
class append_frame(metaclass=S):
    def __str__(self):
        frame_type = f"        frame_type = {self.frame_type} /* {self.__class__.__name__[:-6]} */" +"\n"
        offset_delta = f"          offset_delta = {self.offset_delta}" +"\n"
        locals = f"         locals = [ {', '.join([ vi.__str__() for vi in self.locals.values()])} ]" +"\n"
        return frame_type + offset_delta + locals
    
class full_frame(metaclass = S):
    def __str__(self):
        frame_type = f"        frame_type = {self.frame_type} /* {self.__class__.__name__} */" +"\n"
        offset_delta = f"        offset_delta = {self.offset_delta}" + "\n"
        locals = f"        locals = [ {', '.join([ vi.__str__() for vi in self.locals.values()])} ]" +"\n"
        stack = f"         stack = [ {', '.join([ vi.__str__() for vi in self.stack.values()])} ]" +"\n"
        return frame_type + offset_delta + locals + stack

class verification_type_info(metaclass = S):
    def __str__(self):
        if self.__class__.__name__ == "Object_variable_info":
            return "class " + self.cpool_index.value.name_index.value.utf8
        elif self.__class__.__name__ == "Uninitialized_variable_info":
            return "Uninitialized_variable " + self.offset
        else:
            return self.itemtag

class exception_table(metaclass = S):
    def __str__(self, value):
        firstline = "     Exception table\n"
        secondline = f"        {'from': >7} {'to': >4} {'target': >6} {'type': >4}" +"\n"
        for vi in value.values():
            catchtype = vi.catch_type.index
            if catchtype == 0:
                catchtype = "any"
            else:
                catchtype = vi.catch_type.value
            secondline += f"        {vi.start_pc.index: >7} {vi.end_pc.index: >4} {vi.handler_pc.index: >6} {catchtype: >4}" +"\n"
        return firstline + secondline
class Exceptions_attribute(metaclass = S):
    def __str__(self):
        firstline = "      Exceptions\n"
        for value in self.exception_index_table.values():
            firstline += f"        throws {value.value.name_index.value.utf8}" +"\n"
        return firstline
class EnclosingMethod_attribute(metaclass = S):
    def __str__(self):
        if self.method_index.index == 0:
            methodindex = "this"
        else:
            methodindex = self.method_index.value.name_index.value.utf8
        firstline = f"EnclosingMethod: {'#' + str(self.class_index.index) +'.#' + str(self.method_index.index): <20} \\ {self.class_index.value.name_index.value.utf8}.{methodindex}" + "\n"
        return firstline
class Deprecated_attribute(metaclass = S):
    def __str__(self):
        return "      Deprecated: true\n"
class Synthetic_attribbute(metaclass = S):
    def __str__(self):
        return "      Synthetic: true\n"
class SourceFile_attribute(metaclass = S):
    def __str__(self):
        return f'SourceFile: "{self.sourcefile_index.value.utf8}"' + "\n"
class SourceDebugExtesion_attribute(metaclass = S): 
        def __str__(self):
            return f'SourceDebugExtesion: "{self.debug_extension}"' + "\n"
        