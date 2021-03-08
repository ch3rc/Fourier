"""
Author:     Cody Hawkins
Date:       3/7/2021
Class:      6420
Desc:       Enter in a input image and find the
            periodic noise frequencies and remove them.
            you can manually enter the image name and return
            a path. You can also bring up a file explorer and
            choose your image if you have forgotten your image
            name.
"""

import sys
import os
import getopt
import cv2 as cv
import numpy as np
from Fourier import resize, DFT, IDFT

ix, iy = -1, -1
copy_img = None
points = []


def file_search(image, path):
    result = []

    for root, dirs, files in os.walk(path):
        if image in files:
            result.append(os.path.join(root, image))

    if len(result) == 0:
        print("Could not find image, please check image extension")
        sys.exit(0)

    return result[0]


def click_event(event, x, y, flags, param):
    global ix, iy, copy_img, points

    if event == cv.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        copy_img = cv.circle(copy_img, (ix, iy), 5, (0, 0, 0), -1)
        points.append((ix, iy))
        cv.imshow("image", copy_img)


def help_me():
    print("\n{:->24}{}{:->24}".format("-", " HELP ", "-"))
    print("freq_filter:     Name of your executable")
    print("input_image:     Name of file containing image with periodic noise")
    print("output_image:    Name of file to save the image [default: noise_free.jpg]")
    print("-M or --manual:  Pop open a file explorer to pick your picture [helpful if you forgot image name]")
    print("{:->54}".format("-"))


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hM", ["help", "manual"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    input_image = None
    output_image = "noise_free.jpg"
    path = "C:\\Users\\codyh\\Desktop\\Test Pics"
    manual = False
    window = "image"

    for o, a in opts:
        if o in ("-h", "--help"):
            help_me()
            sys.exit(1)
        elif o in ("-M", "--manual"):
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            input_image = filedialog.askopenfilename()
            manual = True

            if len(args) == 1:
                output_image = args[0]
        else:
            assert False, "Unhandled Option!"

    if len(args) > 2 and manual is False:
        print("Too many arguments!")
        help_me()
        sys.exit(0)
    elif len(args) == 2 and manual is False:
        input_image = args[0]
        output_image = args[1]
        print(f"Input image {input_image}, output image {output_image}")
    elif len(args) == 1 and manual is False:
        input_image = args[0]
        print(f"Input image {input_image}, output image {output_image}")
    elif len(args) == 0 and manual is False:
        print("Need an input image!")
        help_me()
        sys.exit(0)

    if manual is True and len(args) > 1:
        print("Too many inputs!")
        help_me()
        sys.exit(0)
    elif manual is True and len(args) == 1:
        output_image = args[0]
        print(f"Input image {input_image}, output image {output_image}")
    elif manual is True and len(args) == 0:
        print(f"Input image {input_image}, output image {output_image}")

    global copy_img, points

    if manual is False:
        input_image = file_search(input_image, path)
        image = resize(input_image)
        magnitude, spectrum, phase = DFT(image)

        copy_img = np.copy(spectrum)
        cv.imshow(window, copy_img)
        cv.setMouseCallback(window, click_event)
        cv.waitKey(0)
        cv.destroyAllWindows()

        IDFT(magnitude, phase, points, output_image, path)

    if manual is True:
        image = resize(input_image)
        magnitude, spectrum, phase = DFT(image)

        copy_img = np.copy(spectrum)
        cv.imshow(window, copy_img)
        cv.setMouseCallback(window, click_event)
        cv.waitKey(0)
        cv.destroyAllWindows()

        IDFT(magnitude, phase, points, output_image, path)


if __name__ == "__main__":
    main()