import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
# from imutils.video import WebcamVideoStream
import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second

def decode(im):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    # Print results
    if decodedObjects is not None:
        for obj in decodedObjects:
            print('Type : ', obj.type)
            print('Data : ', obj.data, '\n')
            winsound.Beep(frequency, duration)

    return decodedObjects


# Display barcode and QR code location
def display(im, decodedObjects):
    # Loop over all decoded objects
    if decodedObjects is not None:
        for decodedObject in decodedObjects:
            points = decodedObject.polygon

            # If the points do not form a quad, find convex hull
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points;

            # Number of points in the convex hull
            n = len(hull)

            # Draw the convext hull
            for j in range(0, n):
                cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)


def make_1080p(capture):
    capture.set(3, 1920)
    capture.set(4, 1080)


def make_720p(capture):
    capture.set(3, 1280)
    capture.set(4, 720)


def make_480p(capture):
    capture.set(3, 640)
    capture.set(4, 480)


def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

first = True # first time to True
def set_avaliable():
    if not first:
        return
    winsound.Beep(frequency, 200)
    time.sleep(0.5)
    winsound.Beep(frequency, 200)
    # first = False


# Main
if __name__ == '__main__':


    # Read camera
    # vs = WebcamVideoStream()
    cap = cv2.VideoCapture(1)
    time.sleep(2.0)

    if cap is None:
        print("Camera wasn't initialized!")
        exit(-1)

    # cap.set(cv2.CAP_PROP_POS_MSEC, 60*1000)

    make_480p(cap)

    while True:
        # time.sleep(1000)
        ret, frame = cap.read()

        if frame is not None:
            im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if first:
                set_avaliable()
                first = False
            cv2.imshow('color frame', frame)
            cv2.imshow('gray frame', im)
            decodedObjects = decode(im)
            if decodedObjects is not None:
                display(im, decodedObjects)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
