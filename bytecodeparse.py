from byteconv import *
from typing import Tuple
from functools import partial
from classfileconsts import *


class BytecodeParser:
    def __init__(self, filepath):
        self.file = Trackspos(filepath, self)
        self.currentmethodpos = None
class Trackspos:
    def __init__(self, filepath, parser):
        self.file = open(filepath, "rb")
        self.parser: Trackspos = parser
        self.pos = 0
    def read(self, number: int) -> bytes:
        readval = self.file.read(number)
        self.pos += number

def parseop(file: Trackspos):
    try:
        op = getopname(file.read(1).hex())
        classandoperands = parsefuncdict[javabyteparsedict[op]](file)
        return classandoperands[0](**classandoperands[1:])
    except InvalidOpcodeError as e:
        e.pos = file.pos
        raise e
def parsecafebabe(file: Trackspos):
    cafebabe = file.read(4)
    assert cafebabe == bytes.fromhex("cafebabe"), f"Magic Number incorrect: {cafebabe.hex()}, should be cafebabe"
def parseminorno(file: Trackspos):
    minorno = jbyteu16(file.read(2))
def parsemajorno(file: Trackspos):
    majorno = jbyteu16(file.read(2))
def parseconstant_pool(file: Trackspos):
    constant_pool_count = jbyteu16(file.read(2))
    constants = []
    parseconstants(file)
def parseaccess_flags(file):
    accessflags = file.read(2)
def parsethis_class(file):
    thisclassindex = jbyteu16(file.read(2))
def parsesuper_class(file):
    superclassindex = jbyteu16(file.read(2))
def parse4sections(file):
    for type_ in ["interface". "field", "method", "attribute"]:
        count = jbyteu16(file.read(2))
        parsefunc = parsetypedict[type_]
        for i in range(count):
            parsefunc(file)
def parsecindex(file: Trackspos):
    return (CindexOp, jbyteu16(file.read(2)))
def parsefield_info(file: Trackspos):
    flags = file.read(2)
    name_index = parsecindex()
    descriptor_index = parsecindex()
    attributes_count = jbyteu16(file.read(2))
    for i in range(attributes_count):
        parseattribute_info(file)
def parsemethod_info(file: Trackspos):
    flags = file.read(2)
    name_index = parsecindex()
    decriptor_index = parsecindex()
    attributes_count = jbyteu16(file.read(2))
    for i in range(attributes_count):
        parseattribute_info(file)

def parseattribute_info(file: Trackspos, type_: str):
    attribute_name_index, attribute_name = parsecindex(file)
    attribute_length = jbyteu32(file.read(4))
    if attribute_name in registeredattributes:
        contents = eval("parse" + attribute_name_tuple[1])(file)
    else:
        contents = parseunknownattribute(file, attribute_name)
def parseotherattributes(type_):
    pass
def parseConstantValue(file):
    constantvalue_index = parsecindex(file)
def parseCode(file):
    max_stack = jbyteu16(file.read(2))
    max_locals = jbyteu16(file.read(2))
    code_length = jbyteu32(file.read(4))
    precodepos = file.pos
    while(file.pos - precodepos < code_length):
        codearr = parseop(file)
    assert file.pos - precodepos == code_length, f"Unexpected end to code section at position {precodepos + code_length}"
    exception_table_length = jbyteu16(file.read(2))
    def parseexception_table(file):
        start_pc = jbyteu16(file.read(2))
        end_pc = jbyteu16(file.read(2))
        handler_pc = jbyteu16(file.read(2))
        catch_type = parsecindex(file)
    for i in range(exception_table_length):
        exceptiontable = parseexceptiontable(file)
    attributes_count = jbyteu16(file.read(2))
    for i in range(attributes_count):
        attribute_info = parseattribute()
def parseStackMapTable(file):
    number_of_entries = jbyteu16(read.file(2))
    pass #This function is going to get very messy
def parseExceptions(file):
    number_of_exceptions = jbyteu16(read.file(2))
    for i in range(number_of_exceptions):
        exception_index_table = parsecindex(file)
def parseClasses

