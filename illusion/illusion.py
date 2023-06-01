# The top level illusion module.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from module import Module
from i_cache import ICache
from register_file import RegisterFile
from alu import ALU
from d_cache import DCache
from hazard_control import HazardControl

from converter import Converter

class Illusion(Module):

    def __init__(self, program: str = "../testgen/branch_test.txt", filename: str="illusion_states.txt"):
        self.outfile = open(filename, "w")
        self.eot_instr_in_mem = False
        self.eot = False

        self.modules = {}
        self.modules["icache"] = ICache(program)
        self.modules["rf"] = RegisterFile()
        self.modules["alu"] = ALU()
        self.modules["dcache"] = DCache()
        self.modules["hc"] = HazardControl()
        #Program counter will be implemented in this top level module.

        self.pc = "0000"
        self.id_pc = "0000"
        self.ex_pc = "0000"
        self.mem_pc = "0000"
        self.wb_pc = "0000"

        self.i_id = "0000"
        self.id_instr = "0000"
        self.m1_instr = "0000"
        self.mem_instr = "0000"
        self.wb_instr = "0000"

        self.mem_alu_out = "0000"
        self.wb_alu_out = "0000"

        self.mem_r2_data = "0000"

        self.comb_signals = {}
        self.update_comb_signals(self.comb_signals)
        
        self.comb_signals_new = self.comb_signals.copy()

    # while there is no difference between the two comb_signals dicts, run
    # calculate_combinational on all submodules
    def calculate_combinational(self):
        while(True):
            self.update_comb_signals(self.comb_signals)
            
            #update the in signals in the modules/propogate combinational signals

            # IF
            if (self.modules["hc"].out_dict["if_id_stall"] == "0"):
                self.pc = Converter.int2hex(Converter.hex2int(self.id_pc) + 1, 4)
                if (self.modules["alu"].out_dict["br_taken"] == "1"):
                    self.pc = self.modules["alu"].out_dict["br_target"]
            else:
                self.pc = self.id_pc
            self.modules["icache"].in_dict["rd_dest"] = self.pc
            self.modules["icache"].in_dict["nop"] = "0"
            if (self.modules["hc"].out_dict["if_id_stall"] == "1" and self.modules["hc"].out_dict["id_ex_stall"] == "0"):
                self.modules["icache"].in_dict["nop"] = "1"

            # ID
            self.id_instr = self.modules["icache"].out_dict["rd_out"]
            id_opcode = self.id_instr[0]
            rd1 = self.id_instr[1]
            if (id_opcode == "e"):
                rd1 = "0"
            rd2 = "0"
            if (id_opcode in ["0", "1", "2", "3", "4", "5"]):
                rd2 = self.id_instr[2]
            elif (id_opcode in ["c", "d"]):
                rd2 = self.id_instr[3]
            
            self.modules["rf"].in_dict["rd_1"] = rd1
            self.modules["rf"].in_dict["rd_2"] = rd2
            # wr, wr_data, wr_en are configured in wb stage above

            # EX
            self.modules["alu"].in_dict["rs1_data"] = self.modules["rf"].out_dict["rd_1_data"]
            self.modules["alu"].in_dict["rs2_data"] = self.modules["rf"].out_dict["rd_2_data"]
            self.modules["alu"].in_dict["instr"] = self.m1_instr
            self.modules["alu"].in_dict["pc"] = self.ex_pc

            # MEM
            # based on the current instr, determine what inputs to dcache should be
            mem_opcode = self.mem_instr[0]
            if (mem_opcode == "b"):
                self.modules["dcache"].in_dict["rd_en"] = "1"
                self.modules["dcache"].in_dict["rd_dest"] = self.mem_alu_out
            elif (mem_opcode == "c"):
                self.modules["dcache"].in_dict["wr_en"] = "1"
                self.modules["dcache"].in_dict["wr_dest"] = self.mem_alu_out
                self.modules["dcache"].in_dict["wr_data"] = self.mem_r2_data

            # WB
            # based on the instr, determine if alu_out, mem_out or nothing should be
            # put back into the registerfile.
            self.modules["rf"].in_dict["wr"] = self.wb_instr[3]
            self.modules["rf"].in_dict["wr_en"] = "1"
            wb_opcode = self.wb_instr[0]
            if (wb_opcode == "b"):    #load instr => use dcache output
                self.modules["rf"].in_dict["wr_data"] = self.modules["dcache"].out_dict["rd_out"]
            else:           
                self.modules["rf"].in_dict["wr_data"] = self.wb_alu_out #FIXME
            if (wb_opcode in ["c", "d"]):       # store & beq do not wb into rf
                self.modules["rf"].in_dict["wr_en"] = "0"

            # Hazard Control
            self.modules["hc"].in_dict["id_instr"] = self.id_instr
            self.modules["hc"].in_dict["ex_rd"] = self.m1_instr[3]
            if (self.m1_instr[0] in ["c", "d"]):
                self.modules["hc"].in_dict["ex_rd"] = "0"
            self.modules["hc"].in_dict["m1_instr"] = self.m1_instr
            if (self.modules["alu"].out_dict["alu_status"] != "0" or self.m1_instr[0] == "5"):
                self.modules["hc"].in_dict["ex_rd"] = self.modules["alu"].ex_instr[3]
            self.modules["hc"].in_dict["mem_rd"] = self.mem_instr[3]
            if (self.mem_instr[0] in ["c", "d"]):
                self.modules["hc"].in_dict["mem_rd"] = "0"
            self.modules["hc"].in_dict["wb_rd"] = self.wb_instr[3]
            if (self.wb_instr[0] in ["c", "d"]):
                self.modules["hc"].in_dict["wb_rd"] = "0"
            self.modules["hc"].in_dict["alu_status"] = self.modules["alu"].out_dict["alu_status"]

            # run calculate_combinational on all modules
            for module_name in self.modules.keys():
                self.modules[module_name].calculate_combinational()

            # get the combinational signal dict into self.comb_signals_new
            self.update_comb_signals(self.comb_signals_new)
            if (self.comb_signals == self.comb_signals_new):
                break

    # update the state (positive clock edge).
    def update_state(self):

        # WB Stage
        self.wb_instr = self.mem_instr
        self.wb_alu_out = self.mem_alu_out
        self.wb_pc = self.mem_pc

        # MEM Stage
        # implement mem stall if needed (prob not)
        self.mem_alu_out = self.modules["alu"].out_dict["out"]
        self.mem_instr = self.m1_instr
        self.mem_r2_data = self.modules["alu"].in_dict["rs2_data"]
        if (self.modules["alu"].out_dict["alu_status"] != "0" or self.m1_instr[0] == "5"):
            self.mem_instr = self.modules["alu"].ex_instr
            self.mem_r2_data = self.modules["alu"].ex_r2
        self.mem_pc = self.ex_pc

        # EX Stage
        if (self.modules["hc"].out_dict["id_ex_stall"] == "0"):
            self.m1_instr = self.id_instr
            self.ex_pc = self.id_pc
        else:
            # if there is a stall, then a nop should be inputted to alu.
            self.m1_instr = "0000"
        

        # ID Stage
        self.id_pc = self.pc

        # IF Stage

        for module_name in self.modules.keys():
            self.modules[module_name].update_state() 
        
    # update the given comb_signals dict based on the current self.modules dict.
    def update_comb_signals(self, signal_dict: dict):
        for module_name in self.modules.keys():
            module = self.modules[module_name]
            for signal_name in module.out_dict.keys():
                total_signal_name = module_name + "." + signal_name
                signal_dict[total_signal_name] = module.out_dict[signal_name]
            for signal_name in module.in_dict.keys():
                total_signal_name = module_name + "." + signal_name
                signal_dict[total_signal_name] = module.in_dict[signal_name]

    # record the state in the outfile.  pc, i_id, and gprs, then all the signals
    # in modules dict.
    def record_state(self):
        #self.outfile.write("pc " + self.pc + "\n")
        #self.outfile.write("i_id " + self.i_id + "\n")
        for i in range(16):
            self.outfile.write("gpr " + self.modules["rf"].registers[i] + "\n")

        for signal_name in self.comb_signals.keys():
            self.outfile.write(signal_name + " " + self.comb_signals[signal_name] + "\n")
        # if end of test, write that.
        if (self.eot):
            self.outfile.write("End of Test\n")    
        self.outfile.write("\n")

        # if a retirement is about to occur, record that and the instr to be retired.
        if (self.modules["rf"].in_dict["wr_en"] == "1" or self.wb_instr[0] in ["c", "d"]):
            self.outfile.write("retirement\npc= " + self.wb_pc + " instr= " + self.wb_instr + "\n")
        # if an end of test memory write is about to occur, record that.
        if (self.modules["dcache"].in_dict["wr_en"] == "1" and self.modules["dcache"].in_dict["wr_data"] == "d074" and self.modules["dcache"].in_dict["wr_dest"] == "d074"):
            self.eot_instr_in_mem = True

    def set_eot(self, value: bool):
        self.eot = value

def main():
    illusion = Illusion()
    # there needs to be end of test logic.  for now, just run 1000 cycles.
    illusion.update_state()
    while (not illusion.eot_instr_in_mem):
        illusion.calculate_combinational()
        illusion.record_state()
        illusion.update_state()
    illusion.calculate_combinational()
    illusion.record_state()
    illusion.update_state()
    illusion.calculate_combinational()
    illusion.set_eot(True)
    illusion.record_state()

if __name__ == "__main__":
    main()

        


