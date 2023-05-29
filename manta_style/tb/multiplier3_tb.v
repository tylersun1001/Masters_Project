/*
tb for the multiplier3 module
*/

module multiplier3_tb;
    wire [15:0] product_out;
    wire [1:0] mult_status_out;
    wire [15:0] ex_instr_out;

    reg clk;
    reg [15:0] instr_in;
    reg [15:0] A;
    reg [15:0] B;

    multiplier3 mult3(
        .clk (clk),
        .instr (instr_in),
        .A (A),
        .B (B),
        .product (product_out),
        .mult_status (mult_status_out),
        .ex_instr_out (ex_instr_out)
    );

    initial begin
        instr_in = 16'h5123;
        A = 16'd2;
        B = 16'd8;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;

        instr_in = 16'h0000;
        A = 16'd0;
        B = 16'd0;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;

        instr_in = 16'h5678;
        A = 16'd300;
        B = 16'd322;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;

        instr_in = 16'h0000;
        A = 16'd0;
        B = 16'd0;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;

        clk = 1'b0;
        #10;
        clk = 1'b1;
        #10;
    end

endmodule