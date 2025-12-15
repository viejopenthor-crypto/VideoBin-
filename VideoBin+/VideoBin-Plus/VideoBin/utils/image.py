import cv2
import numpy as np

def threshold_bw(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bw

def bits_from_bw(bw):
    flat = bw.flatten()
    return ''.join("1" if px > 127 else "0" for px in flat)
