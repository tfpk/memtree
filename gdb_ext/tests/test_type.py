from .utils import get_output

def test_get_type():
    INPUT = """
print(gdb_get_type('i'))
print(gdb_get_type('a'))
print(gdb_get_type('struct_instance'))
print(gdb_get_type('union_instance'))
print(gdb_get_type('*(union_instance->z)'))
print(gdb_get_type('union_instance->z'))
print(gdb_get_type('&(union_instance->z)'))
"""

    OUTPUT = """
int
void *
struct a_struct
union u
struct a_struct *
struct a_struct *[2]
struct a_struct *(*)[2]
"""

    # "gdb_get_type('&(&(union_instance->z))')": "this fails, since not in memory",
    o = get_output(
        """
        int main(void){
            int i = 0;
            void *a = (void *) 0x0;
            typedef struct a_struct {
                int a;
                int b;
            } AStruct;
            typedef struct a_struct *PAStruct;
            AStruct struct_instance;

            union u {
                struct a_struct *z [2];
                int y;
            };
            union u union_instance;

            return 0; // break
        }
        """,
        INPUT
    )
    assert(o.strip() == OUTPUT.strip())
