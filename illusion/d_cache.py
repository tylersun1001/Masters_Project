# The dcache module in the illusion python model.
# The in{} dictionary contains the inputs.
#   rd_dest:        [15:0]
#   rd_en:          [0:0]
#   wr_dest:        [15:0]
#   wr_data:        [15:0]
#   wr_en:          [0:0]
#
# The out{} dictionary contains the combinational outputs.
#   rd_out:         [15:0]

import sys
sys.path.insert(0, '../lib')
from module import Module
from converter import Converter

class DCache(Module):

    def __init__(self):
        super().__init__()
        self.data = ["0000"] * 2**16
        self.curr_out = "0000"

        self.in_dict["rd_dest"] = "0000"
        self.in_dict["rd_en"] = "0"
        self.in_dict["wr_dest"] = "0000"
        self.in_dict["wr_data"] = "0000"
        self.in_dict["wr_en"] = "0"

        self.out_dict["rd_out"] = "0000"

    def calculate_combinational(self):
        self.out_dict["rd_out"] = self.curr_out

    def update_state(self):
        rd_index = Converter.hex2int(self.in_dict["rd_dest"])
        wr_index = Converter.hex2int(self.in_dict["wr_dest"])

        if self.in_dict["rd_en"] == "1":
            self.curr_out = self.data[rd_index]
        if (self.in_dict["wr_en"] == "1"):
            self.registers[write_index] = self.in_dict["wr_data"]

