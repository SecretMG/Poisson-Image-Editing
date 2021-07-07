import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--folder', '-f',
    default='../imgs/mine',
    help='folder of imgs'
)
parser.add_argument(
    '--source_img', '-sos',
    default='source.jpg',
    help='directory of the source_image'
)
parser.add_argument(
    '--target_img', '-tar',
    default='target.jpg',
    help='directory of the target_image'
)
parser.add_argument(
    '--mask_img', '-mask',
    default='mask.jpg',
    help='directory of the mask_image of the source_image'
)
parser.add_argument(
    '--target_ROI', '-tROI',
    default=(0, 0),
    help='coordinate of the left_top ROI of the target_image'
)
args = parser.parse_args()