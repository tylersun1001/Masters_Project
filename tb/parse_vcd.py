# Converts the vcd file outputted by simulation into the parsable format used
# by checker.py, similar to the file outputted by iss.
# utilizes the vcd_parseanalyze module obtained from github

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib", "vcd_parsealyze"))
import vcd
from converter import Converter

class RisingClockWatcher(vcd.VCDWatcher):
    def __init__(self, parser, **kwds):
        # Assume we start in reset, to simplify tracker notification
        super().__init__(parser, **kwds)

    def should_notify(self):
        # Called every time something in the sensitivity list changes
        # This watcher notifies trackers only on rising clock edges.
        if (
            self.get_id("manta_style_tb.DUT.clk") in self.activity
            and self.get_active_2val("manta_style_tb.DUT.clk")
        ):
            return True
        return False

class IllusionTracker(vcd.VCDTracker):

    def __init__(self, signals: dict, outfile_name: str="./manta_states.txt"):
        super().__init__()
        self.outfile = open(outfile_name, "w")
        self.signals = signals
        self.eot_instr_in_mem = False
        self.eot = False

    def start(self):
        pass

    def update(self):
        #for i in range(16):
        #    gprstr = "manta_style_tb.DUT.gpr_" + str(i)
        #    self.outfile.write("gpr " + self[gprstr] + "\n")

        for signal_name in self.signals:
            if ("manta_style_tb.DUT.gpr_" in signal_name):
                signal_value = Converter.vlog_bin2hex(self[signal_name][1], self.signals[signal_name])
                self.outfile.write("gpr " + signal_value + "\n")
        for signal_name in self.signals:
            if ("manta_style_tb.DUT.gpr_" not in signal_name):
                if (self.signals[signal_name] == 1):
                    signal_value = Converter.vlog_bin2hex(self[signal_name], self.signals[signal_name])
                else:
                    signal_value = Converter.vlog_bin2hex(self[signal_name][1], self.signals[signal_name])
                if (signal_name != "manta_style_tb.clk_count"):
                    self.outfile.write(signal_name[19:] + " " + signal_value + "\n")
                else:
                    self.outfile.write(signal_name[15:] + " " + signal_value + "\n")
                    self.outfile.write("sim_time " + self.parser.now + "\n")

        if (self.eot):
            self.outfile.write("End of Test\n")
        self.outfile.write("\n")    

        if (self["manta_style_tb.DUT.id_wr_en"] == "1" 
                or Converter.vlog_bin2hex(self["manta_style_tb.DUT.wb_instr"][1], 16)[0] in ["c", "d", "e", "f"]):
            self.outfile.write("retirement\n")
            pc = Converter.vlog_bin2hex(self["manta_style_tb.DUT.pc"][1], 16)
            wb_instr = Converter.vlog_bin2hex(self["manta_style_tb.DUT.wb_instr"][1], 16)
            self.outfile.write("pc= " + pc + " instr= " + wb_instr + "\n")

        if (self.eot_instr_in_mem):
            self.eot = True

        if (self["manta_style_tb.DUT.mem_wr_en"] == "1" 
                and Converter.vlog_bin2hex(self["manta_style_tb.DUT.mem_wr_data"][1], 16) == "d074"
                and Converter.vlog_bin2hex(self["manta_style_tb.DUT.mem_wr_dest"][1], 16) == "d074"):
            self.eot_instr_in_mem = True



class Parse_VCD():

    def main(self, vcd_filename: str="../manta_style/sim/sim_waveforms.vcd", signal_names_filename: str="./signal_names.txt"):
        self.signals = {}
        #TEMP: manually make this list.  todo: read this from a file
        for i in range(16):
            self.signals["manta_style_tb.DUT.gpr_" + str(i)] = 16
        self.signals["manta_style_tb.DUT.id_wr_en"] = 1
        self.signals["manta_style_tb.DUT.pc"] = 16
        self.signals["manta_style_tb.DUT.wb_instr"] = 16
        self.signals["manta_style_tb.DUT.mem_wr_data"] = 16
        self.signals["manta_style_tb.DUT.mem_wr_dest"] = 16
        self.signals["manta_style_tb.DUT.mem_wr_en"] = 1
        self.signals["manta_style_tb.clk_count"] = 32

        signal_names_fp = open(signal_names_filename, "r")
        lines = signal_names_fp.readlines()
        for line in lines:
            signal_name = line.split()[0]
            if (("manta_style_tb.DUT." + signal_name) not in self.signals.keys()):
                self.signals["manta_style_tb.DUT." + signal_name] = int(line.split()[1])
        signal_names_fp.close()

        parser = vcd.VCDParser()

        tracker = IllusionTracker(self.signals)

        watcher = RisingClockWatcher(
            parser,
            sensitive=["manta_style_tb.DUT.clk"],
            watch=self.signals.keys(),
            trackers=[tracker]
        )

        with open(vcd_filename) as vcd_file:
            parser.parse(vcd_file)

if __name__ == "__main__":
    parse_vcd = Parse_VCD()
    parse_vcd.main()
