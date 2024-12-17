from src.compiler import compile_brain_unfuck
from src.interpreter import interpret

import sys


def pretty_out_write(program: str):
    with open('./output.bf', 'w') as file:
        acc = ""
        lines = []

        for c in program:
            acc += c
            if len(acc) == 80:
                lines.append(f"{acc}")
                acc = ""
        
        lines.append(acc)
        lines.append("")

        file.write("\n".join(lines))


def main(*args):
    args = args[0]

    if len(args) < 2 or len(args[1]) == 0:
        print("Please specify the path to your brain( un)fuck file, for example:")
        print(" > py ./main.py ./addition.bu")
        print("")
        print("You can also specify your own instruction set by specifying additional folders or files:")
        print(" > py ./main.py ./addition.bu ./instructions")
        print("")
        print("Extra specified dependencies will be ignored if your input file path ends with '.bf'. I also assume you stick to '.bu' or '.bf' file extensions")
        print("")
        exit(1)

    program_path = args[1]
    if program_path.endswith('.bu'):
        print("Compiling to brainfuck..")
        dependency_paths = args[2:]
        if len(dependency_paths) == 0:
            dependency_paths = ['./instructions']
        program = compile_brain_unfuck(program_path, dependency_paths)
        print(f"Compiled to brainfuck program of length {len(program)}")

        print("Writing output program to file 'output.bf'..")
        pretty_out_write(program)
    else:
        with open(program_path, 'r') as file:
            program = file.read().replace('\n', '')

    print("Interpreter started! You can now interact with your program.")
    interpret(program)


if __name__ == '__main__':
    main(sys.argv)
