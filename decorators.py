from byteconv import *
import re
import functools

class Array: pass
class Pointer: pass
class Choosing:pass

def parseall(names, parsemethods):
    retdict = {}
    for name, parsemethod in zip(names, parsemethods):
        retdict[name] = parsemethod()
    return retdict
def gennew(cls, container):
    thing =  object.__new__(cls)
    thing.container = container
def geninit(thing, container,**kwargs):
    thing.container = container
    thing.__dict__.update(kwargs)
class MagicMeta(type):
    """This metaclass assumes a flat namespace"""
    def __new__(meta, classname, bases, classDict):
        return type.__new__(meta, classname, bases, classDict)
        def link(dype):
            if type(dype) == str:
                return defclassdict[dype].parse
            elif type(dype) == Array

import struct
class Context:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
class ClassFile(metaclass = TypeDSL):
    def __init__(self, file):
        self.file = file
    ##Atomic type section
    class u1:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">B", file.read(1))[0]

        def __str__(self):
            return str(self.u2)
    class u2:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">H", file.read(2))[0]
        def __str__(self):
            return str(self.u2)
    class u4:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">I", file.read(4))[0]
        def __str__(self):
            return str(self.u4)
    class byte:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">b", file.read(1))[0]
        def __str__(self):
            return str(self.byte)
    class short:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">h", file.read(1))[0]
        def __str__(self):
            return str(self.short)
    class int:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">i", file.read(4))[0]
        def __str__(self):
            return str(self.signedchar)
    class long:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">q", file.read(8))[0]
        def __str__(self):
            return str(self.long)
    class float:
        @classmethod
        def parse(self, context):
            """atom"""
            return struct.unpack(">f", file.read(4))[0]
        def __str__(self):
            return str(self.float)

    class double:
        @classmethod
        def parse(cls, context):
            """atom"""
            return struct.unpack(">l", file.read(8))[0]
        def __str__(self):
            return str(self.double)
    class utf8:
        def __init__(self, utf8, length):
            self.utf8 = utf8
            self.length = length
        @classmethod
        def parse(cls, file, length):
            """atom"""
            return file.read(length).to_string("utf-8")
    class magic:
        u4 = "u4"
        def __init__(self, u4):
            if self.u4.tohex != "CAFEBABE":
                return InvalidMagicNumberError
    class minor_version:
        u2 = "u2"
    class major_version:
        u2 = "u2"
