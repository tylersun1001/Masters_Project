/*
The alu.  3 stages, m1, m2, ex.  This module implements the
m1_m2 registers and m2_ex registers.
*/

module alu (
    input           clk,
    input [15:0]    rs1_data,
    input [15:0]    rs2_data,
    input [15:0]    instr,

    output reg [15:0]   out,
    output [1:0]    alu_status,
    output [15:0]   ex_instr_out
);

    reg [15:0] alu_instr;
    wire [15:0] mul_instr;
    reg [15:0] A;
    reg [15:0] B;
    reg [3:0] opcode;
    reg sel;

    wire [15:0] mul_out;
    wire [1:0] mul_status;

    multiplier3 mul(
        .clk (clk),
        .instr (mul_instr),
        .A (rs1_data),
        .B (rs2_data),
        .product (mul_out),
        .mul_status (mul_status),
        .ex_instr_out (ex_instr_out)
    );

    assign alu_status = mul_status;
    assign mul_instr = (instr[15:12] == 4'h5 ? instr : 4'd0);

    always @(*) begin
        // combinational logic
        sel = (alu_status != 2'b00 || instr[15:12] == 4'h5);
        alu_instr = instr;
        A = rs1_data;
        B = rs2_data;
        if (sel == 1'b1)  begin
            alu_instr = ex_instr_out;
        end
        opcode = alu_instr[15:12];
        // if alu_instr has an immediate, set B to the imm.
        if (opcode > 4'h5) begin
            B = alu_instr[7:4];
        end

        if (opcode == 4'h0 || opcode == 4'h6 || opcode == 4'hb || opcode == 4'hc) begin
            out = A + B;
        end else if (opcode == 4'h1) begin
            out = A - B;
        end else if (opcode == 4'h2 || opcode == 4'h7) begin
            out = A & B;
        end else if (opcode == 4'h3 || opcode == 4'h8) begin
            out = A | B;
        end else if (opcode == 4'h4) begin
            out = A ^ B;
        end else if (opcode == 4'h9) begin
            out = A << B;
        end else if (opcode == 4'ha) begin
            out = A >> B;
        end else if (opcode == 4'h5) begin
            out = mul_out;
        end else begin
            out = 16'hd074;
        end
    end

endmodule
