import base64
import zlib
import marshal
import os
import sys

def xor_encrypt(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def encrypt_file(source, output):
    with open(source, "r", encoding="utf-8") as f:
        code = f.read()
    
    # LAYER 1: Compile
    bytecode = compile(code, "<enc>", "exec")
    
    # LAYER 2: Marshal
    marshaled = marshal.dumps(bytecode)
    
    # LAYER 3: Compress
    compressed = zlib.compress(marshaled, 9)
    
    # LAYER 4: XOR with random key
    key = os.urandom(32)
    encrypted = xor_encrypt(compressed, key)
    
    # LAYER 5: Base64
    b64 = base64.b64encode(encrypted).decode("utf-8")
    key_b64 = base64.b64encode(key).decode("utf-8")
    
    # Split b64 jadi chunks
    chunk_size = 80
    chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]
    b64_joined = '    "' + '"\n    "'.join(chunks) + '"'
    
    wrapper = f'''# -*- coding: utf-8 -*-
# 🔥 SPAM-WA TERMUX EDITION
# Developer: @SetyaFlv
# Powered By Setya
# DO NOT EDIT - AUTO GENERATED

import base64, zlib, marshal, sys

_K = base64.b64decode("{key_b64}")

_D = (
{b64_joined}
)

def _x(d, k):
    return bytes([d[i] ^ k[i % len(k)] for i in range(len(d))])

def _run():
    try:
        data = base64.b64decode(_D)
        dec = _x(data, _K)
        uncompressed = zlib.decompress(dec)
        bytecode = marshal.loads(uncompressed)
        exec(bytecode, {{"__name__": "__main__"}})
    except KeyboardInterrupt:
        print("\\n\\n  ⚠️  Keluar dari program...\\n")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    _run()
'''
    
    with open(output, "w", encoding="utf-8") as f:
        f.write(wrapper)
    
    print(f"✅ Encrypted: {output}")
    print(f"📦 Original: {len(code)} bytes")
    print(f"🔒 Encrypted: {len(wrapper)} bytes")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encrypt.py <source.py> [output.py]")
        sys.exit(1)
    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "enc_" + source
    encrypt_file(source, output)
