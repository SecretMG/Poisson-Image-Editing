import pdb
from tqdm import tqdm
from time import time

import cv2 as cv
import numpy as np
from scipy import sparse
from scipy.sparse import linalg

class PIE():
    def __init__(self, source, target, mask, tROI):
        self.source_img = cv.imread(source)
        self.target_img = cv.imread(target)
        self.mask_img = cv.imread(mask)
        self.tROI = tROI

        num_mask = 0
        for px in self.mask_img[:, :, 0].flatten():
            if self.check_mask(px):
                num_mask += 1
        self.num_mask = num_mask
        self.A = np.zeros((num_mask, num_mask))
        self.b = np.zeros((num_mask, 3))   # 3通道

        cnt = 0
        id2ord = []
        ord2id = {}
        neighbor_is_mask = []
        for i in range(1, self.mask_img.shape[0] - 1):
            for j in range(1, self.mask_img.shape[1] - 1):
                # 注意不能使用source图片的最外一圈，否则计算其散度时没有边缘像素
                if self.check_mask(self.mask_img[i, j, 0]):
                    id2ord.append((i, j))
                    ord2id[(i, j)] = cnt
                    neighbor_is_mask.append(
                        [
                            i > 0 and self.check_mask(self.mask_img[i-1, j, 0]),
                            i < self.mask_img.shape[0] - 1 and self.check_mask(self.mask_img[i+1, j, 0]),
                            j > 0 and self.check_mask(self.mask_img[i, j-1, 0]),
                            j < self.mask_img.shape[1] - 1 and self.check_mask(self.mask_img[i, j+1, 0])
                        ]   # 上、下、左、右是mask点则为True
                    )
                    cnt += 1
        self.id2ord = id2ord
        self.ord2id = ord2id
        self.neighbor_is_mask = neighbor_is_mask

        self.fusion = self.target_img

        cv.imshow('source', self.source_img)
        cv.imshow('target', self.target_img)


    def check_mask(self, px):
        return px >= 255 / 2

    def build(self):
        print('--- build A')
        for i in range(self.A.shape[0]):
            x, y = self.id2ord[i]
            self.A[i, i] = -4
            if self.neighbor_is_mask[i][0]:
                self.A[i, self.ord2id[(x-1, y)]] = 1
            if self.neighbor_is_mask[i][1]:
                self.A[i, self.ord2id[(x+1, y)]] = 1
            if self.neighbor_is_mask[i][2]:
                self.A[i, self.ord2id[(x, y-1)]] = 1
            if self.neighbor_is_mask[i][3]:
                self.A[i, self.ord2id[(x, y+1)]] = 1

        print('--- 转换成稀疏矩阵')
        pre = time()
        self.A = sparse.lil_matrix(self.A)
        print(f'spending time={int(time() - pre)}s')


        print('--- build b')
        for i in tqdm(range(self.b.shape[0])):
            for j in range(self.b.shape[1]):
                x, y = self.id2ord[i]
                self.b[i, j] = -4 * self.source_img[x, y, j] + \
                                    self.source_img[x-1, y, j] + \
                                    self.source_img[x+1, y, j] + \
                                    self.source_img[x, y-1, j] + \
                                    self.source_img[x, y+1, j]
                x, y = self.id2ord[i][0] + self.tROI[0], self.id2ord[i][1] + self.tROI[1]
                self.b[i, j] -= int(not self.neighbor_is_mask[i][0]) * self.target_img[x-1, y, j] + \
                                (not self.neighbor_is_mask[i][1]) * self.target_img[x+1, y, j] + \
                                (not self.neighbor_is_mask[i][2]) * self.target_img[x, y-1, j] + \
                                (not self.neighbor_is_mask[i][3]) * self.target_img[x, y+1, j]


    def forward(self):
        self.build()
        print('--- forward')
        Rx = linalg.cg(self.A, self.b[:, 0])[0]
        Gx = linalg.cg(self.A, self.b[:, 1])[0]
        Bx = linalg.cg(self.A, self.b[:, 2])[0]
        for i in tqdm(range(self.b.shape[0])):
            ord = (self.id2ord[i][0] + self.tROI[0], self.id2ord[i][1] + self.tROI[1])
            self.fusion[ord][0] = np.clip(Rx[i], 0, 255)
            self.fusion[ord][1] = np.clip(Gx[i], 0, 255)
            self.fusion[ord][2] = np.clip(Bx[i], 0, 255)
        return self.fusion
