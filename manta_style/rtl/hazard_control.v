// The hazard control module.  Asserts stalls when needed.
module hazard_control(
    input [15:0]   id_instr,
    input [3:0]    ex_rd,
    input [3:0]    mem_rd,
    input [3:0]    wb_rd,
    input [1:0]    alu_status,
    input [3:0]    m1_opcode,   //TODO: i think this is unnecessary

    output reg if_id_stall,
    output reg id_ex_stall
);
    wire [3:0] id_rs1;
    wire [3:0] id_rs2;
    assign id_rs1 = (id_instr[15:12] != 4'he ? id_instr[11:8] : 4'd0);
    assign id_rs2 = (id_instr[15:12] < 4'h6 ? id_instr[7:4] : (id_instr[15:13] == 3'b110 ? id_instr[3:0] : 4'd0));
    assign rs1_hazard = (id_rs1 != 4'd0 && (id_rs1 == ex_rd || id_rs1 == mem_rd || id_rs1 == wb_rd));
    assign rs2_hazard = (id_rs2 != 4'd0 && (id_rs2 == ex_rd || id_rs2 == mem_rd || id_rs2 == wb_rd));

    always @(*) begin
        if_id_stall = 1'b0;
        id_ex_stall = 1'b0;
        if (alu_status > 2'b01 || m1_opcode == 4'h5) begin
            if_id_stall = 1'b1;
            id_ex_stall = 1'b1;
        end else if (rs1_hazard || rs2_hazard) begin
            if_id_stall = 1'b1;
            id_ex_stall = 1'b1;
        end
        if (id_instr[15:12] == 4'hd || id_instr[15:12] == 4'he ||id_instr[15:12] == 4'hf) begin
            if_id_stall = 1'b1;
        end
    end

endmodule