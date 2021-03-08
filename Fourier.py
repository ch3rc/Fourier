"""
Author:     Cody Hawkins
Date:       3/7/2021
Class:      6420
Desc:       DFT and IDFT functions to help with showing
            noise frequencies in an image and pick noise
            to remove then transform to image with noise
            removed.
"""

import cv2 as cv
import numpy as np
import os


def resize(image):
    shape = (640, 480)

    try:
        image = cv.imread(image, 0)
        if image is not None:
            if image.shape != shape:
                image = cv.resize(image, shape, interpolation=cv.INTER_CUBIC)
    except cv.error as e:
        print(e)

    return image


def DFT(image):
    # get optimal DFT shape
    r, c = image.shape

    m = cv.getOptimalDFTSize(r)
    n = cv.getOptimalDFTSize(c)

    if (m % 2) != 0:
        m += 1
    if (n % 2) != 0:
        n += 1

    # make a padded border of zeros for optimal DFT performance
    padded = cv.copyMakeBorder(image, 0, m - r, 0, n - c, cv.BORDER_CONSTANT, value=0)

    # Create real and imaginary plane for DFT
    planes = [np.float32(padded), np.zeros(padded.shape, dtype=np.float32)]
    planes = cv.merge(planes)
    complex = cv.dft(planes, flags=cv.DFT_COMPLEX_OUTPUT)

    # shift the quadrants so top left point is at origin
    # |Q0|Q1|  =>  |Q3|Q2|
    # |Q2|Q3|      |Q1|Q0|
    complex = np.fft.fftshift(complex)

    # you get your magnitude calculated along with the angles changes / works better
    # than magnitude alone
    magnitude, phase = cv.cartToPolar(complex[:, :, 0], complex[:, :, 1])

    # magnitude spectrum
    spectrum = np.log(magnitude) / 30

    # sharpen the pixels on output
    magnitude = cv.pow(magnitude, 1.001)

    return magnitude, spectrum, phase


def IDFT(magnitude, phase, points, output_image, path):

    magnitude_cpy = np.copy(magnitude)

    # remove the noise from the image
    for point in points:
        magnitude_cpy = cv.circle(magnitude_cpy, point, 5, (0, 0, 0), -1)

    # get the real and imaginary planes with noise removed
    real, imaginary = cv.polarToCart(magnitude_cpy, phase)

    complex = cv.merge([real, imaginary])

    # shift the quadrants so origin is at top left
    # |Q3|Q2|  =>  |Q0|Q1|
    # |Q1|Q0|      |Q2|Q3|
    complex = np.fft.ifftshift(complex)

    # inverse DFT
    complex = cv.idft(complex)

    # get the magnitude of the image
    result = cv.magnitude(complex[:, :, 0], complex[:, :, 1])

    # normalize the result as 8 bit image
    real_image = cv.normalize(result, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)

    cv.imshow("Image with noise removed", real_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    output = os.path.join(path, output_image)
    cv.imwrite(output, real_image)