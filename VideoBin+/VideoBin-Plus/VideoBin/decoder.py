import hashlib
from .utils.bits import bits_to_bytes
from .utils.aes import aes_decrypt
from .utils.ecc import ecc_remove
from .formats.header import parse_header
from .modes.raw import frame_to_bits
from .utils.video import open_video_reader
from .formats.vbf2 import HEADER_SIZE_BITS
from .config import ECC_STRENGTH

def decode_video(video_path, output_file, password=None):
    """Decodifica un video VBF2 a archivo original"""
    
    cap = open_video_reader(video_path)
    
    try:
        ok, frame = cap.read()
        if not ok:
            raise ValueError("No se pudo leer el video.")

        # Leer y parsear header
        header_bits = frame_to_bits(frame)[:HEADER_SIZE_BITS]
        header = parse_header(bits_to_bytes(header_bits))

        # Validar que se requiere password si está cifrado
        if header["aes"] and not password:
            raise ValueError("Este video está cifrado. Se requiere --password")

        data_bits = ""

        # Leer frames de datos
        for _ in range(header["frames"]):
            ok, frame = cap.read()
            if not ok:
                raise ValueError(f"Video corrupto: se esperaban {header['frames']} frames")
            data_bits += frame_to_bits(frame)

        # Truncar al tamaño exacto
        data_bits = data_bits[:header["size"] * 8]
        data = bits_to_bytes(data_bits)

        # Remover ECC si está presente
        if header["ecc"]:
            data = ecc_remove(data, strength=ECC_STRENGTH)

        # Descifrar AES si está presente
        if header["aes"]:
            salt = header["salt"]
            nonce = data[:16]
            tag = data[16:32]
            ciphertext = data[32:]
            data = aes_decrypt(salt, nonce, tag, ciphertext, password)

        # Escribir archivo de salida
        with open(output_file, "wb") as f:
            f.write(data)
            
    finally:
        # Siempre liberar recursos
        cap.release()
