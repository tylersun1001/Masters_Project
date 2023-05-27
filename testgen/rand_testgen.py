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

    def rand_instr(self):
        field3 = format(random.randint(0, 10), '04b')  #opcode
        #print(field3)
        field2 = format(random.randint(0, 15), '04b')
        field1 = format(random.randint(0, 15), '04b')
        field0 = format(random.randint(0, 15), '04b')
        
        bininstr = "0b" + field3 + field2 + field1 + field0
        hexinstr = format(int(bininstr, 2), '04x')
        #print(bininstr)
        #print(hexinstr)
        self.f.write(hexinstr + "\n")

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

def main(n: int = 100, outfile: str = "generated_test.txt"):
    testgenerator = testgen(outfile)
    testgenerator.init_sequence()
    for i in range(n):
        testgenerator.rand_instr()


if __name__ == "__main__":
    main(n=250)