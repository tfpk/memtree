import tempfile
from pathlib import Path

import subprocess

import os
DIR = os.path.dirname(os.path.abspath(__file__))

GDB_PRECOMMANDS = [
    f'source {DIR}/../gdb_commands.py',
]
GDB_POSTCOMMANDS = [
    'set confirm off',
    'q'
]
GDB_COMMAND = "gdb -q "

COMMAND_SIGNAL = "|=+=-=+=|"

def get_output(program, test, break_line=None):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d)
        if break_line is None:
            for i, line in enumerate(program.split('\n')):
                if "// break" in line:
                    break_line = i + 1
        with open(path / 'file.c', 'w') as f:
            f.write(program)

        with open(path / 'test.py', 'w') as f:
            f.write(test)

        try:
            compile_output = subprocess.check_output(
                f'cd {str(d)} && gcc -g -o file file.c',
                shell=True
            )
        except subprocess.CalledProcessError as e:
            print("=== Compile failed ===")
            assert(False)

        commands = [f'b {break_line}', 'r', f'python print(\\"{COMMAND_SIGNAL}\\")']
        commands += [f"source {path / 'test.py'}", f'python print(\\"{COMMAND_SIGNAL}\\")']

        commands = GDB_PRECOMMANDS + commands + GDB_POSTCOMMANDS

        command = GDB_COMMAND + ' '.join(
            [f'-ex="{x}"' for x in commands]
        ) + f' {str(path)}/file'

        out = subprocess.check_output(command, shell=True).decode('utf-8')
        return out.split(COMMAND_SIGNAL)[1].strip('\n')

