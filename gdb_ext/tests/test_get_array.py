from .utils import get_output

def test_print():
    TESTS = {
        'i': 3,
        'c': 6,
        'sl': 2,
        'slp': 3,
    }
    print('\n'.join([(f"len(__import__('gdb_interface').gdb_get_array('{x}')) == {state}") for x, state in TESTS.items()]))
    o = get_output(
        """
        #define NULL 0x0
        int main(void){
            struct s {
                int a;
                char c;
            };
            int i[3] = {0, 1, 2};
            char c[6] = {'h', 'e', 'l', 'l', 'o', '\\0'};
            struct s sl[2] = {{1, 'a'}, {2, 'b'}};
            struct s *slp[3]= {NULL, NULL, NULL};

            return 0; // break
        }
        """,
        """
import gdb_interface
print(len(gdb_interface.gdb_get_array('i')) == 3)
print(len(gdb_interface.gdb_get_array('c')) == 6)
print(len(gdb_interface.gdb_get_array('sl')) == 2)
print(len(gdb_interface.gdb_get_array('slp')) == 3)
        """
    )
    print(o)
    assert(o == '\n'.join(["True"]*len(TESTS)))
