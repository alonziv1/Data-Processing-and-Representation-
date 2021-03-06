from configparser import NoOptionError
import math
from cv2 import resize
from numpy import arange, exp
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math
import Bases

from numpy.random import default_rng


def show_images(images):

    n: int = len(images)
    f = plt.figure()
    for i in range(n):
        # Debug, plot figure
        if i == 0:
            f.add_subplot(1, n, i + 1).title.set_text(' noa haaama ')
        elif i ==1:
            f.add_subplot(1, n, i + 1).title.set_text('horrible noise appeared ')
        elif i == 2: 
            f.add_subplot(1, n, i + 1).title.set_text('activate Ziv filter ')
        else:
            f.add_subplot(1, n, i + 1).title.set_text('Image ' + str(i))
        plt.imshow(images[i])

    plt.show(block=True)


def phi(x):
    return x*math.exp(x)


def constant_f_x(x):
    return x

def vector(x_value):

    vector = arange(10)
    return vector[int(x_value)] 


def  getNoiseMatrix(frequency, mean = 1/10,  Standard_deviation  = 1/20, m = 256 , n =256):

        matrix = []

        for row in range(m):

            amplitude = default_rng().normal(loc = mean, scale = Standard_deviation)
            phase = default_rng().uniform(low = 0 , high = 2*math.pi)

            row = range(n)
            row = [amplitude * math.cos(2*math.pi*frequency* j + phase) for j in row ]

            matrix.append(row)

        # print(matrix)

        return np.array(matrix)


def myDFT(img):

    dft_matrix = Bases.Fourier(256, 0,1).matrix
    return (dft_matrix @ img.transpose()).transpose()

def myIDFT(img):

    idft_matrix = np.matrix.conjugate(Bases.Fourier(256, 0,1).matrix)
    return (idft_matrix @ img.transpose()).transpose()


class NoisyImage():

    def __init__(self):

        img = Image.open('horse.jpg').convert('L')
        img = img.resize((256,256))
        img = np.array(img) / 255
        self.original_image = img

        noise_matrix_1 = getNoiseMatrix(frequency = 1/8)
        noise_matrix_2 = getNoiseMatrix(frequency = 1/32)
        noise_matrix_3 = np.add(noise_matrix_1, noise_matrix_2) / 2

        self.noise1 = noise_matrix_1

        # show_images([Image.fromarray(np.zeros_like(noise_matrix_1)), Image.fromarray(255*noise_matrix_1),Image.fromarray(255*noise_matrix_2),Image.fromarray(255*noise_matrix_3) ])

        noisy_image_1 =  img + noise_matrix_1
        noisy_image_2 =  img + noise_matrix_2
        noisy_image_3 =  img + noise_matrix_3

        # show_images([Image.fromarray(255*img), Image.fromarray(255*noisy_image_1),Image.fromarray(255*noisy_image_2),Image.fromarray(255*noisy_image_3) ])

        self.img1 = noisy_image_1
        self.img2 = noisy_image_2
        self.img12 = noisy_image_3

def do( transform = 'auto'):
    noisy_images = NoisyImage()

    if transform == 'my':
        
        original_fft = myDFT(noisy_images.original_image)
        noisy_fft_rep = myDFT(noisy_images.img2)
        just_noise_fft = myDFT(noisy_images.noise1)

    else:

        original_fft = np.fft.fft2(noisy_images.original_image)
        noisy_fft_rep = np.fft.fft2(noisy_images.img2)
        just_noise_fft = np.fft.fft2(noisy_images.noise1)


    original_wavelet = np.sum(abs(original_fft), axis=0)
    noisy_wavelet = np.sum(abs(noisy_fft_rep), axis=0)

    for row in noisy_fft_rep:
        for col in [8,248]:
            row[col] = (row[col+1])
            # row[col] = (row[col+1] +row[col-1])/ 2
            # row[col] = 0

    reconstructed_wavelet = np.sum(abs(noisy_fft_rep), axis=0)

    plt.plot(range(256) , original_wavelet, label = 'original')
    plt.plot(range(256) , noisy_wavelet, label = 'noisy')
    plt.plot(range(256) , reconstructed_wavelet, label = 'reconstructed')


    plt.legend(loc='upper left')
    # plt.show()

    if transform == 'my':

        recon_img = myIDFT(noisy_fft_rep).real

    else :

        recon_img = np.fft.ifft2(noisy_fft_rep).real
    show_images([Image.fromarray(255*noisy_images.original_image),Image.fromarray(255*noisy_images.img2),Image.fromarray(255*recon_img)])


"""noisy_images = NoisyImage()
img = noisy_images.noise1
dft_matrix = Bases.Fourier(256, 0,1).matrix
just_noise_fft = (dft_matrix @ img.transpose()).transpose()
noise_wavelet = np.sum(abs(just_noise_fft), axis=0)
plt.plot(range(256) , noise_wavelet, label = 'noisy')
plt.show()
# image_after_dft = np.array([dft_matrix @ row for row in img])

# show_images([Image.fromarray(255*image_after_dft)])"""

do()
do('my')


