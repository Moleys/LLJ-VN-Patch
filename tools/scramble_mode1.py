# -*- coding: utf-8 -*-
"""scramble_mode1.py — re-scramble 1 file text ve dinh dang \xfe\xfe + mode + \xfe\xff (mode 1)"""
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
inp, out = sys.argv[1], sys.argv[2]
mode = int(sys.argv[3]) if len(sys.argv) > 3 else 1

text = open(inp, encoding='utf-8-sig').read()
utf16 = text.encode('utf-16-le')
data = bytearray(utf16)

if mode == 1:
    # ScrambleMode1: swap adjacent bits (0xAAAA>>1 | 0x5555<<1)
    for i in range(0, len(data), 2):
        c = data[i] | (data[i+1] << 8)
        c = ((c & 0xAAAA) >> 1) | ((c & 0x5555) << 1)
        data[i] = c & 0xFF
        data[i+1] = (c >> 8) & 0xFF
elif mode == 0:
    for i in range(0, len(data), 2):
        if data[i+1] == 0 and data[i] < 0x20:
            continue
        data[i] ^= 1
        data[i+1] ^= (data[i] & 0xFE)
else:
    raise SystemExit('unsupported mode')

head = b'\xfe\xfe' + bytes([mode]) + b'\xff\xfe'
res = head + bytes(data)
open(out, 'wb').write(res)
print('wrote', out, len(res), 'bytes (mode', mode, ') head', res[:4])
