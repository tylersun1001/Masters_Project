// The instruction cache module.  Contains 2 ** 16 lines of 16 bit words.
module i_cache #(parameter testfile="../../testgen/generated_test.txt") (
    input clk,
    input [15:0] rd_dest,
    input rd_en,
    input nop,

    output reg [15:0] rd_out,
    output reg [15:0] pc_out
);
    reg [15:0] data [2**16 - 1:0];
    reg [15:0] pc;

    always @(posedge clk) begin
        if (rd_en == 1'b1) begin
            rd_out <= data[rd_dest];
            pc_out <= rd_dest;
        end
        if (nop == 1'b1) begin
            rd_out <= 16'd0;
        end
    end

    initial begin
        $readmemh(testfile, data);
    end
endmodule