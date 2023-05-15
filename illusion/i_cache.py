# The registerfile module in the illusion python model.
# The in{} dictionary contains the inputs.
#   rd_dest:        [15:0]
#
# The out{} dictionary contains the combinational outputs.
#   rd_out:         [15:0]

import Module
import Converter
import sys
sys.path.insert(0, '../lib')

class ICache(Module):

    def __init__(self):
        super().__init__()
        self.data = ["0000"] * 2**16
        self.curr_out = "0000"

        self.in_dict["rd_dest"] = "0000"

        self.out_dict["rd_out"] = "0000"

    def calculate_combinational(self):
        self.out_dict["rd_out"] = self.curr_out

    def update_state(self):
        rd_index = Converter.hex2int(in_dict["rd_dest"])
        self.curr_out = self.data[rd_index]


