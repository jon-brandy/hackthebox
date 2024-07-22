from pwn import *
import os
from z3 import *

result = 0
target_hash = 0x03319f75
byte_array = [BitVec(f'byte index {i}', 8) for i in range(8)]

for byte in byte_array:
    extended_byte = SignExt(24, byte)
    intermediate_res = (result + extended_byte) * 0x401 # 1025
    result = intermediate_res ^ LShR(intermediate_res, 6) ^ extended_byte

# Create a Z3 solver instance
solver = Solver()

# Constraint to solver, that the calc hash must equal to targ hash.
solver.add(result == target_hash)

# if constraint is satisfiable
if solver.check() == sat:
    model = solver.model()
    log.success(f'[+] Correct hash found')
    # print result
    print(bytes(model[byte].as_long() for byte in byte_array))
