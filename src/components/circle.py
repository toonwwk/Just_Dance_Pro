import cv2
import numpy as np


class Circle:
    '''
        The Circle represent the circle in the four corners of the screen waiting for arrow to intersect with it

        Args:
            x (int): x coordinate value
            y (int):  y coordinate value
            c (tuple(int)):  tuple of (blue, green, red) value of the circle
            d (int): the direction of the arrow to moving to
        Attributes:
            original_frame (cv frame): original frame to compare pixel with
            hand_intersect (boolean): is the hand is inside the circle or not
    '''
    def __init__(self, x, y, c, d):
        self.x = x
        self.y = y
        self.color = c
        self.direction = d
        self.origin_frame = None
        self.hand_intersect = False

    # compare original and new pixel and if they are diff by 5 unit then return True
    def is_pixel_change(self, origin, img):
        change = 5
        res = np.abs(origin - img)
        return res[0] > change and (res[1] > change or res[2] > change)

    def display(self, frame):
        if self.origin_frame is not None:
            if self.compare_all(frame, 20):
                return cv2.circle(frame, (self.x, self.y), 20, self.color, 2)

            return cv2.circle(frame, (self.x, self.y), 20, (255, 255, 255), 2)

    def compare_all(self, new_frame, n):
        positions = [(self.x, self.y), (self.x - n, self.y), (self.x, self.y - n), (self.x - n, self.y - n),
                     (self.x + n, self.y), (self.x, self.y + n), (self.x + n, self.y + n), (self.x + n, self.y - n),
                     (self.x - n, self.y + n)]
        result = [self.compare(new_frame, x) for x in positions]

        if result.count(True) > 7:
            self.hand_intersect = True
            return True
        else:
            self.hand_intersect = False
            return False

    def is_hand_intersect(self):
        return self.hand_intersect

    def compare(self, new_frame, position):
        dt = np.dtype(np.int16)
        origin_pixel = np.array(self.origin_frame[position[1], position[0]], dtype=dt)
        new_pixel = np.array(new_frame[position[1], position[0]], dtype=dt)
        return self.is_pixel_change(origin_pixel, new_pixel)


