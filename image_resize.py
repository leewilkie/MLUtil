import os
import glob
import argparse
from PIL import Image


def resize_images(infolder, outfolder, size):
    filenames = glob.glob(infolder+'/*.jpg')
    print("Resizing {} images in '{}' to max size {}...".format(
        len(filenames), infolder, size))
    for filename in filenames:
        resize_image(filename, outfolder, size)


def resize_image(infilepath, outfolder, size):
    im = Image.open(infilepath)
    if im.size[0] > size or im.size[1] > size:
        infilefolder, infilename = os.path.split(infilepath)
        outfilepath = os.path.join(outfolder, infilename)
        #print("Resizing {} from {}".format(infilepath, im.size))
        im.thumbnail([size, size], Image.ANTIALIAS)

        if not os.path.exists(outfolder):
            print("Creating output folder...")
            os.mkdir(outfolder)

        print("Saving resized image to {}...".format(outfilepath))
        im.save(outfilepath)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-o', '--outfolder', help='Folder path for converted images.', required=True)

    parser.add_argument(
        '-s', '--size', help='Maximum size of longest dimension.', required=True, type=int)

    parser.add_argument('-i', '--infolder',
                        help='Folder containing images to be resized (default: current)')

    args = parser.parse_args()

    size = args.size

    infolder = args.infolder
    if infolder == None:
        infolder = os.getcwd()

    resize_images(infolder, args.outfolder, size)


main()
