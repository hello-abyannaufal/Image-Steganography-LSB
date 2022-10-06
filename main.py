from algorithm import ImageLSB

print('=============================WELCOME TO STEGANOGRAPHY LSB============================='
      '\n1. Encode Image'
      '\n2. Decode Image')

method = int(input('Select: '))

if method == 1:
    message = input(str('Input message: '))
    filename = 'Baboon.tiff'
    image = ImageLSB(filename, message)
    image.encode()

elif method == 2:
    filename = 'secret/Stego.png'
    image = ImageLSB(filename)
    cipher = image.decode()
    print('The message is: ' + '"' + str(cipher) + '"')