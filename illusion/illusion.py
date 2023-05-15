# The top level illusion module.

import Module
import Converter
import sys
sys.path.insert(0, '../lib')

class Illusion(Module):

    def __init__(self):
        self.modules = {}
        self.modules["icache"] = ICache()
        self.modules["rf"] = RegisterFile()
        self.modules["alu"] = ALU()
        self.modules["dcache"] = DCache()
        
        self.comb_signals = {}
        update_comb_signals(self.comb_signals)
        
        self.comb_signals_new = self.comb_signals.copy()

    # while there is no difference between the two comb_signals dicts, run
    # calculate_combinational on all submodules
    def calculate_combinational(self):
        
    # update the state (positive clock edge).
    def update_state(self):

    # update the given comb_signals dict based on the current self.modules dict.
    def update_comb_signals(self, signal_dict: dict):
        for module_name in self.modules.keys():
            module = self.modules[module_name]
            for signal_name in module.out_dict.keys():
                total_signal_name = module_name + "." + signal_name
                signal_dict[total_signal_name] = module[signal_name]