##Class Section
    class CONSTANT:
        def add(self):
            self.constant_pool[self.constant_pool.curi] = self
            self.constant_pool.curi += 1

    class CONSTANT_Class_info(CONSTANT):
        name_index = "constant_index"

    class CONSTANT_Fieldref_info(CONSTANT):
        class_index = "constant_index"
        name_and_type_index = "constant_index"

    class CONSTANT_Methodref_info(CONSTANT):
        class_index = "constant_index"
        name_and_type_index = "constant_index"

    class CONSTANT_InterfaceMethodref_info(CONSTANT):
        class_index = "constant_index"
        name_and_type_index = "constant_index"
    class CONSTANT_String_info(CONSTANT):
        string_index = "constant_index"

    class CONSTANT_Integer_info(CONSTANT):
        int = "int";

    class CONSTANT_Float_info(CONSTANT):
        float = "float"

    class CONSTANT_Long_info(CONSTANT):
        long = "long"
        def add(self):
            self.constant_pool[self.constant_pool.curi] = self
            self.constant_pool.curi += 2

    class CONSTANT_Double_info(CONSTANT):
        double = "double"
        def add(self):
            self.constant_pool[self.constant_pool.curi] = self
            self.constant_pool.curi += 2
    class CONSTANT_NameAndType_info(CONSTANT):
        name_index = "constant_index"
        descriptor_index = "constant_index"
    class CONSTANT_Utf8_info(CONSTANT):
        def parse(self):
            length = u2.parse()["u2"]
            return {"length":length, "utf8":utf8.parse(self.length)}

    class CONSTANT_MethodHandle_info:
        reference_kind
        reference_index = "constant_index"

    class CONSTANT_MethodType_info:
        descriptor_index = "constant_index"

    class CONSTANT_InvokeDynamic_info:
        bootstrap_method_attr_index ="*attribute_info super().attributes"
        name_and_type_index = "constant_index"

    class tag:
        constant_pool_tags = {
            "Class": 7,
            "Fieldref": 9,
            "Methodref": 10,
            "InterfaceMethodref": 11,
            "String": 8,
            "Integer": 3,
            "Float": 4,
            "Long": 5,
            "Double": 6,
            "NameAndType": 12,
            "Utf8": 1,
            "MethodHandle": 15,
            "MethodType": 16,
            "InvokeDynamic": 18
        }
        constant_pool_tags_inv = invdict(constant_pool_tags)
        @classmethod
        def parse(cls, context):
            """atom"""
            return {"tag": cls.constant_pool_tags_inv[int(context.file.read(1))]}

        @classmethod
        def __str__(cls):
            return self.tag

        @classmethod
        def bytes(cls):
            return bytes(cls.constant_pool_tags[self.tag])

        @classmethod
        def choose(cls):
            return eval("CONSTANT_" + self.tag)

    class cp_info:
        cp_info = "?tag"

    class constant_pool:
        constant_pool_count  = "u2"
        constant_pool = "cp_info[self.constant_pool_count - 1]"

        def get(constant_pool_index):
            return self.constant_pool[constant_pool_index - 1]

    class access_flags:
        access_flags = "class_or_interface_access_flags"

    class constant_index:
        constant_index = "*u2 cp_info super().constant_pool"

    class this_class:
        this_class = "*constant_index super().constant_pool"

    class super_class:
        this_class = "*constant_index super().constant_pool"
##Attribute Section

    class field_method_info_super:
        name_index = "constant_index"
        descriptor_index = "constant_index"
        attributes_count = "u2"
        attributes = "attribute_info[attributes_count]"
    class field_info(field_method_info_super):
        access_flags = "field_access_flags"
    class fields:
        fields_count  = "u2"
        fields = "field_info[self.fields_count]"
    class methods_info(field_method_info_super):
        access_flags = "method_access_flags"
    class methods:
        methods_count  = "u2"
        fields = "method_info[self.methods_count]"
    class attributes:
        attributes_count  = "u2"
        fields = "method_info[self.methods_count]"
    class CONSTANT_String:
        def choose(self):
            try:
                return eval(self.string_index.value)
            except NameError:
                return OtherAttribute(self.string_index.value)

    class stack_map_frame:
        frame_type = "?frame_type"
    class same_frame: pass
    class same_locals_1_stack_item_frame:
        stack = "verification_type_info"
    class Top_variable_info: pass
    class Integer_variable_info: pass
    class Float_variable_info: pass
    class Long_variable_info: pass
    class Double_variable_info: pass
    class Null_variable_info: pass
    class UninitializedThis_variable_info: pass
    class Object_variable_info:
        cpool_index = "constant_index"
    class Uninitialized_variable_info:
        offset = "Bytecode* [super().method]"
    class verification_type_info:
        variable_info = {
            "Top_variable_info":0,
            "Integer_variable_info":1,
            "Float_variable_info":2,
            "Long_variable_info":4,
            "Double_variable_info":3,
            "Null_variable_info":5,
            "UninitializedThis_variable_info":6,
            "Object_variable_info":7,
            "Uninitialized_variable_info":8
        }
    class frame_type:
        def choose(self):
            if self.frame_type <= 63:
                return same_frame
            elif self.frame_type <= 127:
                return same_locals_1_stack_item_frame
            elif self.frame_type < 247:
                return Invalid_frame_type_Error
            elif self.frame_type == 247:
                return same_locals_1_stack_item_frame_extended
            elif self.frame_type =<= 250:
                return chop_frame
            elif self.frame_type == 251:
                return same_frame_extended
            elif self.frame_type < 254:
                return append_frame
            elif self.frame_type == 255:
                return full_frame

    class local_index:
        u1 = "u1"
    class long_local_index:
        u2 = "u2"
    class atype:
        def __init__(self, tag):
            self.atype = atype
        @staticmethod
        def parse(self, file):
            return primitivetypeinvhex[file.read(1).tohex]
        def __str__(self, file):
            return self.atype
        def bytes(self):
            return bytes(primitivetypehex[self.atype])
    constant_info = "tag?"
    constant_pool = "constant_info[constant_pool_count - 1]"
    class LineNumberTable_attribute:
        class line_number_table_entry:
            start_pc = "u2"
            line_number = "u2"
        line_number_table_length = "u2"
        line_number_table = "line_number_table_entry[line_number_table_length]"
    class LocalVariableTable_attribute:
        class local_variable_table_entry:
            start_pc = "u2"
            length = "u2"
            name_index = "constant_index"
            descriptor_index = "constant_index"
            index = "u2"
        local_variable_table_length = "u2"
        local_variable_table = "local_variable_table_entry[local_variable_table_length]"


    class LocalVariableTypeTable_attribute:
        class local_variable_type_table_entry:
            start_pc = "code_pointer"
            length = "u2"
            name_index = "constant_index"
            signature_index = "constant_index"
            index = "u2"
        local_variable_type_table_length = "u2"
        local_variable_type_table = "local_variable_type_table_entry[local_variable_type_table_length]"


    class Deprecated_attribute:
        pass

