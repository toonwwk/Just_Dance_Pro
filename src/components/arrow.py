import cv2
from numpy import ones, vstack
from numpy.linalg import lstsq

from .circle import Circle


class Arrow(Circle):
    def __init__(self, x, y, c, fc, s, a, d=1):
        super().__init__(x, y, c, d)
        self.speed = s
        self.final_circle = fc
        self.arrows = a
        self.origin_color = self.color
        self.white = (255, 255, 255)

        points = [(self.x, self.y), (self.final_circle.x, self.final_circle.y)]
        x_coords, y_coords = zip(*points)
        A = vstack([x_coords, ones(len(x_coords))]).T
        self.m, self.c = lstsq(A, y_coords)[0]

    def display(self, frame, score):
        self.move()

        if self.x < 10 or self.x > 1250:
            self.delete()
            return

        if self.is_intersect() and self.final_circle.is_hand_intersect():
            self.delete()
            if abs(self.x - self.final_circle.x) < self.speed and abs(self.y - self.final_circle.y) < self.speed:
                score[0] += 5
                # print('perfect')
                self.color = self.white
            else:
                score[0] += 1
                self.color = self.origin_color

        return cv2.circle(frame, (self.x, self.y), 20, self.color, -1)

    def delete(self):
        self.arrows.remove(self)

    def move(self):
        self.x += self.speed * self.final_circle.direction
        self.y = int(self.m * self.x + self.c)

    def is_intersect(self):
        dist = ((self.x - (self.final_circle.x - self.speed)) ** 2) + ((self.y - (self.final_circle.y - self.speed)) ** 2)
        rad = 80 ** 2
        return dist < rad
        # if dist == rad:
        #     return True
        # elif dist > rad:
        #     return False
        # else:
        #     return True
