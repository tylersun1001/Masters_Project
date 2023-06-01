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

    def __init__(self, watch_list: list, outfile_name: str="./manta_states.txt"):
        super().__init__()
        self.outfile = open(outfile_name, "w")
        self.watch_list = watch_list
        self.eot = False

    def start(self):
        pass

    def update(self):
        #for i in range(16):
        #    gprstr = "manta_style_tb.DUT.gpr_" + str(i)
        #    self.outfile.write("gpr " + self[gprstr] + "\n")

        for signal_name in self.watch_list:
            if ("manta_style_tb.DUT.gpr_" in signal_name):
                signal_value = Converter.vlog_bin2hex(self[signal_name][1], 4)
                self.outfile.write("gpr " + signal_value + "\n")
        self.outfile.write("\n")

        if (self["manta_style_tb.DUT.id_wr_en"] == "1" 
                or Converter.vlog_bin2hex(self["manta_style_tb.DUT.wb_instr"][1], 4)[0] in ["c", "d", "e", "f"]):
            self.outfile.write("retirement\n")
            pc = Converter.vlog_bin2hex(self["manta_style_tb.DUT.pc"][1], 4)
            wb_instr = Converter.vlog_bin2hex(self["manta_style_tb.DUT.wb_instr"][1], 4)
            self.outfile.write("pc= " + pc + " instr= " + wb_instr + "\n")
        if (self.eot):
            self.outfile.write("End of Test\n")


        if (self["manta_style_tb.DUT.mem_wr_en"] == "1" 
                and Converter.vlog_bin2hex(self["manta_style_tb.DUT.mem_wr_data"][1], 4)[0] == "d074"
                and Converter.vlog_bin2hex(self["manta_style_tb.DUT.mem_wr_dest"][1], 4)[0] == "d074"):
            self.eot = True



class Parse_VCD():

    def main(self, vcd_filename: str="../manta_style/sim/sim_waveforms.vcd"):
        self.watch_list = []
        #TEMP: manually make this list.  todo: read this from a file
        for i in range(16):
            self.watch_list.append("manta_style_tb.DUT.gpr_" + str(i))
        self.watch_list.append("manta_style_tb.DUT.id_wr_en")
        self.watch_list.append("manta_style_tb.DUT.pc")
        self.watch_list.append("manta_style_tb.DUT.wb_instr")
        self.watch_list.append("manta_style_tb.DUT.mem_wr_data")
        self.watch_list.append("manta_style_tb.DUT.mem_wr_dest")
        self.watch_list.append("manta_style_tb.DUT.mem_wr_en")

        parser = vcd.VCDParser()

        tracker = IllusionTracker(self.watch_list)

        watcher = RisingClockWatcher(
            parser,
            sensitive=["manta_style_tb.DUT.clk"],
            watch=self.watch_list,
            trackers=[tracker]
        )

        with open(vcd_filename) as vcd_file:
            parser.parse(vcd_file)

if __name__ == "__main__":
    parse_vcd = Parse_VCD()
    parse_vcd.main()
