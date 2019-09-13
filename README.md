# Classfile_Parser
This project currently is capable of reading and writing java class files. compiledecode's ClassFile class can currently
read class files when initialized (readfile = compiledecode.ClassFile("/path/to/classfile.class"). It can also write class files 
through its writetofile method (readfile.writefile("/path/to/output.class"))). The constant pool, method bytecode,
and the StackMapTable, LineNumberTable, LocalVariableTable, and exceptions all now have printable representations. 
javaprolog.py is an in progress bytecode verifier.
