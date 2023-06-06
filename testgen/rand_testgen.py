# Generates a file which contains a list of instructions in hex format.

# Currently only generates arithmetic operations.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import random
from converter import Converter

class testgen:

    def __init__(self, outfile: str="temp", seed: str="defaultseed"):
        random.seed(seed)
        self.f = open(outfile, "w")

    def rand_arith_instr(self):
        field3 = format(random.randint(0, 10), '04b')  #opcode
        field2 = format(random.randint(0, 15), '04b')
        field1 = format(random.randint(0, 15), '04b')
        field0 = format(random.randint(0, 15), '04b')
        
        bininstr = "0b" + field3 + field2 + field1 + field0
        hexinstr = format(int(bininstr, 2), '04x')

        self.f.write(hexinstr + "\n")

    # does not wb into x13-15 (these are the jump registers)
    # random non branching instr
    def rand_instr(self) -> str:
        field3 = format(random.randint(0, 12), '04b')  #opcode
        field2 = format(random.randint(0, 15), '04b')
        field1 = format(random.randint(0, 15), '04b')
        field0 = format(random.randint(0, 12), '04b')
        
        bininstr = "0b" + field3 + field2 + field1 + field0
        hexinstr = format(int(bininstr, 2), '04x')

        return hexinstr + "\n"
        #self.f.write(hexinstr + "\n")

    # init every register as 0 through addi
    def init_sequence_zeros(self):
        field3 = "0110"
        field2 = "0000"
        field1 = "0000"
        field0 = "0000"
        for i in range(16):
            self.f.write(format(int("0b" + field3 + field2 + field1 + field0, 2), '04x') + "\n")
            field0 = format(int(field0, 2) + 1, '04b')

    # init every register w/ their register name number through addi
    def init_sequence(self):
        field3 = "0110"
        field2 = "0000"
        field1 = "0000"
        field0 = "0000"
        for i in range(16):
            self.f.write(format(int("0b" + field3 + field2 + field1 + field0, 2), '04x') + "\n")
            field0 = format(int(field0, 2) + 1, '04b') 
            field1 = field0       

    # init every register randomly through addi
    def init_random_sequence(self):
        field3 = "0110"
        field2 = "0000"
        field1 = "0000"
        field0 = "0000"
        for i in range(16):
            field1 = format(random.randint(0, 15), '04b')
            self.f.write(format(int("0b" + field3 + field2 + field1 + field0, 2), '04x') + "\n")
            field0 = format(int(field0, 2) + 1, '04b')

    def nops(self, n: int):
        for i in range(n):
            self.f.write("0000\n")

    # creates a random block of code of length 80 to 128 instrs long.
    # repeatedly called to create the final program
    def random_code_block(self) -> str:
        code_block = ""
        block_len = random.randint(80, 128)
        num_programs = random.randint(0, 3)
        # determine the programs.
        # first program (1-15 iteration for loop):
        program_1 = "6001\n"
        iter_len = random.randint(1, 15)
        program_1 += "60" + Converter.int2hex(iter_len, 1) + "2\n"
        program_1 += "6111\nd1f2\nff00\n"

        # second program (11-25 instrs per call, each instr 10% to be call to prg1)
        program_2 = ""
        program_2_len = random.randint(11, 25)
        for i in range(program_2_len - 1):
            if (random.randint(0, 9) == 0):
                jump_imm = i + 5
                jump_imm_str = Converter.int2hex(256 - jump_imm, 2)
                program_2 += ("e" + jump_imm_str + "f\n")
            else:
                program_2 += self.rand_instr()
        program_2 += "fe00\n"

        # third program (17 - 33 instrs per call, 3.3% call prg 2, 6.6% call prg1)
        program_3 = ""
        program_3_len = random.randint(17, 33)
        for i in range(program_3_len - 1):
            temp = random.randint(0, 29)
            if (temp == 0):
                jump_imm = i + program_2_len
                jump_imm_str = Converter.int2hex(256 - jump_imm, 2)
                program_3 += ("e" + jump_imm_str + "e\n")
            elif (temp < 3):
                jump_imm = i + program_2_len + 5
                jump_imm_str = Converter.int2hex(256 - jump_imm, 2)
                program_3 += ("e" + jump_imm_str + "f\n")
            else:
                program_3 += self.rand_instr()
        program_3 += "fd00\n"
        
        # jump past the programs to start code block
        jump_imm = 1
        if (num_programs > 0):
            jump_imm += 5
        if (num_programs > 1):
            jump_imm += program_2_len
        if (num_programs > 2):
            jump_imm += program_3_len
        if (num_programs > 0):
            code_block += "e" + Converter.int2hex(jump_imm, 2) + "0\n"

        programs_len = 0
        if (num_programs > 0):
            code_block += program_1
            programs_len += 6
        if (num_programs > 1):
            code_block += program_2
            programs_len += program_2_len
        if (num_programs > 2):
            code_block += program_3
            programs_len += program_3_len

        for i in range(block_len - programs_len):
            if (num_programs > 0):
                if (random.randint(0, 9) == 0):
                    temp = random.randint(1, num_programs)
                    if (temp == 1):
                        jump_imm = i + (programs_len - 1)
                        jump_imm_str = Converter.int2hex(256 - jump_imm, 2)
                        code_block += "e" + jump_imm_str + "f\n"
                    elif (temp == 2):
                        jump_imm = i + (programs_len - 6)
                        jump_imm_str = Converter.int2hex(256 - jump_imm, 2)
                        code_block += "e" + jump_imm_str + "e\n"
                    else:
                        jump_imm = i + (programs_len - program_2_len - 6)
                        jump_imm_str = Converter.int2hex(256 - jump_imm, 2)
                        code_block += "e" + jump_imm_str + "d\n"
                else:
                    code_block += self.rand_instr()
            else:
                code_block += self.rand_instr()
        return code_block

    def write(self, write_str: str):
        self.f.write(write_str)
            
    # Stores d074 to memory address d074.  This signifies end of test to checkers.
    def end_of_test_sequence(self):
        self.f.write("600f\n6fdf\n9f4f\n6f0f\n9f4f\n6f7f\n9f4f\n6f4f\ncf0f\n")

def main(n: int = 100, outfile: str = "generated_test.txt"):
    testgenerator = testgen(outfile)
    testgenerator.init_sequence()
    for i in range(n):
        testgenerator.write(testgenerator.random_code_block())
    testgenerator.end_of_test_sequence()
    testgenerator.nops(10)


if __name__ == "__main__":
    main(n=500)