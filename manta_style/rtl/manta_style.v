// Top level module.
module manta_style (
    input clk
);
    // IF
    reg [15:0] pc;
    
    // ID
    wire [15:0] id_instr;
    wire [15:0] id_pc;
    wire [3:0] id_rs1;
    wire [3:0] id_rs2;
    wire [3:0] id_wr;
    wire [15:0] id_wr_data;
    wire        id_wr_en;

    // EX
    reg [15:0] ex_instr;
    reg [15:0] ex_pc;
    wire [15:0] ex_rs1_data;
    wire [15:0] ex_rs2_data;
    wire [15:0] ex_alu_out;
    wire [1:0]  alu_status;
    wire [15:0] alu_ex_instr;

    // MEM
    reg [15:0] mem_instr;
    reg [15:0] mem_pc;
    wire [15:0] mem_rd_dest;
    wire        mem_rd_en;
    wire [15:0] mem_wr_dest;
    wire [15:0] mem_wr_data;
    wire        mem_wr_en;
    reg  [15:0] mem_alu_out;

    // WB
    reg [15:0] wb_instr;
    reg [15:0] wb_pc;
    wire [15:0] wb_mem_out;
    reg [15:0] wb_alu_out;

    // HC (combinational only)
    reg [3:0]    hc_ex_rd;
    wire [3:0]    hc_mem_rd;
    wire [3:0]    hc_wb_rd;
    wire [3:0]    hc_m1_opcode;
    wire        if_id_stall;
    wire        id_ex_stall;
    

    hazard_control hc(
        .id_instr (id_instr),
        .ex_rd (hc_ex_rd),
        .mem_rd (hc_mem_rd),
        .wb_rd (hc_wb_rd),
        .alu_status (alu_status),
        .m1_opcode (ex_instr[15:12]),       // TODO: remove if possible
        .if_id_stall (if_id_stall),
        .id_ex_stall (id_ex_stall)
    );

    i_cache icache(
        .clk (clk),
        .rd_dest (pc),
        .rd_en (~if_id_stall),
        .rd_out (id_instr),
        .pc_out (id_pc)
    );

    register_file rf(
        .clk (clk),
        .rd_1 (id_rs1),
        .rd_2 (id_rs2),
        .wr (id_wr),
        .wr_data (id_wr_data),
        .wr_en (id_wr_en),
        .rd_1_data (ex_rs1_data),
        .rd_2_data (ex_rs2_data)
    );

    alu alu(
        .clk (clk),
        .rs1_data (ex_rs1_data),
        .rs2_data (ex_rs2_data),
        .instr (ex_instr),
        .out (ex_alu_out),
        .alu_status (alu_status),
        .ex_instr_out (alu_ex_instr)
    );

    d_cache dcache(
        .clk (clk),
        .rd_dest (16'd0),
        .rd_en (1'b0),
        .wr_dest (16'd0),
        .wr_data (16'd0),
        .wr_en (1'b0),
        .rd_out (wb_mem_out)
    );

    assign id_rs1 = id_instr[11:8];
    assign id_rs2 = (id_instr[15:12] < 4'h6 ? id_instr[7:4] : (id_instr[15:13] == 3'b110 ? id_instr[3:0] : 4'd0));

    assign id_wr = wb_instr[3:0];
    assign id_wr_data = (wb_instr[15:12] != 4'hb ? wb_alu_out : wb_mem_out);
    assign id_wr_en = (wb_instr[15:12] != 4'hc && wb_instr[15:12] != 4'hd ? 1'b1 : 1'b0);
    assign hc_mem_rd = (mem_instr[15:13] != 3'b110 ? mem_instr[3:0] : 4'd0);
    assign hc_wb_rd = (wb_instr[15:13] != 3'b110 ? wb_instr[3:0] : 4'd0);
    
    always @(*) begin
        hc_ex_rd = (alu_ex_instr[15:13] != 3'b110 ? alu_ex_instr[3:0] : 4'd0);
        if (alu_status == 2'b00 && ex_instr[15:12] != 4'h5) begin
            hc_ex_rd = (ex_instr[15:13] != 3'b110 ? ex_instr[3:0] : 4'd0);
        end
    end

    always @(posedge clk) begin
        if (if_id_stall != 1'b1) begin
            pc <= pc + 1;
        end
        if (id_ex_stall != 1'b1) begin
            ex_instr <= id_instr;
        end else begin
            ex_instr <= 4'h0;
        end
        if (alu_status == 2'b00 && ex_instr[15:12] != 4'h5) begin
            mem_instr <= ex_instr;
        end else begin
            mem_instr <= alu_ex_instr;
        end
        mem_alu_out <= ex_alu_out;
        wb_instr <= mem_instr;
        wb_alu_out <= mem_alu_out;
    end

    // DV GPR Signals
    wire [15:0] gpr_0;
    wire [15:0] gpr_1;
    wire [15:0] gpr_2;
    wire [15:0] gpr_3;
    wire [15:0] gpr_4;
    wire [15:0] gpr_5;
    wire [15:0] gpr_6;
    wire [15:0] gpr_7;
    wire [15:0] gpr_8;
    wire [15:0] gpr_9;
    wire [15:0] gpr_10;
    wire [15:0] gpr_11;
    wire [15:0] gpr_12;
    wire [15:0] gpr_13;
    wire [15:0] gpr_14;
    wire [15:0] gpr_15;

    assign gpr_0 = rf.gpr[0];
    assign gpr_1 = rf.gpr[1];
    assign gpr_2 = rf.gpr[2];
    assign gpr_3 = rf.gpr[3];
    assign gpr_4 = rf.gpr[4];
    assign gpr_5 = rf.gpr[5];
    assign gpr_6 = rf.gpr[6];
    assign gpr_7 = rf.gpr[7];
    assign gpr_8 = rf.gpr[8];
    assign gpr_9 = rf.gpr[9];
    assign gpr_10 = rf.gpr[10];
    assign gpr_11 = rf.gpr[11];
    assign gpr_12 = rf.gpr[12];
    assign gpr_13 = rf.gpr[13];
    assign gpr_14 = rf.gpr[14];
    assign gpr_15 = rf.gpr[15];

endmodule