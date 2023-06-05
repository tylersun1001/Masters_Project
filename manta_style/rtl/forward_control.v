// The forward control module.  Asserts when forwarding is possible.
module forward_control(
    input [15:0]   id_instr,
    input [15:0]   ex_instr,
    input [15:0]   mem_instr,
    input [3:0]   wb_dest,
    input          wb_en,
    input [15:0]   ex_data,
    input [15:0]   mem_data,
    input [15:0]   wb_data,

    output reg [15:0]   fwd_r1_data,
    output reg          fwd_r1_en,
    output reg [15:0]   fwd_r2_data,
    output reg          fwd_r2_en
);
    wire [3:0] id_rs1;
    wire [3:0] id_rs2;
    assign id_rs1 = (id_instr[15:12] != 4'he ? id_instr[11:8] : 4'd0);
    assign id_rs2 = (id_instr[15:12] < 4'h6 ? id_instr[7:4] : (id_instr[15:13] == 3'b110 ? id_instr[3:0] : 4'd0));

    wire [3:0] ex_dest;
    wire       ex_rdy;
    wire [3:0] mem_dest;
    wire       mem_rdy;
    assign ex_dest = (ex_instr[15:13] != 3'b110 ? ex_instr[3:0] : 4'd0);
    assign ex_rdy = (ex_instr[15:12] != 4'hb);
    assign mem_dest = (mem_instr[15:13] != 3'b110 ? mem_instr[3:0] : 4'd0);
    assign mem_rdy = (mem_instr[15:12] != 4'hb);

    always @(*) begin
        fwd_r1_en = 1'b0;
        fwd_r1_data = 4'd0;
        if (id_rs1 != 4'd0) begin
            if (id_rs1 == wb_dest && wb_en == 1'b1 && id_rs1 != mem_dest && id_rs1 != ex_dest) begin
                fwd_r1_data = wb_data;
                fwd_r1_en = 1'b1;
            end else if (id_rs1 == mem_dest && mem_rdy == 1'b1 && id_rs1 != ex_dest) begin
                fwd_r1_data = mem_data;
                fwd_r1_en = 1'b1;
            end else if (id_rs1 == ex_dest && ex_rdy == 1'b1) begin
                fwd_r1_data = ex_data;
                fwd_r1_en = 1'b1;
            end
        end
        fwd_r2_en = 1'b0;
        fwd_r2_data = 4'd0;
        if (id_rs2 != 4'd0) begin
            if (id_rs2 == wb_dest && wb_en == 1'b1 && id_rs2 != mem_dest && id_rs2 != ex_dest) begin
                fwd_r2_data = wb_data;
                fwd_r2_en = 1'b1;
            end else if (id_rs2 == mem_dest && mem_rdy == 1'b1 && id_rs2 != ex_dest) begin
                fwd_r2_data = mem_data;
                fwd_r2_en = 1'b1;
            end else if (id_rs2 == ex_dest && ex_rdy == 1'b1) begin
                fwd_r2_data = ex_data;
                fwd_r2_en = 1'b1;
            end
        end
    end

endmodule