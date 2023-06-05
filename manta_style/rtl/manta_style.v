// Top level module.
module manta_style (
    input clk
);
    // IF
    reg [15:0] pc;
    
    // ID
    reg [15:0] id_instr;
    reg [15:0] id_pc;
    reg [3:0] id_rs1;
    reg [3:0] id_rs2;
    reg [3:0] id_wr;
    reg [15:0] id_wr_data;
    reg        id_wr_en;

    // EX
    reg [15:0] ex_instr;
    reg [15:0] ex_pc;
    reg [15:0] ex_fwd_r1_data;
    reg        ex_fwd_r1_en;
    reg [15:0] ex_fwd_r2_data;
    reg        ex_fwd_r2_en;
    reg [15:0] ex_rs1_data;
    reg [15:0] ex_rs2_data;
    reg [15:0] ex_alu_out;
    reg [1:0]  alu_status;
    reg [15:0] alu_ex_instr;
    reg        br_taken;
    reg [15:0] br_target;

    // MEM
    reg [15:0] mem_instr;
    reg [15:0] mem_pc;
    reg [15:0] mem_rd_dest;
    reg        mem_rd_en;
    reg [15:0] mem_wr_dest;
    reg [15:0] mem_wr_data;
    reg        mem_wr_en;
    reg  [15:0] mem_alu_out;
    reg [15:0] mem_r2_data;

    // WB
    reg [15:0] wb_instr;
    reg [15:0] wb_pc;
    reg [15:0] wb_mem_out;
    reg [15:0] wb_alu_out;

    // HC (combinational only)
    reg [3:0]    hc_ex_rd;
    reg [3:0]    hc_mem_rd;
    reg [3:0]    hc_wb_rd;
    reg [3:0]    hc_m1_opcode;
    reg        if_id_stall;
    reg        id_ex_stall;

    wire [15:0] id_instr_wire;
    wire [15:0] id_pc_wire;
    wire [15:0] ex_rs1_data_wire;
    wire [15:0] ex_rs2_data_wire;
    wire [15:0] ex_alu_out_wire;
    wire [1:0] alu_status_wire;
    wire [15:0] alu_ex_instr_wire;
    wire        br_taken_wire;
    wire [15:0] br_target_wire;
    wire [15:0] wb_mem_out_wire;
    wire [15:0] fwd_r1_data_wire;
    wire        fwd_r1_en_wire;
    wire [15:0] fwd_r2_data_wire;
    wire        fwd_r2_en_wire;
    

    hazard_control hc(
        .id_instr (id_instr),
        .ex_rd (hc_ex_rd),
        .mem_rd (hc_mem_rd),
        .wb_rd (hc_wb_rd),
        .alu_status (alu_status),
        .m1_opcode (ex_instr[15:12]),       // TODO: remove if possible
        .fwd_r1_en (fwd_r1_en_wire),
        .fwd_r2_en (fwd_r2_en_wire),
        .if_id_stall (if_id_stall_wire),
        .id_ex_stall (id_ex_stall_wire)
    );

    forward_control fc(
        .id_instr (id_instr),
        .ex_instr ((alu_status == 2'b00 && ex_instr[15:12] != 4'h5) ? ex_instr : alu_ex_instr),
        .mem_instr (mem_instr),
        .wb_dest (id_wr),
        .wb_en (id_wr_en),
        .ex_data (ex_alu_out_wire),
        .mem_data (mem_alu_out),
        .wb_data (id_wr_data),
        .fwd_r1_data (fwd_r1_data_wire),
        .fwd_r1_en (fwd_r1_en_wire),
        .fwd_r2_data (fwd_r2_data_wire),
        .fwd_r2_en (fwd_r2_en_wire)
    );

    i_cache icache(
        .clk (clk),
        .rd_dest (pc),
        .rd_en (~if_id_stall),
        .nop (if_id_stall == 1'b1 && id_ex_stall == 1'b0),
        .rd_out (id_instr_wire),
        .pc_out (id_pc_wire)
    );

    register_file rf(
        .clk (clk),
        .rd_1 (id_rs1),
        .rd_2 (id_rs2),
        .wr (id_wr),
        .wr_data (id_wr_data),
        .wr_en (id_wr_en),
        .rd_1_data (ex_rs1_data_wire),
        .rd_2_data (ex_rs2_data_wire)
    );

    alu alu(
        .clk (clk),
        .rs1_data (ex_rs1_data),
        .rs2_data (ex_rs2_data),
        .instr (ex_instr),
        .pc (ex_pc),
        .out (ex_alu_out_wire),
        .alu_status (alu_status_wire),
        .ex_instr_out (alu_ex_instr_wire),
        .br_taken (br_taken_wire),
        .br_target (br_target_wire)
    );

    d_cache dcache(
        .clk (clk),
        .rd_dest (mem_rd_dest),
        .rd_en (mem_rd_en),
        .wr_dest (mem_wr_dest),
        .wr_data (mem_wr_data),
        .wr_en (mem_wr_en),
        .rd_out (wb_mem_out_wire)
    );
    
    always @(*) begin
        if_id_stall = if_id_stall_wire;
        id_ex_stall = id_ex_stall_wire;
        id_instr = id_instr_wire;
        id_pc = id_pc_wire;
        ex_rs1_data = ex_rs1_data_wire;
        ex_rs2_data = ex_rs2_data_wire;
        ex_alu_out = ex_alu_out_wire;
        alu_status = alu_status_wire;
        alu_ex_instr = alu_ex_instr_wire;
        br_taken = br_taken_wire;
        br_target = br_target_wire;

        if (if_id_stall != 1'b1) begin
            pc = id_pc + 1;
            if (br_taken == 1'b1) begin
                pc = br_target;
            end
        end else begin
            pc = id_pc;
        end

        id_rs1 = id_instr[11:8];
        id_rs2 = (id_instr[15:12] < 4'h6 ? id_instr[7:4] : (id_instr[15:13] == 3'b110 ? id_instr[3:0] : 4'd0));

        id_wr = wb_instr[3:0];
        id_wr_data = (wb_instr[15:12] != 4'hb ? wb_alu_out : wb_mem_out_wire);
        id_wr_en = (wb_instr[15:12] != 4'hc && wb_instr[15:12] != 4'hd ? 1'b1 : 1'b0);

        if (ex_fwd_r1_en == 1'b1) begin
            ex_rs1_data = ex_fwd_r1_data;
        end
        if (ex_fwd_r2_en == 1'b1) begin
            ex_rs2_data = ex_fwd_r2_data;
        end

        mem_rd_dest = mem_alu_out;
        mem_wr_dest = mem_alu_out;
        mem_wr_data = mem_r2_data;
        mem_rd_en = 1'b0;
        mem_wr_en = 1'b0;
        if (mem_instr[15:12] == 4'hb) begin
            mem_rd_en = 1'b1;
        end else if (mem_instr[15:12] == 4'hc) begin
            mem_wr_en = 1'b1;
        end

        hc_mem_rd = (mem_instr[15:13] != 3'b110 ? mem_instr[3:0] : 4'd0);
        hc_wb_rd = (wb_instr[15:13] != 3'b110 ? wb_instr[3:0] : 4'd0);

        hc_ex_rd = (alu_ex_instr[15:13] != 3'b110 ? alu_ex_instr[3:0] : 4'd0);
        if (alu_status == 2'b00 && ex_instr[15:12] != 4'h5) begin
            hc_ex_rd = (ex_instr[15:13] != 3'b110 ? ex_instr[3:0] : 4'd0);
        end
    end

    always @(posedge clk) begin
        ex_pc <= id_pc_wire;
        if (id_ex_stall != 1'b1) begin
            ex_instr <= id_instr;
        end else begin
            ex_instr <= 4'h0;
        end
        ex_fwd_r1_data = fwd_r1_data_wire;
        ex_fwd_r1_en = fwd_r1_en_wire;
        ex_fwd_r2_data = fwd_r2_data_wire;
        ex_fwd_r2_en = fwd_r2_en_wire;

        if (alu_status == 2'b00 && ex_instr[15:12] != 4'h5) begin
            mem_instr <= ex_instr;
        end else begin
            mem_instr <= alu_ex_instr;
        end
        mem_alu_out <= ex_alu_out;
        mem_r2_data <= ex_rs2_data;
        wb_instr <= mem_instr;
        wb_alu_out <= mem_alu_out;
    end

    // DV GPR Signals
    reg [15:0] gpr_0;
    reg [15:0] gpr_1;
    reg [15:0] gpr_2;
    reg [15:0] gpr_3;
    reg [15:0] gpr_4;
    reg [15:0] gpr_5;
    reg [15:0] gpr_6;
    reg [15:0] gpr_7;
    reg [15:0] gpr_8;
    reg [15:0] gpr_9;
    reg [15:0] gpr_10;
    reg [15:0] gpr_11;
    reg [15:0] gpr_12;
    reg [15:0] gpr_13;
    reg [15:0] gpr_14;
    reg [15:0] gpr_15;

    always @(*) begin
        gpr_0 = rf.gpr[0];
        gpr_1 = rf.gpr[1];
        gpr_2 = rf.gpr[2];
        gpr_3 = rf.gpr[3];
        gpr_4 = rf.gpr[4];
        gpr_5 = rf.gpr[5];
        gpr_6 = rf.gpr[6];
        gpr_7 = rf.gpr[7];
        gpr_8 = rf.gpr[8];
        gpr_9 = rf.gpr[9];
        gpr_10 = rf.gpr[10];
        gpr_11 = rf.gpr[11];
        gpr_12 = rf.gpr[12];
        gpr_13 = rf.gpr[13];
        gpr_14 = rf.gpr[14];
        gpr_15 = rf.gpr[15];
    end

endmodule