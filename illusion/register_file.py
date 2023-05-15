# The registerfile module in the illusion python model.
# The in{} dictionary contains the inputs.
#   rd_1: [3:0]
#   rd_2: [3:0]
#   wr:  [3:0]
#   wr_data: [15:0]
#   wr_en:   [0:0]
#
# The out{} dictionary contains the combinational outputs.
#   rd_1_data:    [15:0]
#   rd_2_data:    [15:0]

import Module
import Converter
import sys
sys.path.insert(0, '../lib')

class RegisterFile(Module):

    def __init__(self):
        super().__init__()
        self.registers = ["0000"] * 16

        self.in_dict["rd_1"] = "0"
        self.in_dict["rd_2"] = "0"
        self.in_dict["wr"] = "0"
        self.in_dict["wr_data"] = "0000"
        self.in_dict["wr_en"] = "0"

        self.out_dict["rd_1_data"] = "0000"
        self.out_dict["rd_2_data"] = "0000"

    def calculate_combinational(self):
        read1_index = Converter.hex2int(in_dict["rd_1"])
        read2_index = Converter.hex2int(in_dict["rd_2"])

        self.out_dict["rd_1_data"] = self.registers[read1_index]
        self.out_dict["rd_2_data"] = self.registers[read2_index]

    def update_state(self):
        write_index = Converter.hex2int(in_dict["wr"])
        
        if (self.in_dict["wr_en"] == "1"):
            self.registers[write_index] = self.in_dict["wr_data"]

