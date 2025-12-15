def build_header(meta: dict) -> bytes:
  text = (
      f"VBF2|RAW|{meta['aes']}|{meta['ecc']}|"
      f"{meta['size']}|{meta['sha']}|{meta['frames']}|"
      f"{meta['salt'].hex() if meta['salt'] else '00'}"
  )
  return text.encode("utf-8").ljust(4096, b'\0')

def parse_header(data: bytes) -> dict:
  text = data.decode(errors="ignore").split("|")
  return {
      "version": text[0],
      "aes": text[2] == "1",
      "ecc": text[3] == "1",
      "size": int(text[4]),
      "sha": text[5],
      "frames": int(text[6]),
      "salt": bytes.fromhex(text[7])
  }
