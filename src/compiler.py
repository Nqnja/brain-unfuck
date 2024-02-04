import os
import re


class Instruction:
    def __init__(self, identifier: str, instructions: list[str], instr_type: str) -> None:
        self.identifier = identifier
        self.instructions = [instr for instr in instructions if instr != '']
        self.instr_type = instr_type # bf | bu

    def is_brainfuck(self):
        return self.instr_type == 'bf'

    def brainfuck_code(self):
        return self.instructions[0]


def read_file(path: str) -> Instruction:
    contents = ""
    with open(path, mode='r') as file:
        contents = file.read().replace('\n', ' ')

    split = re.split(r"[.\\\/]", path)
    extension = split[-1].lower()
    identifier = split[-2].lower()

    if extension == 'bf':
        # todo: remove comments from instructions
        return Instruction(identifier, [contents], 'bf')

    # todo: comments in brain unfuck
    instructions = [instr.lower() for instr in contents.split(' ')]
    
    return Instruction(identifier, instructions, 'bu')


def read_folder(path: str) -> list[Instruction]:
    instructions = []

    for root, _, files in os.walk(path):
        for file_name in files:
            instructions.append(read_file(f"{root}/{file_name}"))

    return instructions


def build_instruction_set(dependency_paths: list[str]) -> dict[str, str]:
    instructions: list[Instruction] = []
    
    for path in dependency_paths:
        if path.endswith('.bu') or path.endswith('.bf'):
            instructions += [read_file(path)]
        else:
            instructions += read_folder(path)

    all_valid = [instr.identifier for instr in instructions] + [str(i) for i in range(256)]

    result = {instr.identifier: instr.brainfuck_code() for instr in instructions if instr.is_brainfuck()}
    
    for i in range(256):
        result[str(i)] = "+" * i
    
    todo = [instr for instr in instructions if not instr.is_brainfuck()]

    while len(todo) > 0:
        for instr in todo:
            local_instructions = instr.instructions
            
            todo_identifiers = [i.identifier for i in todo]

            if instr in todo_identifiers:
                print(f"Found recursive instruction: {instr.identifier} -> {local_instr}")
                exit(1)

            for local_instr in set(local_instructions):
                if not (local_instr in all_valid):
                    print(f"Found missing instruction: {instr.identifier} -> {local_instr}")
                    exit(1)
                
                if not (local_instr in result):
                    break
            else:
                mapped = [result[k] for k in instr.instructions]

                final = ""
                for m in mapped:
                    final += m
                
                result[instr.identifier] = final

                todo.remove(instr)
    
    return result


def compile_brain_unfuck(program_path: str, dependency_paths: list[str] = ['./instructions']) -> str:
    instruction_set = build_instruction_set([program_path] + dependency_paths)

    instr_identifier = re.split(r"[.\\\/]", program_path)[-2]

    return instruction_set[instr_identifier].replace(' ', '')
