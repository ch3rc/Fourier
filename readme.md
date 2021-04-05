##Purpose
___
Remove periodic noise from an image. Periodic noise is best removed by filtering an image in the
frequency domain. The periodic noise may have been added by atmospheric disturbance or sensor
aberrations.
___

##How to run
___
python3 freq_filter.py [-h, --help] [-M, --manual] input_image [output_image]
___
- -h --help:      Brings up a help message
- -M --manual:    Bring up a file explorer to manually choose the image you want and return the absolute path
- -a --automatic: Automatically find the noise and remove it
- input_image:  Name of file containing image with periodic noise
- ouput_image:  name of file to save the image [default: noise_free.jpg]   
___
##Known issues
___
No Known issues at this time
___
##Notes
___
Rather than using cv.magnitude and cv.normalize before removing frequencies i opted to use
cv.cartToPolar which gave me the magnitude. I then removed the frequencies and used cv.polarToCart
to give back the real and imaginary planes. Those were merged and then the quadrants shifted back
and run through cv.idft. This gave me a much clearer image than trying to multiply the normalized
magnitude image with the real and imaginary planes and then sending those through cv.idft.
___
##links
___
- [github](www.https://github.com/ch3rc/FOURIER "github account") for code and logs under master branch
- contact me at my [UMSL email](ch3rc@umsystem.edu) if you have any questions