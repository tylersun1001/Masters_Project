// testbench for manta_style processor. Simulates the manta style processor for the given instructions.
module manta_style_tb();
    reg clk;
    reg pc;

    manta_style DUT(
        .clk (clk)
    );

    integer i;

    initial begin
        clk = 1'b0;
        force DUT.pc = 16'd0;
        force DUT.id_instr_wire = 16'd0;
        

        for (i = 0; i < 10; i = i+1) begin
            #10;
            clk = ~clk;
            #10;
            clk = ~clk;
            if (i == 8)
                release DUT.pc;
        end
        release DUT.id_instr_wire;

        for (i = 0; i < 16; i = i+1) begin
            force DUT.rf.gpr[i] = 16'd0;
        end
        for (i = 0; i < 16; i = i+1) begin
            release DUT.rf.gpr[i];
        end

        for (i = 0; i < 1000; i = i+1) begin
            #10;
            clk = ~clk;
            #10;
            clk = ~clk;
        end
    end
endmodule