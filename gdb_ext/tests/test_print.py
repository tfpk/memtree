from .utils import get_output

def test_print():
    o = get_output(
        """
        int main(void){
            int i = 0;

            return 0; // break
        }
        """,
        "print(gdb_print('i'))"
    )
    assert(o == "0")
