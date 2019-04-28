import argparse
import os
import glob
from imgaug import augmenters as iaa
from PIL import Image
from uuid import uuid1
import numpy as np

parser = argparse.ArgumentParser(description='Extend data set')
parser.add_argument('source', type=str, help='source folder path')
parser.add_argument('target', type=str, help='target folder path')
parser.add_argument('number', type=int, help='number of fake images per image')

seq = iaa.Sequential([
    iaa.Affine(rotate=(-180, 180))
])

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.exists(args.source):
        raise Exception('source folder "{}" does not exist'.format(args.source))
    if not os.path.exists(args.target):
        raise Exception('target folder "{}" does not exist'.format(args.target))

    for infile in glob.glob(os.path.join(args.source, "*.JPG")):
        im = Image.open(infile)
        im_array = np.asarray(im)
        images = [np.copy(im_array) for _ in range(args.number)]
        images_aug = seq.augment_images(images)
        for image in images_aug:
            pil_image = Image.fromarray(image)
            pil_image.save(os.path.join(args.target, '{name}.JPG').format(name=uuid1()), "JPEG")
