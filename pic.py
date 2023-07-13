import cv2
import numpy as np
from tqdm import tqdm


class Zip2Video:

    def __init__(self, destination, zip_file):
        self.destination = destination
        self.zip_file = zip_file

    def convert_to_binary(self, bin_data):
        """Converts binary string to binary data"""

        binary_data = bytearray()
        for i in range(0, len(bin_data), 8):
            byte = bin_data[i:i + 8]
            byte_value = int(byte, 2)
            binary_data.append(byte_value)

        return binary_data

    def read_zip(self):
        """Reads zip file"""

        with open(self.zip_file, 'rb') as f:
            a = f.read()
            return ''.join(format(byte, '08b') for byte in a)

    def encode(self):

        print('encoding started...')
        binary_data = self.read_zip()

        bin_length = bin(len(binary_data))[2:].zfill(8)
        padding = ''

        for _ in range(80 - len(bin_length)):
            padding += '0'

        bin_length = padding + bin_length

        binary_data = bin_length + binary_data

        # Auflösung definieren
        width, height = 9000, 9000

        if len(binary_data) > (width * height):
            raise Exception('Datei zu groß... (' + str(len(binary_data)) + ' - ' + str(width * height) + ')')

        # Leeren Bild erstellen
        image = np.zeros((height, width, 3), dtype=np.uint8)

        output = tqdm(total=len(binary_data))
        bit = 0
        # Pixel im Bild setzen
        for row in range(height):
            for col in range(width):

                try:

                    if binary_data[bit] == '0':
                        image[row, col] = (255, 255, 255)  # Weiß
                    else:
                        image[row, col] = (0, 0, 0)  # Schwarz

                    bit += 1
                    output.update()

                except IndexError:
                    image[row, col] = (0, 0, 0)
                    output.update()

                if bit >= len(binary_data):
                    break

            if bit >= len(binary_data):
                break

        # Bild speichern
        cv2.imwrite(self.destination, image)

        print('encoding completed.')
        return

    def get_length(self):

        # Bild-Dateiname definieren
        image_file = self.destination

        # Bild einlesen
        image = cv2.imread(image_file)
        length = None
        length_counter = 0
        total_data = ''

        # Pixel im Bild durchlaufen
        for row in image:
            for pixel in row:

                if pixel[0] < 100:
                    total_data += '1'
                else:
                    total_data += '0'
                length_counter += 1

                if length_counter == 80:
                    length = int(total_data, 2)
                    print('Length: ' + str(length))
                    return length

    def get_binary_data(self):
        # Bild-Dateiname definieren
        image_file = self.destination

        # Bild einlesen
        image = cv2.imread(image_file)

        # Zähler für schwarze und weiße Pixel initialisieren
        total_data = ''
        length = self.get_length()
        output = tqdm(total=length)
        counter = 0

        # Pixel im Bild durchlaufen
        for row in image:
            for pixel in row:

                if counter >= 80:
                    if pixel[0] < 100:
                        total_data += '1'
                    else:
                        total_data += '0'

                    counter += 1
                    output.update()

                    if counter == length + 80:
                        output.close()
                        return total_data
                else:
                    counter += 1

        output.close()

        return total_data

    def decode(self):
        print('decoding...')
        bin_data = self.get_binary_data()

        binary_data = self.convert_to_binary(bin_data)

        binary_file_path = 'file.zip'
        with open(binary_file_path, 'wb') as f:
            f.write(binary_data)


if __name__ == '__main__':
    video = Zip2Video('./pic.jpg', 'Enigma.zip')
    video.encode()

    video.decode()
