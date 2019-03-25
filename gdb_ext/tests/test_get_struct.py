from .utils import get_output

import pathlib, tempfile


def test_get_struct():

    o = get_output(
        """
        #define NULL 0x0
        int main(void){
            struct s {
                int i;
                char c;
                int ints[4];
            };
            struct s s = {1, 'c', {5,6,7,8}};
            struct s sl[2] = {{1, 'c', {5,6,7,8}}, {1, 'd', {9,6,4,2}}};
            return 0; // break
        }
        """,
        """
import gdb_interface

TEST = {'i': '1', 'c': "99 'c'", 'ints': '{5, 6, 7, 8}'} 
print(gdb_interface.gdb_get_struct('s') == TEST)
try:
    s = gdb_interface.gdb_get_struct('sl')
    print(False)
except ValueError:
    print(True)
    """)
    print(o)

    assert(o == 'True\nFalse')
