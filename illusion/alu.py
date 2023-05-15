# The registerfile module in the illusion python model.
# The in{} dictionary contains the inputs.
#   rs1_data:   [15:0]
#   rs2_data:   [15:0]
#   instr:      [15:0]
#
# The out{} dictionary contains the combinational outputs.
#   out:        [15:0]
#   mul_stage:  [2:0]       //One hot encoding
#                               001 = mul_done
#                               010 = mul_second stage
#                               100 = mul_first stage

import Module
import Converter
import sys
sys.path.insert(0, '../lib')

class ALU(Module):

    def __init__(self):
        super().__init__()
        self.mul_stage = 0

        self.in_dict["rs1_data"] = "0000"
        self.in_dict["rs2_data"] = "0000"
        self.in_dict["instr"] = "0000"

        self.out_dict["out"] = "0000"
        self.out_dict["mul_stage"] = "0"

    def calculate_combinational(self):
        opcode = self.in_dict["instr"][0]
        rs1_data = Convert.hex2int(self.in_dict["rs1_data"])
        rs2_data = Convert.hex2int(self.in_dict["rs2_data"])
        out_val = 0

        self.out_dict["mul_stage"] = "1"
        if (opcode == "0" or opcode == "6"):        #ADD, ADDI
            out_val = rs1_data + rs2_data % 2**16
        elif opcode == "1":                         #SUB
            out_val = rs1_data - rs2_data % 2**16
        elif (opcode == "2" or opcode == "7"):      #AND, ANDI
            out_val = rs1_data & rs2_data
        elif (opcode == "3" or opcode == "8"):      #OR, ORI
            out_val = rs1_data | rs2_data
        elif opcode == "4":                         #XOR
            out_val = rs1_data ^ rs2_data
        elif opcode == "9":                         #SLL
            out_val = rs1_data << rs2_data % 2**16
        elif opcode == "a":                         #SRL
            out_val = rs1_data >> rs2_data
        elif opcode == "5":                         #MUL
            out_val = 0
            self.mul_stage += 1
            if (mul_stage == 3):
                product = rs1_data * rs2_data
                if (product > (2**16 - 1)):
                    product = 2**16 - 1
                out_val = product
                self.mul_stage = 0
        
        self.out_dict["mul_stage"] = Converter.int2hex(2 - self.mul_stage)
        self.out_dict["out"] = Converter.int2hex(out_val, 4)

