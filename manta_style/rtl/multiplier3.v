/*
3 stage multiplier instantiated within the alu.
*/ 
module multiplier3 (
    input           clk,
    input [15:0]    instr,
    input [15:0]    A,
    input [15:0]    B,

    output [15:0]   product,
    output [1:0]    mul_status,
    output [15:0]   ex_instr_out
);

    reg [15:0]      m2_instr;
    reg [20:0]      m2_pp [3:0];
    reg [15:0]      ex_instr;
    reg [31:0]      ex_sum;

    assign mul_status[1] = (m2_instr != 16'd0);
    assign mul_status[0] = (ex_instr != 16'd0);
    assign ex_instr_out = ex_instr;
    assign product = (ex_sum > 16'hffff ? 16'hffff : ex_sum[15:0]);

    always @(posedge clk) begin
        m2_instr <= instr;
        ex_instr <= m2_instr;

        m2_pp[3] <= (((A & {16{B[15]}}) << 3) 
                    + ((A & {16{B[14]}}) << 2)
                    + ((A & {16{B[13]}}) << 1)
                    + ((A & {16{B[12]}})));

        m2_pp[2] <= (((A & {16{B[11]}}) << 3) 
                    + ((A & {16{B[10]}}) << 2)
                    + ((A & {16{B[9]}}) << 1)
                    + ((A & {16{B[8]}})));

        m2_pp[1] <= (((A & {16{B[7]}}) << 3) 
                    + ((A & {16{B[6]}}) << 2)
                    + ((A & {16{B[5]}}) << 1)
                    + ((A & {16{B[4]}})));

        m2_pp[0] <= (((A & {16{B[3]}}) << 3) 
                    + ((A & {16{B[2]}}) << 2)
                    + ((A & {16{B[1]}}) << 1)
                    + ((A & {16{B[0]}})));

        ex_sum = (m2_pp[3] << 12) + (m2_pp[2] << 8)
                   + (m2_pp[1] << 4) + m2_pp[0];
    end



endmodule