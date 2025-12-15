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

    data = Path(input_path).read_bytes()
    salt = None
    nonce = None
    tag = None

    # AES
    if use_aes:
        salt, nonce, tag, data = aes_encrypt(data, password)

    # ECC
    if use_ecc:
        data = ecc_add(data, strength=ECC_STRENGTH)

    sha = hashlib.sha256(data).hexdigest()
    bits = bytes_to_bits(data)

    w, h = DEFAULT_RESOLUTION
    bits_per_frame = w * h

    # Frame count
    frames = (len(bits) + bits_per_frame - 1) // bits_per_frame

    # Build header
    header_bytes = build_header({
        "aes": int(use_aes),
        "ecc": int(use_ecc),
        "size": len(data),
        "sha": sha,
        "frames": frames,
        "salt": salt
    })

    header_bits = bytes_to_bits(header_bytes)

    # Write video
    out = open_video_writer(output_video, w, h, DEFAULT_FPS)

    # Header frame
    header_frame = bits_to_frame(header_bits, w, h)
    out.write(header_frame)

    # Data frames
    for i in range(frames):
        chunk = bits[i*bits_per_frame:(i+1)*bits_per_frame]
        frame = bits_to_frame(chunk, w, h)
        out.write(frame)

    out.release()
