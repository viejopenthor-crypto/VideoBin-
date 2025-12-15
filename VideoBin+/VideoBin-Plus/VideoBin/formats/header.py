def build_header(meta: dict) -> bytes:
    """Construye el header VBF2 con metadatos"""
    salt_hex = meta['salt'].hex() if meta['salt'] else '00'
    text = (
        f"VBF2|RAW|{meta['aes']}|{meta['ecc']}|"
        f"{meta['size']}|{meta['sha']}|{meta['frames']}|"
        f"{salt_hex}"
    )
    return text.encode("utf-8").ljust(4096, b'\0')

def parse_header(data: bytes) -> dict:
    """Parsea el header VBF2 desde bytes"""
    text = data.decode(errors="ignore").rstrip('\0').split("|")
    
    if len(text) < 8:
        raise ValueError("Header corrupto o inválido")
    
    if text[0] != "VBF2":
        raise ValueError(f"Formato inválido: se esperaba VBF2, se obtuvo {text[0]}")
    
    # Parsear salt (puede ser '00' si no hay cifrado)
    salt_hex = text[7]
    salt = bytes.fromhex(salt_hex) if salt_hex != '00' else None
    
    return {
        "version": text[0],
        "mode": text[1],
        "aes": text[2] == "1",
        "ecc": text[3] == "1",
        "size": int(text[4]),
        "sha": text[5],
        "frames": int(text[6]),
        "salt": salt
    }
