from .utils import get_output

import pathlib, tempfile


def test_get_struct():

    o = get_output(
        """
#include <stdlib.h>

int main(){
    char *m_size_8 = malloc(8);
    char *f_size_8 = malloc(8);
    char *c_size_8 = calloc(8, sizeof(char));

    char *r_size_8_to_6 = malloc(8);
    char *old_r_size_8_to_6 = r_size_8_to_6;
    r_size_8_to_6 = realloc(r_size_8_to_6, 6);

    char *r_size_8_to_200 = malloc(8);
    char *old_r_size_8_to_200 = r_size_8_to_200;
    r_size_8_to_200 = realloc(r_size_8_to_200, 200);

    free(f_size_8); // break
}
        """,
        """
from gdb_interface import gdb_malloc_size

print([
    gdb_malloc_size('m_size_8') == 8,
    gdb_malloc_size('c_size_8') == 8,
    gdb_malloc_size('old_r_size_8_to_6') in [6, 0],
    gdb_malloc_size('r_size_8_to_6') == 6,
    gdb_malloc_size('old_r_size_8_to_200') in [200, 0],
    gdb_malloc_size('r_size_8_to_200') == 200,
])
    """)

    assert(o == '[' + ', '.join(['True']*6) + ']')