parsetypedict = {
    "interface":parsecindex,
    "field":parsefield_info,
    "method":parsemethod_info,
    "attribute":parseattribute_info
}

def parsecindexanddim(file: Trackspos):
    cindex = jbyteu16(file.read(2))
    dim = jbyteu8(file.read(1))
    return (CindexAndDimOp, cindex, dim)
def parselindex(file: Trackspos):
    lindex = jbyteu8(file.read(1))
    return (LindexOp, lindex)
def parsebranch(file: Trackspos):
    offset = jbyteshort(file.read(2))
    return (BranchOp, offset)
def parsewbranch(file: Trackspos):
    offset = jbyteint(file.read(4))
    return (BranchOp, offset)
def parselindexandbyte(file: Trackspos):
    lindex = jbyteu8(file.read(1))
    incint = jbytechar(file.read(1))
    return (IncOp, lindex, incint)
def parsebyte(file: Trackspos):
    byteint = jbytechar(file.read(1))
def parseshort(file: Trackspos):
    shortint = jbyteshort(file.read(1))
def parseatype(file: Trackspos):
    ano = file.read(1).hex()
    assert ano in primitivetypeinvhex.keys(), f"Invalid Array type code {ano} at position {file.pos}"
    atype = primitivetypeinvhex[file.read(1).hex()]
    return (ATypeOp, atype)
def parselcindex(file: Trackspos):
    lcindex = jbyteu8(file.read(1))
    return (LCindexOp, lcindex)
validwideops = ["iload", "fload", "aload", "lload", "dload", "istore", "fstore", "astore", "lstore", "dstore", "ret", "iinc"]
def parsewide(op, file: Trackspos):
    op = getopbyte(file.read(1).hex())
    assert op in validwideops, f"Invalid opcode after wide: {op} at position {file.pos}"
    wlindex = jbyteu16(file.read(2))
    if op == "iinc":
        wincint = jbyteshort(file.read(2))
        return WLindexAndByteOp(op, wlindex, wincint)
    return WLindexOp(op, wlindex)
def parsecindexdyn(file: Trackspos):
    cindex = jbyteu16(file.read(2))
    zero = jbyteu16(file.read(2))
    assert zero == 0, f"bytes 3 and 4 of invokedynamic operands must be 0 at position {file.pos}"
def parsecindexint(file: Trackspos) -> Constant_Pool_Entry:
    cindex = jbyteu16(file.read(2))
    count = jbyteu8(file.read(1))
    zero = jbyteu8(file.read(2))
    assert zero == 0, f"byte 4 of invokeinterface operands must be 0 at position {file.pos}"
def parselookupswitch(file: Trackspos):
    alignment = (file.pos - file.parser.currentmethodpos) % 4
    file.read(alignment)
    default = jbyteint(file.read(4))
    branchno = jbyteu32(file.read(4))
    for i in range(branchno):
        pairswitchjump = parseswitchpairjump(file)
def parsetableswitch(file: Trackspos):
    alignment = (file.pos - file.parser.currentmethodpos) % 4
    file.read(alignment)
    default = jbyteint(file.read(4))
    low = jbyteint(file.read(4))
    high = jbyteint(file.read(4))
    branchno = high - low
    for i in range(branchno):
        switchjump = parseswitchjump(file)
def parseswitchjump(file: Trackspos):
    offset = jbyteint(file.read(4))
def parseswitchpairjump(file: Trackspos):
    value = jbyteint(file.read(4))
    offset = jbyteint(file.read(4))
parsefuncdict = {
    "cindex": parsecindex,
    "cindexanddim": parsecindexanddim
    "lindex": parselindex,
    "lindexandbyte": parselindexandbyte,
    "byte": parsebyte,
    "short": parseshort,
    "branch": parsebranch,
    "wbranch": parsewbranch,
    "lcindex" parselcindex,
    "wide": parsewide,
    "atype": parseatype,
    "lookupswitch": parselookupswitch,
    "tableswitch": parsetableswitch,
    "cindexdyn": parsecindexdyn,
    "cindexint": parsecindexint
    "0": lambda x: "",
}