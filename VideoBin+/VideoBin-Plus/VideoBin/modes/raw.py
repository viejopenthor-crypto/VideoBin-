import numpy as np
import cv2

def bits_to_frame(bits, w, h):
    bits = bits.ljust(w*h, "0")
    arr = np.array([255 if b == "1" else 0 for b in bits], dtype=np.uint8)
    arr = arr.reshape((h, w))
    return cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)

def frame_to_bits(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return ''.join("1" if px > 127 else "0" for px in bw.flatten())
