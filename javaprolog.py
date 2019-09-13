#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 19:16:10 2019

@author: jacobsolinsky
"""
from codeprinter import parsemethodtypestring, parsefieldtypestring
def classIsTypeSafe(klass):  
    klassname = classClassName(klass)
    if klassname !=     'java/lang/Object'   : 
        klassloader = classDefiningLoader(klass)    
        superklassChain = superclassChain(Name, L, Chain)    
        Chain \= [],    
        klassSuperClassName = classSuperClassName(klass)    
        loadedClass(SuperclassName, L, Superclass),    
        klassIsNotFinal = classIsNotFinal(Superclass),      
        klassMethods = classMethods(klass),   
        checklist(methodIsTypeSafe(Class), Methods).
    else:
        klassname = 'java/lang/Object'   
        classDefiningLoader(Class, L),    
        isBootstrapLoader(L),    
        classMethods(Class, Methods),     
        checklist(methodIsTypeSafe(Class), Methods)
    
def classClassName(classfile):
    return classfile.this_class.value.name_index.value.utf8

def classIsInterface(classfile):
    return "INTERFACE" in classfile.access_flags

def classIsNotFinal(classfile):
    return not("FINAL" in classfile.access_flags)

def classSuperClassName(classfile):
    return classfile.super_class.value.name_index.value.utf8

def classMethods(classfile):
    return classfile.methods

def classAttributes(classfile):
    return classfile.attribute_info

def classDefiningLoader:
    """Extracts the defining class loader, Loader, of the class Class"""
    return None 
def isBootstrapLoader(loader):
    """True iff the class loader Loader is the bootstrap class loader."""
    return None
def loadedClass(Name, InitiatingLoader, ClassDefinition):
    """True iff there exists a class named Name whose representation (in accordancewith this specification) when loaded by the class loader InitiatingLoader isClassDefinition."""
    return None

def methodName(method):
    return method.name_index.value.utf8

def methodAccessFlags(method):
    return method.access_flags

def methodDescriptor(method):
    return parsemethodtypestring(method.descriptor_index.value.utf8)

def isInit(method):
    return "<init>" == methodName(method)

def isNotInit(method):
    return "<init>" != methodName(method)

def isNotFinal(method):
    return not("FINAL" in method.access_flags)

def isStatic(method):
    return "STATIC" in method.access_flags

def isPrivate(method):
    return "PRIVATE" in method.access_flags

def isNotPrivate(method):
    return not("PRIVATE" in method.access_flags)

def isProtected(memberClass, memberName, memberDescriptor):
    mmet = memberClass.method_name_list
    fmet = memberClass.field_name_list 
    ametm = [memberClass.methods[i] for i, name in enumerate(mmet) if name == memberName] +\
            [memberClass.fields[i] for i, name in enumerate(fmet) if name == memberName]
    retval = ["PROTECTED" in i.access_flags and i.descriptor_index.value.utf8 == memberDescriptor for i in ametm]
    return any(retval)

def isNotProtected(memberClass, memberName, memberDescriptor):
    return not(isProtected(memberClass, memberName, memberDescriptor))

def parseFieldDescriptor(fielddescriptor):
    return parsefieldtypestring(fielddescriptor)

def parseMethodDescriptor(fielddescriptor):
    return parsemethodtypestring(fielddescriptor)


def parseCodeAttribute(method):
    codeattr = method.attributes[0]
    FrameSize = codeattr.max_locals
    MaxStack = codeattr.max_stack
    ParsedCode = codeattr.code.codearr
    Handlers = codeattr.exception_table
    StackMap = codeattr.getattribute("StackMapTable")
    return (FrameSize, MaxStack, ParsedCode, Handlers, StackMap)

def samePackageName(Class1, Class2):
    pass

def differentPackageName(Class1, Class2):
    pass

class Environment:
    def __init__(self, klass, method):
        self.klass = klass
        self.method = method
        _, MaxStack, ParsedCode, Handlers, _ = parseCodeAttribute(method)
        self.MaxStack = MaxStack
        self.ParsedCode = ParsedCode
        self.Handlers = Handlers
        _, rettype = parseMethodDescriptor(method.descriptor_index.value.utf8)
        self.rettype = rettype
        
def allInstructions(enviroment):
    return environment.ParsedCode

def exceptionHandlers(environment):
    return environment.Handlers

def maxOperandStackLength(environment):
    return environment.MaxStack

def thisClass(environment):
    return environment.klass

def thisMethodReturnType(environment):
    return environment.rettype








    