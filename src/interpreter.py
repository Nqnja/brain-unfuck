import msvcrt
import time


class State:
    def __init__(
            self,
            program: str,
            memory_size: int,
            instr_count_limit: int
    ):
        self.program = program
        self.memory = [0 for _ in range(memory_size)]
        self.instr_count_limit = instr_count_limit

        self.instr_count = 0

        self.memory_ptr = 0
        self.instr_ptr = 0
    
    def read_memory_at_current_ptr(self):
        self._assert_valid_memory_ptr()
        return self.memory[self.memory_ptr]

    def set_memory_at_current_ptr(self, value: int):
        self._assert_valid_memory_ptr()
        self.memory[self.memory_ptr] = value % 256

    def read_program_at_current_ptr(self):
        return self.program[self.instr_ptr]

    # returns True if the program should be terminated
    def add_to_instr_ptr(self, a: int) -> bool:
        self.instr_ptr += a

        return self.instr_ptr >= len(self.program)

    def add_to_memory_ptr(self, a: int):
        self.memory_ptr += a

    def _assert_valid_memory_ptr(self):
        if self.memory_ptr < 0:
            print("")
            print("Memory read failed because memory pointer < 0")
            self.debug()
            exit(1)
        
        if self.memory_ptr >= len(self.memory):
            print("")
            print("Memory read failed because memory pointer > size of memory")
            self.debug()
            exit(1)

    def debug(self):
        print("")
        print(f"Memory pointer: {self.memory_ptr}")
        print(f"Instruction pointer: {self.instr_ptr}")

        last = 0
        for i in range(len(self.memory)):
            if self.memory[i] > 0:
                last = i

        print(f"Memory dump: {self.memory[:max(last, self.memory_ptr)+1]}")


def interpret(
        program: str, 
        memory_size: int = 30_000,
        instr_count_limit: int = 100_000 
) -> int:
    state = State(
        program=program,
        memory_size=memory_size,
        instr_count_limit=instr_count_limit
    )

    another = True
    while another:
        another = step(state)


# returns whether we want to continue after this step
def step(state: State) -> bool:
    instr = state.read_program_at_current_ptr()

    match instr:
        case '>':
            state.add_to_memory_ptr(1)
        case '<':
            state.add_to_memory_ptr(-1)
            
        case '+':
            state.set_memory_at_current_ptr(state.read_memory_at_current_ptr() + 1)
        case '-':
            state.set_memory_at_current_ptr(state.read_memory_at_current_ptr() - 1)
            
        case '.':
            print(chr(state.read_memory_at_current_ptr()), end='', flush=True)
        case ',':
            state.set_memory_at_current_ptr(ord(msvcrt.getch()))

        case '[':
            skip = state.read_memory_at_current_ptr()
            if skip == 0:
                level = 1
                while level > 0:
                    state.add_to_instr_ptr(1)
                    instr = state.read_program_at_current_ptr()
                    if instr == '[':
                        level += 1
                    elif instr == ']':
                        level -= 1
        case ']':
            skip = state.read_memory_at_current_ptr()
            if skip != 0:
                level = 1
                while level > 0:
                    state.add_to_instr_ptr(-1)
                    instr = state.read_program_at_current_ptr()
                    if instr == ']':
                        level += 1
                    elif instr == '[':
                        level -= 1
        
        # only custom instruction: allows to print all memory
        case '#':
            state.debug()
    
    if state.add_to_instr_ptr(1):
        return False
    
    return True
