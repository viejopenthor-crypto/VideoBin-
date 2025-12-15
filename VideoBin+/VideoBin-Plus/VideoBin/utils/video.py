import cv2

def open_video_writer(path, w, h, fps):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    return cv2.VideoWriter(path, fourcc, fps, (w, h))

def open_video_reader(path):
    return cv2.VideoCapture(path)
