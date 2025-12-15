import hashlib
from pathlib import Path
from .utils.bits import bytes_to_bits
from .utils.aes import aes_encrypt
from .utils.ecc import ecc_add
from .formats.header import build_header
from .modes.raw import bits_to_frame
from .utils.video import open_video_writer
from .config import DEFAULT_RESOLUTION, DEFAULT_FPS, ECC_STRENGTH

def encode_file(input_path, output_video, use_aes=False, password=None, use_ecc=False):
    """Codifica un archivo a video VBF2"""
    
    # Validar que existe password si se usa AES
    if use_aes and not password:
        raise ValueError("Se requiere password cuando use_aes=True")
    
    # Leer archivo original
    data = Path(input_path).read_bytes()
    salt = None
    nonce = None
    tag = None

    # Aplicar cifrado AES si se solicita
    if use_aes:
        salt, nonce, tag, encrypted = aes_encrypt(data, password)
        # Concatenar nonce + tag + ciphertext
        data = nonce + tag + encrypted

    # Aplicar corrección de errores si se solicita
    if use_ecc:
        data = ecc_add(data, strength=ECC_STRENGTH)

    # Calcular hash SHA-256 para verificación
    sha = hashlib.sha256(data).hexdigest()
    bits = bytes_to_bits(data)

    w, h = DEFAULT_RESOLUTION
    bits_per_frame = w * h

    # Calcular número de frames necesarios
    frames = (len(bits) + bits_per_frame - 1) // bits_per_frame

    # Construir header VBF2
    header_bytes = build_header({
        "aes": int(use_aes),
        "ecc": int(use_ecc),
        "size": len(data),
        "sha": sha,
        "frames": frames,
        "salt": salt
    })

    header_bits = bytes_to_bits(header_bytes)

    # Crear video writer
    out = open_video_writer(output_video, w, h, DEFAULT_FPS)
    
    try:
        # Escribir frame de header
        header_frame = bits_to_frame(header_bits, w, h)
        out.write(header_frame)

        # Escribir frames de datos
        for i in range(frames):
            chunk = bits[i*bits_per_frame:(i+1)*bits_per_frame]
            frame = bits_to_frame(chunk, w, h)
            out.write(frame)
    finally:
        # Siempre liberar recursos
        out.release()
