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

    def check_illu(self):
        self.strip_state(self.illu)
        counter = 0
        while (True):     #TEMP: use while true.  Change to end when iss_state has no more lines.
            print(counter)
            counter += 1
            iss_fp = self.iss.tell()
            iss_state = self.parse_iss_state()
            illu_state = self.parse_state(self.illu)
            if iss_state != illu_state:
                if (illu_state["instr"] == "0000"):
                    counter -= 1
                    self.iss.seek(iss_fp)
                    continue
                abort = self.error("mismatch between illusion and iss states")
                for signal_name in iss_state:
                    if iss_state[signal_name] != illu_state[signal_name]:
                        print("iss " + signal_name + ": " + str(iss_state[signal_name]))
                        print("illusion " + signal_name + ": " + str(illu_state[signal_name]))
                        print("counter: " + str(counter))
                print("At: instr={}, pc={}".format(iss_state["instr"], "temp"))
                if (abort):
                    exit()

    def check_manta(self):
        self.strip_state(self.illu)
        self.strip_state(self.manta)
        counter = 0
        while (True):     #TEMP: use while true.  Change to end when iss_state has no more lines.
            print(counter)
            counter += 1
            illu_state = self.parse_state(self.illu)
            manta_state = self.parse_state(self.manta)
            if illu_state != manta_state:
                abort = self.error("mismatch between illusion and manta states")
                for signal_name in illu_state:
                    if illu_state[signal_name] != manta_state[signal_name]:
                        print("illusion " + signal_name + ": " + str(illu_state[signal_name]))
                        print("manta " + signal_name + ": " + str(manta_state[signal_name]))
                        print("counter: " + str(counter))
                print("At: instr={}, pc={}".format(illu_state["instr"], "temp"))
                if (abort):
                    exit()


    def parse_iss_state(self) -> dict:
        data_dict = {}
        data_dict["instr"] = self.iss.readline().strip()
        self.iss.readline().strip()#data_dict["pc"] = iss.readline().strip()
        self.iss.readline().strip()#data_dict["i_id"] = iss.readline().strip()
        self.iss.readline()
        data_dict["gpr"] = [None] * 16
        for i in range(16):
            data_dict["gpr"][i] = self.iss.readline().strip()
        self.iss.readline()
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
        return data_dict

    # strips manta/illusion states of leading nops (initialization phase)
    def strip_state(self, fp):
        last_pos = fp.tell()
        while (self.parse_state(fp)["instr"] == "0000"):
            last_pos = fp.tell()
            pass
        fp.seek(last_pos)

            
    def error(self, msg: str) -> bool:
        print("ERROR: " + msg)
        self.err_count += 1
        if self.err_count >= self.max_err_count:
            return True
        return False

def main():
    checker = Checker(max_err_count=3)
    #checker.check_illu()
    checker.check_manta()

if (__name__ == "__main__"):
    main()