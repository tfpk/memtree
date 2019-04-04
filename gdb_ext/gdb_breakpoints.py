"""
In order to determine the size of malloced pointers, 
gdb needs to remember sizes every time a malloc/realloc occurs.

To do this, breakpoints are set on malloc, realloc and free.
When the function is called, we set a breakpoint on the end of that function.
This lets us determine the size of the [m|re]alloc and also the returned addr.
"""

import gdb

from gdb_interface import (
    gdb_get_pointer,
    gdb_get_struct,
    gdb_get_array,
    gdb_get_type,
    gdb_get_dump,
    gdb_print,
    gdb_execute,
)

def create_gdb_globals():
    if not hasattr(gdb, 'mallocs'):
        gdb.mallocs = {}
    if not hasattr(gdb, 'gdb_breakpoints'):
        gdb.gdb_breakpoints = []

class AllocFinishBreakpoint(gdb.FinishBreakpoint):
    def __init__(self, place, num_bytes, **kwargs):
        super().__init__(place, internal=True, **kwargs)
        self.num_bytes = num_bytes

    def stop(self):
        gdb.mallocs[str(self.return_value)] = self.num_bytes
        return False

class MallocBreakpoint(gdb.Breakpoint):
    def __init__(self, *args, **kwargs):
        if 'internal' in kwargs:
            del kwargs['internal']
        super().__init__(*args, internal=True, **kwargs)
        create_gdb_globals()

    def stop(self):
        cur_frame = gdb.newest_frame()
        try:
            num_bytes = int(gdb_print('bytes'))
        except:
            return False

        gdb.gdb_breakpoints.append(AllocFinishBreakpoint(cur_frame, num_bytes))
        return False

class CallocBreakpoint(MallocBreakpoint):
    def __init__(self, *args, **kwargs):
        if 'internal' in args:
            del kwargs['internal']
        super().__init__(*args, internal=True, **kwargs)
        create_gdb_globals()

    def stop(self):
        cur_frame = gdb.newest_frame()
        try:
            num_bytes = int(gdb_print('n')) * int(gdb_print('elem_size'))
        except:
            return False

        gdb.gdb_breakpoints.append(AllocFinishBreakpoint(cur_frame, num_bytes))
        return False


class ReallocBreakpoint(gdb.Breakpoint):
    def __init__(self, *args, **kwargs):
        create_gdb_globals()
        if 'internal' in args:
            del kwargs['internal']
        super().__init__(*args, internal=True, **kwargs)

    def stop(self):
        cur_frame = gdb.newest_frame()
        try:
            num_bytes = int(gdb_print('bytes'))
            gdb.mallocs[str(gdb_print('oldmem'))] = 0
        except:
            return False

        gdb.gdb_breakpoints.append(AllocFinishBreakpoint(cur_frame, num_bytes))
        return False


class FreeBreakpoint(gdb.Breakpoint):
    def __init__(self, *args, **kwargs):
        create_gdb_globals()
        if 'internal' in args:
            del args['internal']
        super().__init__(*args, internal=True, **kwargs)

    def stop(self):
        try:
            gdb.mallocs[str(gdb_print('mem'))] = 0
        except:
            return False

        return False

