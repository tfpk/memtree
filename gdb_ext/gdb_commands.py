#!/usr/bin/python3
""" The base of this program, that takes a memory address, and writes out all the
values obtained by following links.
"""

import gdb

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gdb_interface import (
    gdb_get_pointer,
    gdb_get_struct,
    gdb_get_array,
    gdb_get_type,
    gdb_get_dump,
    gdb_print,
    gdb_execute,
    gdb_toggle_pagination
)

from gdb_breakpoints import (
    MallocBreakpoint,
    CallocBreakpoint,
    ReallocBreakpoint,
    FreeBreakpoint
)

from gdb_http_server import run

CURRENT_DUMP = ""


class JsonDump(gdb.Command):
    def __init__(self, name):
        super().__init__(name, gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        if len(args) != 2:
            raise ValueError("Please provide two arguments: the object, and path to dump file")
        obj_name, path = args

        dump = {}

        try:
            gdb_get_dump(obj_name, dump)
        except:
            import traceback
            traceback.print_exc()

        print(dump)

JsonDump("jdump")

class JsonServe(gdb.Command):
    def __init__(self, name):
        super().__init__(name, gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        if len(args) != 1:
            raise ValueError("Please provide an argument: the object")
        obj_name = args[0]

        dump = {}

        try:
            gdb_get_dump(obj_name, dump)
        except:
            import traceback
            traceback.print_exc()
        gdb_toggle_pagination(False)
        run(dump)
        gdb_toggle_pagination(True)


JsonServe("jserve")

class XPython(gdb.Command):
    def __init__(self, name):
        super().__init__(name, gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        print(eval(arg))


XPython("xpy")
XPython("xpython")


print("... Initializing Breakpoints (ignore this) ...")
MallocBreakpoint("malloc")
CallocBreakpoint("calloc")
ReallocBreakpoint("realloc")
FreeBreakpoint("free")
print("... Breakpoints Initialized ...")


class MallocList(gdb.Command):
    def __init__(self, name):
        super().__init__(name, gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        print(gdb.mallocs)


MallocList("ml")
