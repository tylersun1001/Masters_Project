# runs the sim and dumps the appropriate waveform
vcd file "sim_waveforms.vcd"
vcd add -r DUT/*
run -all
quit -sim