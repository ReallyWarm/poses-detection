import cv2, time

class FPS:
    def __init__(self):
        self.dt = 0
        self.prvTime = 0
        self.fps = 0
        self.fps_data = []

    def update(self):
        # Current FPS
        if self.dt % 10 == 0:
            try:
                self.crnTime = time.perf_counter()
                self.fps = int(10 / (self.crnTime - self.prvTime))
                self.prvTime = self.crnTime
            except ZeroDivisionError:
                self.prvTime = time.perf_counter()
        self.dt += 1

        # FPS history data
        if len(self.fps_data) >= 10:
            self.fps_data.pop(0)
        self.fps_data.append(self.fps)

    def getFPS(self):
        return int(sum(self.fps_data) / len(self.fps_data))

    def draw(self, frame):
        cv2.putText(frame, f'FPS: {self.getFPS()}', (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (120, 120, 255), 2)
        cv2.putText(frame, f'FPS: {self.getFPS()}', (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 55, 200), 1)