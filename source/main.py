import os.path

import cv2 as cv
from utils.args import args
from PIE import PIE




def main():
    source = os.path.join(args.folder, args.source_img)
    target = os.path.join(args.folder, args.target_img)
    mask = os.path.join(args.folder, args.mask_img)
    solver = PIE(source, target, mask, args.target_ROI)
    fusion_img = solver.forward()
    cv.imshow('fusion', fusion_img)
    cv.waitKey()

if __name__ == '__main__':
    main()
