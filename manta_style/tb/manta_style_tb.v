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

        for (i = 0; i < 10; i = i+1) begin
            #10;
            clk = ~clk;
            #10;
            clk = ~clk;
        end
        
        release DUT.pc;

        for (i = 0; i < 1000; i = i+1) begin
            #10;
            clk = ~clk;
            #10;
            clk = ~clk;
        end
    end
endmodule