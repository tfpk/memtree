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
                int ints[4]; };
            return 0; // break
        }
        """,
        """
import gdb_interface
TEST = {
    'i': 'int',
    'c': 'char',
    'ints': 'int [4]'
}
print(gdb_interface.gdb_get_struct_desc('struct s') == TEST)
    """)
    print(o)

    assert(o == 'True\nFalse')
