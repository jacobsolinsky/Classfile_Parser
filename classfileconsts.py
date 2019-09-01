from commonutilities import invdict
import struct
#Dictionaries have mnemonic keys and coded values
#Inverse dictionaries have coded keys and mnemonic values
def getconstant_pool_tag(type_:str) -> bytearray:
    return ju8byte(constant_pool_tags[type_])
def get_constant_pool_tag_name(tag: bytes)
    return constant_pool_tags_inv[jbyteu8(tag)]
def get_type_code(type_: JTypeU) -> str:
    if type(type_) is tuple:
        return "[" * type[1] + field_type_characters.get(type_[0], "L" + type_[0] + ";")
    return field_type_characters.get(type_, "L" + type_ + ";")
def get_method_code(methodsignature: MethodSignature) -> str:
    paramsignature =  "(" + "".join([get_type_code(type_) for type_ in methodsignature]) + ")" +
    retsignature = "V" if methodsignature[1] is None else get_type_code(methodsignature[1])
    return paramsignature + retsignature
field_type_characters = {
    "byte":"B",
    "char":"C",
    "double":"D",
    "float":"F",
    "int":"I",
    "long":"J",
    "short":"S",
    "boolean":"Z",
    "reference":"["
}
filed_type_characters_inv = invdict(field_type_characters)
java_lang_interfaces = (
"Appendable",
"AutoCloseable",
"CharSequence",
"Cloneable",
"Readable",
"Runnable"
)





def methodkinds = {
    "REF_getField":1,
 	"REF_getStatic":2,
 	"REF_putField":3,
 	"REF_putStatic":4,
 	"REF_invokeVirtual":5,
 	"REF_invokeStatic":6,
 	"REF_invokeSpecial":7,
 	"REF_newInvokeSpecial":8,
 	"REF_invokeInterface":9
}
def methodkindsinv = invdict(methodkinds)
primitivetypehex = {
    "byte":"08",
    "short":"09",
    "int":"0a",
    "long":"0b",
    "float":"06",
    "double":"07",
    "boolean":"04",
    "char":"05"
}
primitivetypeinvhex = invdict(primitivetypehex)
java_lang_classes = (
"Boolean",
"Byte",
"Character",
"ClassLoader",
"Compiler",
"Double",
"Float",
"Integer",
"Long",
"Math",
"Number",
"Object",
"Package",
"Process",
"ProcessBuilder",
"Runtime",
"RuntimePermission",
"SecurityManager",
"Short",
"StackTraceElement",
"StrictMath",
"String",
"StringBuffer",
"System",
"Thread",
"ThreadGroup",
"Throwable",
"Void"
)
java_lang_exeptions = (
"ArithmeticException",
"ArrayIndexOutOfBoundsExeption",
"ArrayStoreException",
"ClassCastException",
"ClassNotFoundException",
"CloneNotSupportedException",
"EnumConstantNotPresentException",
"Exception",
"IllegalAccessException",
"IllegalArgumentException",
"IllegalMonitorStateException",
"IndexOutOfBoundsException",
"InstatiationException",
"NegativeArraySizeException",
"NoSuchFieldException",
"NoSuchMethodException",
"NullPointerException",
"NumberFormatException",
"ReflectiveOperationException",
"RuntimeException",
"SecurityException",
"StringIndexOutOfBoundsException",
"TypeNotPresentEception",
"UnsupportedOperationException"
)
java_lang_errors = (
"AbstractMethodError",
"AssertionError",
"BootstrapMethodError",
"ClassCircularityError",
"ClassFormatError",
"Error",
"ExceptionInInitializerError",
"IllegalAccessError",
"IncompatibleClassChangeError",
"InstantiationError",
"InternalError",
"LinkageError",
"NoClassDefFoundError",
"NoSuchFieldErrir",
"NoSuchMethodError",
"OutOfMemoryError",
"StackOverflowError",
"ThreadDeath",
"UnsatisfiedLinkError",
"UnsupportedClassVersionError",
"VerifyError",
"VirtualMachineError"
)
java_lang_annotation_types =(
"Deprecated",
"Override",
"SafeVarargs",
"SuppressWarnings"
)
registeredattributes = [
    "ConstantValue",
    "Code",
    "StackMapTable",
    "Exceptions",
    "InnerClasses",
    "EnclosingMethod",
    "Synthetic",
    "Signature",
    "SourceFile",
    "sourceSourceDebugExtension",
    "LineNumberTable",
    "LocalVariableTable",
    "LocalVariableTypeTable",
    "Deprecated",
    "RuntimeVisibleAnnotations",
    "RuntimeInvisibleAnnotations",
    "RuntimeVisibleParameterAnnotations",
    "RuntimeInvisibleParameterAnnotations",
    "AnnotationDefault",
    "BootstrapMethods"
]