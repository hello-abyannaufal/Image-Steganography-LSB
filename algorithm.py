import pathlib
import numpy as np
from PIL import Image


class ImageLSB:
    def __init__(self, filename, cipher=None):
        self.filename = filename
        self.cipher = cipher

    def encode(self):
        # Set path for stego and image
        path_stego = str(pathlib.Path().resolve()) + '/secret/Stego.png'
        path_img = 'image/'+str(self.filename)

        # Open Image
        img = Image.open(path_img, 'r')
        width, height = img.size
        arr = np.array(list(img.getdata()))

        # Check if image mode is RGB with 3 channels of RGBA with 4 channels
        if img.mode == 'RGB':
            n = 3
        if img.mode == 'RGBA':
            n = 4
        total_pixel = arr.size//n

        print('--------[Image Information]--------\n'
              'Name   :' + str(self.filename) +
              '\nWidth  : ' + str(width) +
              '\nHeight : ' + str(height) +
              '\nMode   : ' + str(img.mode) +
              '\n-----------------------------------')

        # Set limiter for extracting cipher
        self.cipher += '-UwU-'

        # Convert cipher to bits form
        bits_cipher = ''.join([format(ord(i), '08b') for i in self.cipher])

        # Check if bits of cipher fit with pixel of image
        req_pixel = len(bits_cipher)
        if req_pixel > total_pixel:
            print('Error: cipher is too large for cover')
        else:
            index = 0
            for x in range(total_pixel):
                for y in range(0, 3):
                    if index < req_pixel:
                        arr[x][y] = int(bin(arr[x][y])[2:9] + bits_cipher[index], 2)
                        index += 1

            # Transform array in row form to shape of image and convert to stego image
            arr = arr.reshape(height, width, n)
            enc_img = Image.fromarray(arr.astype('uint8'), img.mode)

            # Save stego image in folder secret
            enc_img.save(path_stego)

            print('Image encoded successfully!')

    def decode(self):
        # Open Image
        img = Image.open(self.filename, 'r')
        width, height = img.size
        arr = np.array(list(img.getdata()))

        # Check if image mode is RGB with 3 channels of RGBA with 4 channels
        if img.mode == 'RGB':
            n = 3
        if img.mode == 'RGBA':
            n = 4
        total_pixel = arr.size//n

        # Image Information
        print('--------[Image Information]--------\n'
              'Name   :' + str(self.filename) +
              '\nWidth  : ' + str(width) +
              '\nHeight : ' + str(height) +
              '\nMode   : ' + str(img.mode) +
              '\n-----------------------------------')

        # Extracting cipher from last bits of pixels
        bits_get = ''
        for x in range(total_pixel):
            for y in range(0, 3):
                bits_get += (bin(arr[x][y])[2:][-1])
        bits_get = [bits_get[i:i+8] for i in range(0, len(bits_get), 8)]

        # Processing extracted bits to message and stop extracting if get string = '--UwU--'
        message = ''
        for i in range(len(bits_get)):
            if message[-5:] == '-UwU-':
                break
            else:
                message += chr(int(bits_get[i], 2))

        if '-UwU-' in message:
            # print('Message: "' + str(message[:-5] + '"'))
            print('Found a cipher!')
            return message[:-5]
        else:
            return print('Cipher not found')