// The register file module.  Contains 16 registers with 16 bit data.
module register_file(
    input clk,
    input [3:0]    rd_1,
    input [3:0]    rd_2,
    input [3:0]    wr,
    input [15:0]    wr_data,
    input           wr_en,

    output reg [15:0] rd_1_data,
    output reg [15:0] rd_2_data
);
    reg [15:0] gpr [15:0];

    always @(posedge clk) begin
        rd_1_data <= gpr[rd_1];
        rd_2_data <= gpr[rd_2];
        
        if (wr_en == 1'b1 && wr != 4'd0) begin
            gpr[wr] <= wr_data;
        end
        gpr[4'd0] <= 16'd0;
    end
endmodule