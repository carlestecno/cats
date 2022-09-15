import cv2
import time
from datetime import datetime
import socket

thres = 0.5
# print(cv2.__version__)

class Cam:
    cap: int
    cam_value: int

    def __init__(self, cam_number):
        self.cam_value = cam_number
        self.cap = 0
    
    def increase_cap(self):
        self.cap += 1

    @property
    def total_cap(self):
        return self.cap





def connect(img, value):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("192.168.1.40", 80))
    except:
        print("No connected reg automtic")
    if value == 0:
        print("regun", value)
        s.send("/regun".encode("utf_8"))
        s.close()
    elif value == 1:
        s.send("/regdos".encode("utf_8"))
        print("regdos", value)
        s.close()
    s.close()

def xarxa(img, thres, value):
    global num
    #global capture1
    #global capture2
    #global capture
    global camera
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    hour_time = int(time.strftime('%H%M')) #per limitar l'horari
    # print("hour-time", hour_time) 
    if len(classIds) != 0 and not 900 < hour_time < 1300 and not 1700 < hour_time < 2000 and not 650 < hour_time < 800: # per horari de reg
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            if classId in {int(17), int(18)} and num == 0:
                print("hour-time", hour_time)
                connect(img, value)
                num += 1
                if value == 1:
                    camera = True
                    # capture2 += 1
                    capture2.increase_cap()
                    capture_str = str(capture2.total_cap)
                else:
                    # capture1 += 1
                    capture1.increase_cap()
                    capture_str = str(capture1.total_cap)
                formatted_time = curr_time.strftime('%A %H.%M.%S') + " cap: " + capture_str + "  fps" + fps
                cv2.putText(img, formatted_time, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                cv2.putText(img, classNames[classId - 1], (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 255, 0), 2)
                cv2.putText(img, str(confidence), (box[0] + 150, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 255, 0), 2)
                out.write(img)
                #out1.write(img)
                cv2.imwrite(f"cat_picture/{formatted_time}.jpg", img)
                if num == 100:
                    num = 0
                    break


set2 =' tcpclientsrc host=192.168.1.46 port=8554 ! gdpdepay ! rtph264depay ! h264parse ! nvv4l2decoder  ! nvvidconv flip-method='+str(0)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(1080)+', height='+str(720)+',format=BGR ! appsink  drop=true sync=false '
set3 =' tcpclientsrc host=192.168.1.48 port=8554 ! gdpdepay ! rtph264depay ! h264parse ! nvv4l2decoder  ! nvvidconv flip-method='+str(0)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(1080)+', height='+str(720)+',format=BGR ! appsink  drop=true sync=false '
cap = cv2.VideoCapture(set2)
cap3 = cv2.VideoCapture(set3)

#cap.set(3, 1080)
#cap.set(4, 720)
#cap3.set(3, 1080)
#cap3.set(4, 720)

frame_width = 1080
frame_height = 720

frame_height1 = 500
n = datetime.now()
out = cv2.VideoWriter(f"video_cap/video_prove_{n}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 5, (frame_width, frame_height))
#out1 = cv2.VideoWriter(f"video_cap/video_prove_{n}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 5, (frame_width, frame_height1))

classNames = []
classFile = 'coco.names'

with open(classFile, 'r') as f:
    classNames = f.read().rstrip("\n").split("\n")

print("[INFO] loading model...")
configpath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = "frozen_inference_graph.pb"
net = cv2.dnn_DetectionModel(weightsPath, configpath)
# antigament (320,320)
net.setInputSize(300, 300)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
new_frame_time = 0
prev_frame_time = 0

capture1 = Cam(0)
capture2 = Cam(1)
# capture = 0
num = 0
camera = False
new_frame_time = 0
prev_frame_time = 0

while True:
    curr_time = datetime.now()

    new_frame_time = time.time()

    fps = int(1 / (new_frame_time - prev_frame_time))
    prev_frame_time = new_frame_time

    fps = str(fps)


    hour_time = time.strftime('%H%M')
    hour_time_int = int(hour_time)

    capture_str_1 = str(capture1.total_cap)
    capture_str_2 = str(capture2.total_cap) 

    formatted_time_1 = curr_time.strftime('%d/%m/%Y %A,%H:%M:%S') + " cap: " + capture_str_1 + "  fps: " + fps
    formatted_time_2 = curr_time.strftime('%d/%m/%Y %A,%H:%M:%S') + " cap: " + capture_str_2 + "  fps: " + fps

    succes, img = cap.read()
    if not succes:
        print("No camera compostador/possiblement reg automatic")

    succes1, img3 = cap3.read()
    #clone = img3[270:720,0:1080]
    if not succes1:
        print("No camera olivera")


    xarxa(img, thres, capture1.cam_value)
    xarxa(img3, thres, capture2.cam_value)
    cv2.putText(img, formatted_time_1, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(img3, formatted_time_2, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Output", img)
    cv2.imshow("Output3", img3)
    if 1 <= num < 50:
        num += 1

        if camera:
            out.write(img3)
            #out1.write(clone)
            print("camera1")
            cv2.imwrite(f"cat_picture/{formatted_time_1}.jpg", img3)
            if num == 50:
                num = 0
                camera = False
                print("num2", num)
        else:
            out.write(img)
            print("camera")
            cv2.imwrite(f"cat_picture/{formatted_time_2}.jpg", img)
            if num == 50:
                num = 0
                print("num1", num)
                 
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cap.release()
cap3.release()
cv2.destroyAllWindows()