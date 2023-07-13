import cv2
import numpy as np
from tqdm import tqdm
import math


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

        # Auflösung und Anzahl der Frames definieren
        width, height = 1920, 1080
        num_frames = math.ceil(len(binary_data) / (width * height))

        # Video-Codec und -Dateiname festlegen
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # VideoWriter-Objekt erstellen
        video_writer = cv2.VideoWriter(self.destination, fourcc, 30, (width, height))
        output = tqdm(total=(width * height) * num_frames)

        bit = 0
        # Frames erstellen und zum Video hinzufügen
        for i in range(num_frames):
            # Leeren Frame erstellen
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            for row in range(height):
                for col in range(width):

                    try:

                        if binary_data[bit] == '0':
                            frame[row, col] = (255, 255, 255)  # Weiß
                        else:
                            frame[row, col] = (0, 0, 0)  # Schwarz

                        bit += 1
                        output.update()

                    except IndexError:
                        frame[row, col] = (0, 0, 0)
                        output.update()

            # Frame zum Video hinzufügen
            video_writer.write(frame)

        output.close()
        # VideoWriter-Objekt und Fenster schließen
        video_writer.release()
        cv2.destroyAllWindows()

        return

    def get_length(self):

        video_file = 'video.mp4'

        # Video-Objekt erstellen
        video = cv2.VideoCapture(video_file)

        # Zähler für schwarze und weiße Pixel initialisieren
        total_data = ''

        # Frames im Video durchlaufen
        while True:
            # Frame aus dem Video lesen
            ret, frame = video.read()

            length = None

            if length is None:
                length_counter = 0
                for width in frame:
                    for pixel in width:
                        if pixel[0] < 100:
                            total_data += '1'
                        else:
                            total_data += '0'
                        length_counter += 1

                        if length_counter == 80:
                            length = int(total_data, 2)
                            return length

    def get_binary_data(self):
        # Video-Dateiname definieren
        video_file = 'video.mp4'

        # Video-Objekt erstellen
        video = cv2.VideoCapture(video_file)

        # Zähler für schwarze und weiße Pixel initialisieren
        total_data = ''
        length = self.get_length()
        output = tqdm(total=length)
        counter = 0

        # Frames im Video durchlaufen
        while True:
            # Frame aus dem Video lesen
            ret, frame = video.read()

            # Überprüfen, ob das Video erfolgreich eingelesen wurde
            if not ret:
                break

            for width in frame:
                for pixel in width:

                    if counter >= 80:
                        if pixel[0] < 100:
                            total_data += '1'
                        else:
                            total_data += '0'

                        counter += 1
                        output.update()

                        if counter == length + 80:
                            video.release()
                            output.close()

                            return total_data
                    else:
                        counter += 1

        # Video-Objekt schließen
        video.release()
        output.close()

        with open('com2.txt', 'x') as f:
            f.write(total_data)

        return total_data

    def decode(self):
        print('decoding...')
        bin_data = self.get_binary_data()

        binary_data = self.convert_to_binary(bin_data)

        binary_file_path = 'file.zip'
        with open(binary_file_path, 'wb') as f:
            f.write(binary_data)


if __name__ == '__main__':
    video = Zip2Video('./video.mp4', 'Software Engineering.zip')
    video.encode()

    video.decode()
