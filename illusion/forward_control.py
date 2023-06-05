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

class ForwardControl(Module):

    def __init__(self):
        super().__init__()
        
        self.in_dict["id_instr"] = "0000"
        self.in_dict["ex_instr"] = "0000"
        self.in_dict["mem_instr"] = "0000"
        self.in_dict["wb_dest"] = "0"
        self.in_dict["wb_en"] = "0"
        self.in_dict["ex_data"] = "0000"    #ALU comb output
        self.in_dict["mem_data"] = "0000"   #mem stage's alu output
        self.in_dict["wb_data"] = "0000"    #should take from rf's wr_data input

        self.out_dict["fwd_r1_data"] = "0000"
        self.out_dict["fwd_r1_en"] = "0"
        self.out_dict["fwd_r2_data"] = "0000"
        self.out_dict["fwd_r2_en"] = "0"

    def calculate_combinational(self):
        id_opcode = self.in_dict["id_instr"][0]
        rs1 = "0"
        if (id_opcode != "e"):
            rs1 = self.in_dict["id_instr"][1]
        rs2 = "0"
        if (Converter.hex2int(id_opcode) < 6):
            rs2 = self.in_dict["id_instr"][2]
        elif (id_opcode == "c" or id_opcode == "d"):
            rs2 = self.in_dict["id_instr"][3]

        ex_opcode = self.in_dict["ex_instr"][0]
        ex_dest = "0"             # destination wb register of instr
        ex_rdy = "0"              # 1 bit signal, signals if ready to fwd
        if (Converter.hex2int(ex_opcode) < 12 or Converter.hex2int(ex_opcode) > 13):
            ex_dest = self.in_dict["ex_instr"][3]
        if (Converter.hex2int(ex_opcode) != 11):
            ex_rdy = "1"             # a LD instr is not ready in the ex stage.  only after mem (wb)
        mem_opcode = self.in_dict["mem_instr"][0]
        mem_dest = "0"
        mem_rdy = "0"
        if (Converter.hex2int(mem_opcode) < 12 or Converter.hex2int(mem_opcode) > 13):
            mem_dest = self.in_dict["mem_instr"][3]
        if (Converter.hex2int(mem_opcode) != 11):
            mem_rdy = "1"
        
        self.out_dict["fwd_r1_en"] = "0"
        self.out_dict["fwd_r1_data"] = "0000"
        if (rs1 != "0" and rs1 in [ex_dest, mem_dest, self.in_dict["wb_dest"]]):
            if (rs1 == self.in_dict["wb_dest"] and self.in_dict["wb_en"] == "1" and rs1 not in [ex_dest, mem_dest]):
                self.out_dict["fwd_r1_data"] = self.in_dict["wb_data"]
                self.out_dict["fwd_r1_en"] = "1"
            elif (rs1 == mem_dest and mem_rdy == "1" and rs1 != ex_dest):
                self.out_dict["fwd_r1_data"] = self.in_dict["mem_data"]
                self.out_dict["fwd_r1_en"] = "1"
            elif (rs1 == ex_dest and ex_rdy == "1"):
                self.out_dict["fwd_r1_data"] = self.in_dict["ex_data"]
                self.out_dict["fwd_r1_en"] = "1"
            
        self.out_dict["fwd_r2_en"] = "0"
        self.out_dict["fwd_r2_data"] = "0000"
        if (rs2 != "0" and rs2 in [ex_dest, mem_dest, self.in_dict["wb_dest"]]):
            if (rs2 == self.in_dict["wb_dest"] and self.in_dict["wb_en"] == "1" and rs2 not in [ex_dest, mem_dest]):
                self.out_dict["fwd_r2_data"] = self.in_dict["wb_data"]
                self.out_dict["fwd_r2_en"] = "1"
            if (rs2 == mem_dest and mem_rdy == "1" and rs2 != ex_dest):
                self.out_dict["fwd_r2_data"] = self.in_dict["mem_data"]
                self.out_dict["fwd_r2_en"] = "1"
            if (rs2 == ex_dest and ex_rdy == "1"):
                self.out_dict["fwd_r2_data"] = self.in_dict["ex_data"]
                self.out_dict["fwd_r2_en"] = "1"