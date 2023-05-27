# The registerfile module in the illusion python model.
# The in{} dictionary contains the inputs.
#   id_rs1:             [3:0]
#   id_rs2:             [3:0]
#   ex_rd:              [3:0]
#   ex_mul_stage:       [2:0]
#
# The out{} dictionary contains the combinational outputs.
#   if_id_stall:        [0:0]
#   id_ex_stall:        [0:0]
#   ex_mem_stall:       [0:0]      (? may not be needed)

import sys
sys.path.insert(0, '../lib')
from module import Module
from converter import Converter

class HazardControl(Module):

    def __init__(self):
        super().__init__()

        self.in_dict["id_rs1"] = "0"
        self.in_dict["id_rs2"] = "0"
        self.in_dict["ex_rd"] = "0"
        self.in_dict["mem_rd"] = "0"
        self.in_dict["wb_rd"] = "0"
        self.in_dict["alu_status"] = "0"
        self.in_dict["m1_instr"] = "0000"

        self.out_dict["if_id_stall"] = "0"
        self.out_dict["id_ex_stall"] = "0"

    def calculate_combinational(self):
        if (Converter.hex2int(self.in_dict["alu_status"]) > 1 or self.in_dict["m1_instr"][0] == "5"):
            self.out_dict["if_id_stall"] = "1"
            self.out_dict["id_ex_stall"] = "1"
        elif ((self.in_dict["id_rs1"] != "0" and self.in_dict["id_rs1"] in [self.in_dict["ex_rd"], self.in_dict["mem_rd"], self.in_dict["wb_rd"]])
                or (self.in_dict["id_rs2"] != "0" and self.in_dict["id_rs2"] in [self.in_dict["ex_rd"], self.in_dict["mem_rd"], self.in_dict["wb_rd"]])):
            self.out_dict["if_id_stall"] = "1"
            self.out_dict["id_ex_stall"] = "1"
        else:
            self.out_dict["if_id_stall"] = "0"
            self.out_dict["id_ex_stall"] = "0"
