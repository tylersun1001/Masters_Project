# Compiles all verilog files, runs simulation, creates .vcd file.
vlog -work work ../tb/manta_style_tb.v ../rtl/manta_style.v ../rtl/alu.v ../rtl/multiplier3.v ../rtl/d_cache.v ../rtl/hazard_control.v ../rtl/i_cache.v ../rtl/register_file.v
vsim -do sim_script.do work.manta_style_tb