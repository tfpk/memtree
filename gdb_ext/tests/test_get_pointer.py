from .utils import get_output


def test_get_pointer():
    o = get_output(
        """
#include <stdlib.h>
char *chars[3] = {"one", "two", "three"};
typedef struct rand_struct {
    int a;
    int *b;
    char c;
} rand_struct;
int main(void){
    int i = 0;
    int *pointer_in_stack = &i;
    rand_struct struct_stack = {1, &i, 'c'};
    rand_struct *struct_heap = calloc(1, sizeof(rand_struct));

    return 0; // break
        }
        """,
        """
from gdb_interface import gdb_get_pointer
print(gdb_get_pointer('pointer_in_stack'))
print(gdb_get_pointer('struct_stack'))
print(gdb_get_pointer('&struct_heap'))
print(gdb_get_pointer('&chars'))
print(gdb_get_pointer('chars'))
        """
    )
    # this test is not portable (consider changing it to just check relatively)
    assert(len(o.split("\n")) == 5)
