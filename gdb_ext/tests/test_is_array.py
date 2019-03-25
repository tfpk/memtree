from .utils import get_output

def test_print():
    TESTS = {
        'i': True,
        'c': True,
        'sl': True,
        'slp': True,
        'io': False,
        'co': False,
        'so': False,
        'sop': False
    }
    
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
            struct s *slp[2]= {NULL, NULL};

            int io = 1;
            char co = 'c';
            struct s so = {1, 'a'};
            struct s *sop = NULL;

            return 0; // break
        }
        """,
        """
from gdb_interface import gdb_is_array
print(gdb_is_array('i') == True)
print(gdb_is_array('c') == True)
print(gdb_is_array('sl') == True)
print(gdb_is_array('slp') == True)
print(gdb_is_array('io') == False)
print(gdb_is_array('co') == False)
print(gdb_is_array('so') == False)
print(gdb_is_array('sop') == False)"""
    )
    assert(o == '\n'.join(["True"]*len(TESTS)))
