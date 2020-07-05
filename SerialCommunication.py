import serial

class SerialCommunication:

    targets = []

    def __init__(self, targets):

        self.targets = targets


    def printeaza(self):

            ser = serial.Serial('COM4', 115200)

            ser.write(self.targets)

            while True:
                if ser.in_waiting > 0:
                    ser.flush()
                    line = ser.readline().decode('utf-8').rstrip()
                    print(line)