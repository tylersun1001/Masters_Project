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

import Module
import Converter
import sys
sys.path.insert(0, '../lib')

class HazardControl(Module):

    def __init__(self):
        super().__init__()
        self.three_cycle_stall = 0

        self.in_dict["id_rs1"] = "0000"
        self.in_dict["id_rs2"] = "0000"
        self.in_dict["ex_rd"] = "0000"
        self.in_dict["ex_mul_stage"] = "000"

        self.out_dict["if_id_stall"] = "0"
        self.out_dict["id_ex_stall"] = "0"

    def calculate_combinational(self):
        if (self.in_dict["ex_mul_stage"]) != "001":
            self.out_dict["if_id_stall"] = "1"
            self.out_dict["id_ex_stall"] = "1"
        elif (self.in_dict["ex_rd"] == self.in_dict["id_rs1"] or self.in_dict["ex_rd"] == self.in_dict["id_rs2"]):
            self.out_dict["if_id_stall"] = "1"
            self.out_dict["id_ex_stall"] = "1"
        elif (self.three_cycle_stall != 0):
            self.out_dict["if_id_stall"] = "1"
            self.out_dict["id_ex_stall"] = "1"
        else:
            self.out_dict["if_id_stall"] = "0"
            self.out_dict["id_ex_stall"] = "0"

    def update_state(self):
        if (self.in_dict["ex_rd"] == self.in_dict["id_rs1"] or self.in_dict["ex_rd"] == self.in_dict["id_rs2"]):
            self.three_cycle_stall = 1
        elif (self.three_cycle_stall != 0):
            self.three_cycle_stall += 1
        elif (self.three_cycle_stall == 3):
            self.three_cycle_stall = 0
