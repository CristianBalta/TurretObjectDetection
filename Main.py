import threading
from InitialiseVideoStream import InitialiseVideoStream
from SerialCommunication import SerialCommunication


def main():


    initialiseVideoStream = InitialiseVideoStream()
    #serialCommunication = SerialCommunication(8000)

    t1 = threading.Thread(target=initialiseVideoStream.stream)
   # t2 = threading.Thread(target=serialCommunication.printeaza)

    t1.start()
    #t2.start()
    t1.join()
   # t2.join()


if __name__ == '__main__':
    main()
