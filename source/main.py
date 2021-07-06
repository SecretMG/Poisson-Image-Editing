import cv2 as cv
from utils.args import args
from PIE import PIE




def main():
    solver = PIE(args.source_img, args.target_img, args.mask_img, args.target_ROI)
    fusion_img = solver.forward()
    cv.imshow('fusion', fusion_img)
    cv.waitKey()

if __name__ == '__main__':
    main()
