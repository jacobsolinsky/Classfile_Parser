import struct
import pandas as pd
import os
tsvloc = os.path.join(os.path.dirname(__file__), "JavaByteCodes.txt")
javabytecodeframe = pd.read_table(tsvloc, sep="\t", encoding = "ISO-8859-1")
javabytecodedict = pd.Series(javabytecodeframe.Hex.values, index=javabytecodeframe.Mnemonic).to_dict()
javabyteparsedict = pd.Series(javabytecodeframe.Argtype.values, index=javabytecodeframe.Mnemonic).to_dict()
javainvbytecodedict = pd.Series(javabytecodeframe.Mnemonic.values, index=javabytecodeframe.Hex).to_dict()
class InvalidOpcodeError(Exception):
    def __init__(self, opcode: str, pos:int):
        self.opcode = opcode
        self.pos = pos
    def __str__(self):
        return f"InvalidOpcodeError: Opcode {self.opcode} at position {self.pos}"
def getopbyte(opname: str) -> bytearray:
    return bytes.fromhex(javabytecodedict[opname])
def getopname(opbyte: bytes) -> str:
    hexstr = opbyte.hex()
    try:
        return javainvbytecodedict[hexstr]
    except KeyError:
        raise InvalidOpcodeError(hexstr, 0)
def jutf8byte(a: str):
    return bytearray(a, encoding = "utf-8")
def jhexbyte(a: str) -> bytearray:
    return bytearray.fromhex(a)
def ju8byte(a: int) -> bytearray:
    return bytearray(struct.pack(">u1", a))
def ju16byte(a: int) -> bytearray:
    return bytearray(struct.pack(">u2", a))
def ju32byte(a: int) -> bytearray:
    return bytearray(struct.pack(">u4", a))
def jcharbyte(a: int) -> bytearray:
    return bytearray(struct.pack(">i1", a))
def jshortbyte(a: int) -> bytearray:
    return bytearray(struct.pack(">i2", a))
def jintbyte(a: int) -> bytearray:
    return bytearray(struct.pack(">i4", a))
def jlongbyte(a: int) -> bytearray:
    return bytearray(struct.pack(">i8", a))
def jfloatbyte(a: float) -> bytearray:
    return bytearray(struct.pack(">f4", a))
def jdoublebyte(a: float) -> bytearray:
    return bytearray(struct.pack(">f8", a))


def jbyteutf8(a: bytes) -> str:
    return a.decode("utf-8")
def jbytehex(a: bytes) -> str:
    return a.hex()
def jbyteu8(a: bytes) -> int:
    return int.from_bytes(a, byteorder="big", signed = False)
def jbyteu16(a: bytes) -> int:
    return int.from_bytes(a, byteorder="big", signed=False)
def jbyteu32(a: bytes) -> int:
    return int.from_bytes(a, byteorder="big", signed=False)
def jbytechar(a: bytes) -> int:
    return int.from_bytes(a, byteorder="big", signed=True)
def jbyteshort(a: bytes) -> int:
    return int.from_bytes(a, byteorder="big", signed=True)
def jbyteint(a: bytes) -> int:
    return int.from_bytes(a, byteorder="big", signed=True)
def jbytelong(a: bytes) -> int:
    return int.from_bytes(a, byteorder="big", signed=True)
def jbytefloat(a: bytes) -> float:
    return struct.unpack(">f", a)[0]
def jbytedouble(a: bytes) -> float:
    return struct.unpack(">d", a)[0]
