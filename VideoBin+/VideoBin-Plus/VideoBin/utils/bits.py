def bytes_to_bits(data: bytes) -> str:
  return ''.join(f'{b:08b}' for b in data)

def bits_to_bytes(bits: str) -> bytes:
  return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
