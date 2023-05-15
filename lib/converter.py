# Easy methods to convert bin/hex/int

class Converter():
    
    def hex2int(hexstr: str) -> int:
        return int(hexstr, 16)

    # converts an int to a hex str with length out_len
    # if out_len is 0 (default), then use min length.
    def int2hex(integer: int, out_len: int=0) -> str:
        formatstr = ''
        if (out_len > 0):
            formatstr += str(out_len)
        formatstr += 'x'
        return format(int, formatstr)

