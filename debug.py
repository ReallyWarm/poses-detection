import cv2
from fps import FPS
fps = FPS()

def debug(frame, data: list):
    fps.update()
    fps.draw(frame)

    if data:
        for i, v in enumerate(data):
            i += 1
            cv2.putText(frame, f'{i}: {v}', (20, 20*i + 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 55, 200), 1)