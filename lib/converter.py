# Easy methods to convert bin/hex/int

class Converter():
    
    def hex2int(hexstr: str) -> int:
        return int(hexstr, 16)

    # converts an int to a hex str with length out_len
    # if out_len is 0 (default), then use min length.
    def int2hex(integer: int, out_len: int=0) -> str:
        formatstr = '0'
        if (out_len > 0):
            formatstr += str(out_len)
        formatstr += 'x'
        return format(integer, formatstr)

    # converts a verilog (1, 0, x, z) bitstring to hex.  bin_signal_len must be provided.
    def vlog_bin2hex(vlog_bin_str: str, bin_signal_len: int) -> str:
        out_len = (bin_signal_len // 4) + int(bin_signal_len % 4 != 0)
        formatstr = '0'
        formatstr += str(out_len)
        formatstr += 'x'
        decimalvalue = 0
        for i, bit in enumerate(vlog_bin_str):
            if bit == "1":
                decimalvalue += (2 ** (len(vlog_bin_str) - (i+1)))
            if bit == "x" or bit == "z":
                return (str(i) + ":" + bit)
        return format(decimalvalue, formatstr)