ClassFile {
    u4             magic;
    u2             minor_version;
    u2             major_version;
    u2             constant_pool_count;
    cp_info        constant_pool[constant_pool_count-1];
    u2             access_flags;
    u2             this_class;
    u2             super_class;
    u2             interfaces_count;
    u2             interfaces[interfaces_count];
    u2             fields_count;
    field_info     fields[fields_count];
    u2             methods_count;
    method_info    methods[methods_count];
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
cp_info {
    u1 tag;
    u1 info[];
}

field_info {
    u2             access_flags;
    u2             name_index;
    u2             descriptor_index;
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
method_info {
    u2             access_flags;
    u2             name_index;
    u2             descriptor_index;
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
attribute_info {
    u2 attribute_name_index;
    u4 attribute_length;
    u1 info[attribute_length];
}
ConstantValue_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 constantvalue_index;
}
Code_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 max_stack;
    u2 max_locals;
    u4 code_length;
    u1 code[code_length];
    u2 exception_table_length;
    {   u2 start_pc;
        u2 end_pc;
        u2 handler_pc;
        u2 catch_type;
    } exception_table[exception_table_length];
    u2 attributes_count;
    attribute_info attributes[attributes_count];
}
StackMapTable_attribute {
    u2              attribute_name_index;
    u4              attribute_length;
    u2              number_of_entries;
    stack_map_frame entries[number_of_entries];
}
union stack_map_frame {
    same_frame;
    same_locals_1_stack_item_frame;
    same_locals_1_stack_item_frame_extended;
    chop_frame;
    same_frame_extended;
    append_frame;
    full_frame;
}
same_frame {
    u1 frame_type = SAME; /* 0-63 */
}
same_locals_1_stack_item_frame {
    u1 frame_type = SAME_LOCALS_1_STACK_ITEM; /* 64-127 */
    verification_type_info stack[1];
}
same_locals_1_stack_item_frame_extended {
    u1 frame_type = SAME_LOCALS_1_STACK_ITEM_EXTENDED; /* 247 */
    u2 offset_delta;
    verification_type_info stack[1];
}
chop_frame {
    u1 frame_type = CHOP; /* 248-250 */
    u2 offset_delta;
}
same_frame_extended {
    u1 frame_type = SAME_FRAME_EXTENDED; /* 251 */
    u2 offset_delta;
}
append_frame {
    u1 frame_type = APPEND; /* 252-254 */
    u2 offset_delta;
    verification_type_info locals[frame_type - 251];
}
full_frame {
    u1 frame_type = FULL_FRAME; /* 255 */
    u2 offset_delta;
    u2 number_of_locals;
    verification_type_info locals[number_of_locals];
    u2 number_of_stack_items;
    verification_type_info stack[number_of_stack_items];
}
union verification_type_info {
    Top_variable_info;
    Integer_variable_info;
    Float_variable_info;
    Long_variable_info;
    Double_variable_info;
    Null_variable_info;
    UninitializedThis_variable_info;
    Object_variable_info;
    Uninitialized_variable_info;
}
Top_variable_info {
    u1 tag = ITEM_Top; /* 0 */
}
Integer_variable_info {
    u1 tag = ITEM_Integer; /* 1 */
}
Float_variable_info {
    u1 tag = ITEM_Float; /* 2 */
}
Long_variable_info {
    u1 tag = ITEM_Long; /* 4 */
}
Double_variable_info {
    u1 tag = ITEM_Double; /* 3 */
}
Null_variable_info {
    u1 tag = ITEM_Null; /* 5 */
}
UninitializedThis_variable_info {
    u1 tag = ITEM_UninitializedThis; /* 6 */
}
Object_variable_info {
    u1 tag = ITEM_Object; /* 7 */
    u2 cpool_index;
}
Uninitialized_variable_info {
    u1 tag = ITEM_Uninitialized /* 8 */
    u2 offset;
}
    class Exceptions_attribute:
        number_of_exceptions = "u2"
        exception_index_table = "u2[number_of_exceptions]"
InnerClasses_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 number_of_classes;
    {   u2 inner_class_info_index;
        u2 outer_class_info_index;
        u2 inner_name_index;
        u2 inner_class_access_flags;
    } classes[number_of_classes];
}
EnclosingMethod_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 class_index;
    u2 method_index;
}
Synthetic_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
}
Signature_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 signature_index;
}
SourceFile_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 sourcefile_index;
}
SourceDebugExtension_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u1 debug_extension[attribute_length];
}
LineNumberTable_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 line_number_table_length;
    {   u2 start_pc;
        u2 line_number;
    } line_number_table[line_number_table_length];
}
LocalVariableTable_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 local_variable_table_length;
    {   u2 start_pc;
        u2 length;
        u2 name_index;
        u2 descriptor_index;
        u2 index;
    } local_variable_table[local_variable_table_length];
}
LocalVariableTypeTable_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 local_variable_type_table_length;
    {   u2 start_pc;
        u2 length;
        u2 name_index;
        u2 signature_index;
        u2 index;
    } local_variable_type_table[local_variable_type_table_length];
}
Deprecated_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
}
RuntimeVisibleAnnotations_attribute {
    u2         attribute_name_index;
    u4         attribute_length;
    u2         num_annotations;
    annotation annotations[num_annotations];
}
annotation {
    u2 type_index;
    u2 num_element_value_pairs;
    {   u2            element_name_index;
        element_value value;
    } element_value_pairs[num_element_value_pairs];
}
element_value {
    u1 tag;
    union {
        u2 const_value_index;

        {   u2 type_name_index;
            u2 const_name_index;
        } enum_const_value;

        u2 class_info_index;

        annotation annotation_value;

        {   u2            num_values;
            element_value values[num_values];
        } array_value;
    } value;
}
RuntimeInvisibleAnnotations_attribute {
    u2         attribute_name_index;
    u4         attribute_length;
    u2         num_annotations;
    annotation annotations[num_annotations];
}
RuntimeVisibleParameterAnnotations_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u1 num_parameters;
    {   u2         num_annotations;
        annotation annotations[num_annotations];
    } parameter_annotations[num_parameters];
}
RuntimeInvisibleParameterAnnotations_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u1 num_parameters;
    {   u2         num_annotations;
        annotation annotations[num_annotations];
    } parameter_annotations[num_parameters];
}
AnnotationDefault_attribute {
    u2            attribute_name_index;
    u4            attribute_length;
    element_value default_value;
}
BootstrapMethods_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 num_bootstrap_methods;
    {   u2 bootstrap_method_ref;
        u2 num_bootstrap_arguments;
        u2 bootstrap_arguments[num_bootstrap_arguments];
    } bootstrap_methods[num_bootstrap_methods];
}
