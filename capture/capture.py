import cv2
import boto
import boto.s3
import sys
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import time
import datetime


AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

bucket_name = 'hackarizonaasu'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)

bucket = conn.get_bucket(bucket_name)


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

cv2.namedWindow('your_face')
video_capture = cv2.VideoCapture(0)


while True:
    dt = datetime.datetime.now()
    #file_name = dt.strftime("%d_%m_%Y__%H_%M_%S") + '.jpg'
    file_name = "suspect.jpg"
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frameClone = frame.copy()
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    if len(faces) > 0:
        faces = sorted(faces, reverse=True,
                       key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        fx, fy, fw, fh = faces

        roi = frame[fy:fy + fh, fx:fx + fw]

        cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh),
                      (0, 0, 255), 2)


        cv2.imwrite(file_name,frameClone)

        k = Key(bucket)
        k.key = file_name
        k.set_contents_from_filename(file_name,
                                     cb=percent_cb, num_cb=10)
        time.sleep(10)


    cv2.imshow('your_face', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
