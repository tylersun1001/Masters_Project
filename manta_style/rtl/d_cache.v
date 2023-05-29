// The data cache module.  Contains 2 ** 16 lines of 16 bit words.
module d_cache (
    input clk,
    input [15:0]    rd_dest,
    input           rd_en,
    input [15:0]    wr_dest,
    input [15:0]    wr_data,
    input           wr_en,

    output reg [15:0] rd_out
);
    reg [15:0] data [2**16 - 1:0];

    always @(posedge clk) begin
        if (rd_en == 1'b1) begin
            rd_out <= data[rd_dest];
        end
        if (wr_en == 1'b1) begin
            data[wr_dest] <= wr_data;
        end
    end

    initial begin
        $readmemh("../rtl/dcache_init.mem", data);
    end
endmodule