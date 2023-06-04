// testbench for manta_style processor. Simulates the manta style processor for the given instructions.
module manta_style_tb();
    reg clk;
    reg pc;

    manta_style DUT(
        .clk (clk)
    );

    integer i;
    reg eot_signal = 1'b0;

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

        while (eot_signal == 1'b0) begin
            #10;
            clk = ~clk;
            #10;
            if (DUT.mem_wr_en == 1'b1 
                && DUT.mem_wr_dest == 16'hd074
                && DUT.mem_wr_data == 16'hd074) begin
                eot_signal = 1'b1;
            end
            clk = ~clk;
        end

        for (i = 0; i < 5; i = i+1) begin
            #10;
            clk = ~clk;
            #10;
            clk = ~clk;
        end
    end
endmodule