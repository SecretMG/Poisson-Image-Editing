import cv2 as cv
import numpy as np


class drawer():
    def __init__(self, source, mask):
        source = cv.imread(source)
        for i in range(source.shape[0]):
            for j in range(source.shape[1]):
                # 防止干扰mask
                if source[i, j, 0] == 255:
                    source[i, j, 0] -= 1
        self.source = source

        self.pressed = False

        self.draw()

    def draw(self):
        cv.imshow('source', self.source)
        cv.setMouseCallback('source', self.get_mask)


    def get_mask(self, event, y, x, _, __):
        if event == 0:
            # 鼠标滑动
            if self.pressed:
                self.source[x, y] = 255
        elif event == 1:
            # 按下左键
            self.pressed = True
        elif event == 4:
            # 释放左键
            self.pressed = False
            # 绘制mask区域
            for i in range(self.source.shape[0]):
                left, right = 0, 0
                for j in range(self.source.shape[1]):
                    if self.source[i, j, 0] == 255:
                        left = j
                        break
                for j in range(self.source.shape[1]-1, -1, -1):
                    if j <= left:
                        break
                    if self.source[i, j, 0] == 255:
                        right = j
                        break
                if left and right:
                    for j in range(left, right+1):
                        self.source[i, j] = 255
            # 绘制非mask区域
            for i in range(self.source.shape[0]):
                for j in range(self.source.shape[1]):
                    if self.source[i, j, 0] != 255:
                        self.source[i, j] = 0
            # 存mask图
            cv.imwrite('mask.jpg', self.source)
        cv.imshow('source', self.source)





def main():
    dir_source = 'source.jpg'
    dir_mask = 'mask.jpg'
    solver = drawer(dir_source, dir_mask)
    cv.waitKey()

if __name__ == '__main__':
    main()
