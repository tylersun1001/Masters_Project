# The registerfile module in the illusion python model.
# The in{} dictionary contains the inputs.
#   rd_dest:        [15:0]
#
# The out{} dictionary contains the combinational outputs.
#   rd_out:         [15:0]

from module import Module
from converter import Converter

class ICache(Module):

    def __init__(self, program: str):
        super().__init__()
        self.data = ["0000"] * 2**16
        instrs = open(program, "r")
        for i, instr in enumerate(instrs):
            self.data[i] = instr.strip()

        self.curr_out = "0000"

        self.in_dict["rd_dest"] = "0000"
        self.in_dict["nop"] = "0"

        self.out_dict["rd_out"] = "0000"

    def calculate_combinational(self):
        self.out_dict["rd_out"] = self.curr_out
        #rd_index = Converter.hex2int(self.in_dict["rd_dest"])
        #self.out_dict["rd_out"] = self.data[rd_index]

    def update_state(self):
        pass
        rd_index = Converter.hex2int(self.in_dict["rd_dest"])
        self.curr_out = self.data[rd_index]
        if (self.in_dict["nop"] == "1"):
            self.curr_out = "0000"


