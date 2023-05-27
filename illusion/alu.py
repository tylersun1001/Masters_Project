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

import sys
sys.path.insert(0, '../lib')
from module import Module
from converter import Converter

class ALU(Module):

    def __init__(self):
        super().__init__()

        #self.m1_instr = "0000"
        #self.m1_r1 = "0000"
        #self.m1_r2 = "0000"
        self.m2_instr = "0000"
        self.m2_r1 = "0000"
        self.m2_r2 = "0000"
        self.ex_instr = "0000"
        self.ex_r1 = "0000"
        self.ex_r2 = "0000"

        self.in_dict["rs1_data"] = "0000"
        self.in_dict["rs2_data"] = "0000"
        self.in_dict["instr"] = "0000"

        self.out_dict["out"] = "0000"
        self.out_dict["alu_status"] = "0"       # 2 bit value.  alu_status[1] signals if a mul is in m2.  [0] signals if a mul is in ex.

    def calculate_combinational(self):
        alu_status_int = 0
        if (self.m2_instr != "0000"):
            alu_status_int += 2
        if (self.ex_instr != "0000"):
            alu_status_int += 1
        self.out_dict["alu_status"] = Converter.int2hex(alu_status_int)

        instr = self.in_dict["instr"]
        rs1_hex = self.in_dict["rs1_data"]
        rs2_hex = self.in_dict["rs2_data"]
        if (Converter.hex2int(self.out_dict["alu_status"]) > 0):
            instr = self.ex_instr
            rs1_hex = self.ex_r1
            rs2_hex = self.ex_r2

        opcode = instr[0]
        rs1_data = Converter.hex2int(rs1_hex)
        rs2_data = Converter.hex2int(rs2_hex)
        if (opcode in ["6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]):
            rs2_data = Converter.hex2int(instr[2])
        out_val = 0

        if (opcode == "0" or opcode == "6"):        #ADD, ADDI
            out_val = (rs1_data + rs2_data) % 2**16
        elif opcode == "1":                         #SUB
            out_val = (rs1_data - rs2_data) % 2**16
        elif (opcode == "2" or opcode == "7"):      #AND, ANDI
            out_val = rs1_data & rs2_data
        elif (opcode == "3" or opcode == "8"):      #OR, ORI
            out_val = rs1_data | rs2_data
        elif opcode == "4":                         #XOR
            out_val = rs1_data ^ rs2_data
        elif opcode == "9":                         #SLL
            out_val = (rs1_data << rs2_data) % 2**16
        elif opcode == "a":                         #SRL
            out_val = rs1_data >> rs2_data
        elif opcode == "5":                         #MUL
            product = rs1_data * rs2_data
            if (product > (2**16 - 1)):
                product = 2**16 - 1
            out_val = product
        
        self.out_dict["out"] = Converter.int2hex(out_val, 4)

    def update_state(self):
        opcode = self.in_dict["instr"][0]
        # proceed pipeline if there is a mul in flight in alu or to be added.  else, forward id_instr to ex_instr
        #if (Converter.hex2int(self.out_dict["alu_status"]) > 1 or opcode == "5"):
        self.ex_instr = self.m2_instr
        self.ex_r1 = self.m2_r1
        self.ex_r2 = self.m2_r2

        if (opcode == "5"):
            self.m2_instr = self.in_dict["instr"]
            self.m2_r1 = self.in_dict["rs1_data"]
            self.m2_r2 = self.in_dict["rs2_data"]
        else:
            self.m2_instr = "0000"
            self.m2_r1 = "0000"
            self.m2_r2 = "0000"
        
        
