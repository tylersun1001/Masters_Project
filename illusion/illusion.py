# The top level illusion module.

import Module
import Converter
import sys
sys.path.insert(0, '../lib')

class Illusion(Module):

    def __init__(self, filename: str="illusion_states.txt"):
        self.outfile = open(filename, "w")

        self.modules = {}
        self.modules["icache"] = ICache()
        self.modules["rf"] = RegisterFile()
        self.modules["alu"] = ALU()
        self.modules["dcache"] = DCache()
        self.modules["hc"] = HazardControl()
        #Program counter will be implemented in this top level module.

        self.pc = "0000"
        self.i_id = "0000"
        self.id_instr = "0000"
        self.alu_instr = "0000"
        self.mem_instr = "0000"
        self.mem_alu_out = "0000"

        self.comb_signals = {}
        update_comb_signals(self.comb_signals)
        
        self.comb_signals_new = self.comb_signals.copy()

    # while there is no difference between the two comb_signals dicts, run
    # calculate_combinational on all submodules
    def calculate_combinational(self):
        
    # update the state (positive clock edge).
    def update_state(self):
        # IF Stage
        if (self.modules["hc"].in_dict["if_id_stall"] == "0"):
            self.pc = Converter.int2hex(Converter.hex2int(self.pc) + 1, 4)
            self.modules["icache"].in_dict["rd_dest"] = pc
        
        # ID Stage
        if (self.modules["hc"].in_dict["if_id_stall"] == "0"):
            # based on the instruction, feed rs1 and rs2 into rf
            self.id_instr = self.modules["icache"].out_dict["rd_out"]
            opcode = id_instr[0]
            rs1 = "0"
            rs2 = "0"
            if (opcode in ["0", "1", "2", "3", "4", "5", "9", "a"]):
                rs1 = id_instr[1]
                rs2 = id_instr[2]
            # FIX THIS BASED ON THE ISA SPEC SHEET
            elif (opcode in ["6", "7", "8"]):
                rs1 = id_instr[2]
            
            # CONFIGURE WR, WR_DATA, WR_EN

        # EX Stage
        if (self.modules["hc"].in_dict["id_ex_stall"] == "0"):
            self.ex_instr = self.id_instr #FIX THIS (getting new value of instr)
            self.modules["alu"].in_dict["rs1_data"] = modules["rf"].out_dict["rd_1_data"]
            self.modules["alu"].in_dict["rs2_data"] = modules["rf"].out_dict["rd_2_data"]
            self.modules["alu"].in_dict["instr"] = self.ex_instr

        # MEM Stage
        # implement mem stall if needed (prob not)
        self.mem_alu_out = self.modules["alu"].out_dict["out"]
        self.mem_instr = self.ex_instr #FIX THIS (getting new value of instr)
        # based on the current instr, determine what inputs to dcache should be
        self.modules["dcache"].in_dict["rd_dest"] = "urmom"

        # WB Stage
        # \
        self.wb_instr = self.mem_instr #FIXME
        # based on the instr, determine if alu_out, mem_out or nothing should be
        # put back into the registerfile.
        self.modules["rf"].in_dict["wr"] = self.wb_instr[3]
        self.modules["rf"].in_dict["wr_en"] = "1"
        if (self.wb_instr in ["", ]):    #instrs that use alu result
            self.modules["rf"].in_dict["wr_data"] = self.mem_alu_out #FIXME
        elif ():
            self.modules["rf"].in_dict["wr_data"] = self.modules["dcache"].out_dict["rd_out"]
        else:
            self.modules["rf"].in_dict["wr_en"] = "0"

        
    # update the given comb_signals dict based on the current self.modules dict.
    def update_comb_signals(self, signal_dict: dict):
        for module_name in self.modules.keys():
            module = self.modules[module_name]
            for signal_name in module.out_dict.keys():
                total_signal_name = module_name + "." + signal_name
                signal_dict[total_signal_name] = module[signal_name]

    # record the state in the outfile.  pc and i_id, then all the signals
    # in modules dict.
    def record_state(self):
        self.outfile.write("pc " + self.pc + "\n")
        self.outfile.write("i_id" + self.i_id + "\n")
        for signal_name in self.signal_dict.keys():
            self.outfile.write(signal_name + " " + self.signal_dict[signal_name] + "\n")
        self.outfile.write("\n")

def main():
    illusion = Illusion()
    while (True):
        illusion.calculate_combinational()
        illusion.update_state()
        illusion.record_state()

if __name__ == "__main__":
    main()

        


