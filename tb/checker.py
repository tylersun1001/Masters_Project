# Testbench for all systems.  Compares illusion with iss,
# compares RTL with illusion.  Will run both by default, can
# be configured to only run one or the other.

# need to run illusion main and iss first to obtain data files.
# ./signal_names.txt contains the name of the signals to compared
# between the RTL and illusion.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib", "vcd_parsealyze"))
import vcd

class Checker():

    def __init__(self, iss_filename: str="../iss/iss_states.txt", 
                        illusion_filename: str="../illusion/illusion_states.txt", 
                        manta_filename: str="./manta_states.txt", 
                        max_err_count: int = 0):
        self.iss = open(iss_filename, "r")
        self.illu = open(illusion_filename, "r")
        self.manta = open(manta_filename, "r")
        self.err_count = 0
        self.max_err_count = (2 ** 32) - 1
        if (max_err_count > 0):
            self.max_err_count = max_err_count
        self.eot = {}
        self.checked_signals = []
        self.manta_clk_count = 0
        self.manta_sim_time = 0

    def check_illu(self):
        self.eot[self.iss] = False
        self.eot[self.illu] = False
        self.strip_state(self.illu)
        while ((not self.eot[self.iss]) and (not self.eot[self.illu])): 
            iss_fp = self.iss.tell()
            iss_state = self.parse_iss_state()
            illu_state = self.parse_state(self.illu)
            if iss_state != illu_state:
                if (illu_state["instr"] == "0000"):
                    self.iss.seek(iss_fp)
                    self.eot[self.iss] = False
                    self.eot[self.illu] = False
                    continue
                abort = self.error("mismatch between illusion and iss states")
                for signal_name in iss_state:
                    if iss_state[signal_name] != illu_state[signal_name]:
                        print("iss " + signal_name + ": " + str(iss_state[signal_name]))
                        print("illusion " + signal_name + ": " + str(illu_state[signal_name]))
                print("At: instr={}, pc={}".format(iss_state["instr"], "temp"))
                if (abort):
                    exit()
            else:
                print("iss-illu: instruction retired successfully: " + iss_state["instr"])
        if (self.eot[self.iss] != self.eot[self.illu]):
            self.error("illusion and manta end of test mismatch")
            print("iss eot: " + str(self.eot[self.iss]))
            print("illusion eot: " + str(self.eot[self.illu]))
        else:
            print("Illusion matches ISS.")

    def check_manta(self):
        self.eot[self.illu] = False
        self.eot[self.manta] = False
        self.strip_state(self.illu)
        self.strip_state(self.manta)
        while ((not self.eot[self.illu]) and (not self.eot[self.manta])): 
            illu_state = self.parse_state(self.illu)
            manta_state = self.parse_state(self.manta)
            if illu_state != manta_state:
                abort = self.error("mismatch between illusion and manta states")
                for signal_name in illu_state:
                    if illu_state[signal_name] != manta_state[signal_name]:
                        print("illusion " + signal_name + ": " + str(illu_state[signal_name]))
                        print("manta " + signal_name + ": " + str(manta_state[signal_name]))
                print("At: instr={}, pc={}, clk_count={} @sim_time={}".format(illu_state["instr"], "temp", self.manta_clk_count, self.manta_sim_time))
                if (abort):
                    exit()
            else:
                print("illu-manta: instruction retired successfully: " + illu_state["instr"])
        
        if (self.eot[self.illu] != self.eot[self.manta]):
            self.error("illusion and manta end of test mismatch")
            print("illusion eot: " + str(self.eot[self.illu]))
            print("manta eot: " + str(self.eot[self.manta]))
        else:
            print("Manta matches Illusion.  Test finished at clk_count={}".format(self.manta_clk_count))

    def parse_iss_state(self) -> dict:
        data_dict = {}
        data_dict["instr"] = self.iss.readline().strip()
        self.iss.readline().strip()
        self.iss.readline().strip()
        data_dict["gpr"] = [None] * 16
        for i in range(16):
            data_dict["gpr"][i] = self.iss.readline().strip()
        store_line = self.iss.readline()
        if (store_line != "\n"):
            data_dict["store"] = store_line.strip().split()[1]
        if (self.iss.readline() == "End of Test\n"):
            self.eot[self.iss] = True
        return data_dict

    # parses the illu/manta file until the next retirement.
    # then records the state and returns as a dict.
    def parse_state(self, fp) -> dict:
        curr_line =  fp.readline()
        while (curr_line != "retirement\n"):
            curr_line =  fp.readline()
            continue
        retire_str =  fp.readline()

        data_dict = {}
        data_dict["instr"] = retire_str.strip().split()[3]
        #data_dict["pc"] = illu.readline().strip().split()[1]
        #data_dict["i_id"] = illu.readline().strip().split()[1]
        #for i in range(2):
        #     fp.readline()
        data_dict["gpr"] = [None] * 16
        for i in range(16):
            data_dict["gpr"][i] =  fp.readline().strip().split()[1]
        
        curr_line =  fp.readline()
        while (curr_line != "\n"):
            if (curr_line == "End of Test\n"):
                self.eot[fp] = True
            if (curr_line.strip().split()[0] in self.checked_signals or curr_line.strip().split()[0] == "store"):
                data_dict[curr_line.strip().split()[0]] = curr_line.strip().split()[1]
            elif (curr_line.strip().split()[0] == "clk_count"):
                self.manta_clk_count = curr_line.strip().split()[1]
            elif (curr_line.strip().split()[0] == "sim_time"):
                self.manta_sim_time = curr_line.strip().split()[1]
            curr_line =  fp.readline()

        return data_dict
    # strips manta/illusion states of leading nops (initialization phase)
    def strip_state(self, fp):
        last_pos = fp.tell()
        while (self.parse_state(fp)["instr"] == "0000"):
            last_pos = fp.tell()
            pass
        fp.seek(last_pos)

    def read_signals_to_check(self, signal_names_filename: str="./signal_names.txt"):
        signal_names_fp = open(signal_names_filename, "r")
        lines = signal_names_fp.readlines()
        for line in lines:
            signal_name = line.split()[0]
            self.checked_signals.append(signal_name)
        signal_names_fp.close()
            
    def error(self, msg: str) -> bool:
        print("ERROR: " + msg)
        self.err_count += 1
        if self.err_count >= self.max_err_count:
            return True
        return False

def main():
    checker = Checker(max_err_count=1)
    checker.check_illu()
    if (checker.err_count == 0):
        checker = Checker(max_err_count=1)
        checker.read_signals_to_check()
        checker.check_manta()

if (__name__ == "__main__"):
    main()
