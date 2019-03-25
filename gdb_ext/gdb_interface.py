"""
Functions that call gdb functions, and return a python datastructure
that represents the result.
"""

import re

import gdb


def gdb_toggle_pagination(state):
    toggle = "off"
    if state:
        toggle = "on"
    gdb_execute(f'set pagination {toggle}')


def replace_last(s, repl, w):
    return s[::-1].replace(repl[::-1], w[::-1], 1)[::-1]


def gdb_execute(command):
    return gdb.execute(command, to_string=True)


def gdb_print(name):
    return gdb_execute(f'p {name}').split(' = ', 1)[1].split('\n', 1)[0]


def gdb_malloc_size(name):
    """
    Given some `name`, return the size of whatever `name` is (or is malloced to)
    """
    pointer = gdb_get_pointer(name)
    if pointer in gdb.mallocs:
        return gdb.mallocs[pointer]
    raise ValueError("Could not find address malloced anywhere.")


def gdb_is_array(name):
    if set("[]") < set(gdb_get_type(name)):
        # an array in memory
        return True

    try:
        malloc_size = int(gdb_malloc_size(name))
        elem_size = int(gdb_print(f'sizeof(*{name})'))
        num_elems = malloc_size / elem_size
        if num_elems > 1 and num_elems % 1 == 0:
            return True
    except:
        pass

    return False


def get_0x_in_string(string):
    try:
        return re.findall(r'\b0x[0-9a-f]*\b', string)[0]
    except IndexError:
        return None


def gdb_get_pointer(name):
    if name.startswith("0x"):
        return name
    name_type = gdb_get_type(name)
    pointer_indirection = name_type.count('*')
    # TODO: Deal with strings vs string arrays
    if pointer_indirection < 1:
        return gdb_get_pointer(f'&({name})')
    # elif pointer_indirection > 1:
    # return gdb_get_pointer(f"*({name})")
    pointer = get_0x_in_string(gdb_print(name))
    if pointer is None:
        raise RuntimeError("Couldn't find pointer!")
    return pointer


def gdb_struct_type(name):
    """
    """
    field_names = {}
    struct_ptype = gdb_execute(f'ptype {name}')
    for line in struct_ptype.split('\n'):
        line = line.replace(';', '').strip(' ')
        if not line or '{' in line or '}' in line:
            continue

        line_name = re.sub(r'\[\d*\]|\*', '', line)
        line_name = line_name.split(' ')[-1].strip(' ')
        line_type = replace_last(line, line_name, '')
        field_names[line_name] = line_type.strip(' ')

    return field_names


def gdb_get_type(name):
    """
    Invoke the gdb `whatis` command, but do so such that typedefs are ignored

    :param name: The name of the object to inspect.
    """
    command_input = name
    command_result = None
    for i in range(100):
        command_result = gdb_execute(f'whatis {command_input}')
        command_result = command_result.split('type = ')[1].replace('\n', '')
        if command_result == command_input:
            return command_result
        command_input = command_result
    else:
        raise ValueError(f"Could not determine true type of {name}")


def gdb_get_type_pair(name):
    is_array = gdb_is_array(name)
    is_struct = "struct" in gdb_get_type(name) and not is_array
    return is_array, is_struct 


def gdb_get_struct(name):
    struct_name = gdb_get_type(name)
    struct_type = gdb_struct_type(struct_name)
    struct = {}

    for field in struct_type:
        val = gdb_print(f'{name}->{field}')
        struct[field] = val

    return struct


def gdb_get_array(name):
    name_pointer = gdb_get_pointer(name)

    list_size = int(gdb_print(f'sizeof({name})'))
    if name_pointer in gdb.mallocs:
        list_size = int(gdb_malloc_size(name_pointer))

    elem_name = name + "[0]"
    elem_pointer = gdb_get_pointer(elem_name)
    elem_size = int(gdb_print(f'sizeof({elem_name})'))
    if elem_pointer in gdb.mallocs:
        elem_size = int(gdb_malloc_size(elem_pointer))

    list_len = list_size / elem_size
    assert(list_len % 1 == 0)
    list_len = int(list_len)

    list_rep = []
    for i in range(list_len):
        list_rep.append(gdb_print(f'{name}[{i}]'))

    return list_rep


def should_inspect(obj_type):
    if obj_type == "char *":
        return False
    return 'struct' in obj_type


def gdb_get_dump(obj_name, dump):
    obj_addr = gdb_get_pointer(obj_name)
    if obj_addr in dump:
        dump[obj_addr]['name'].append(obj_name)
        return obj_name, obj_addr
    obj_type = gdb_get_type(obj_name)

    is_array, is_struct = gdb_get_type_pair(obj_name)

    obj_references = {}

    obj_value = None

    if is_array:
        obj_value = gdb_get_array(obj_name)
    elif is_struct:
        obj_value = gdb_get_struct(obj_name)
    else:
        obj_value = gdb_print(obj_name)

    if is_array:
        for i, val in enumerate(obj_value):
            new_name = f"{obj_name}[{i}]"
            if should_inspect(gdb_get_type(new_name)):
                try:
                    conn_name, conn_addr = gdb_get_dump(new_name, dump)
                    obj_references[con_addr] = conn_name
                except gdb.MemoryError:
                    pass

    if is_struct:
        struct_type = gdb_struct_type(obj_name)
        for field_name in struct_type:
            if should_inspect(gdb_get_type(struct_type[field_name])):
                try:
                    conn_name, conn_addr = gdb_get_dump(f"{obj_name}->{field_name}", dump)
                    obj_references[conn_addr] = conn_name
                except gdb.MemoryError:
                    pass

    dump[obj_addr] = {
        'name': [obj_name],
        'type': obj_type,
        'value': obj_value,
        'references': obj_references,
        'type_bools': {
            'is_array': is_array,
            'is_struct': is_struct
        },
    }

    return obj_name, obj_addr
