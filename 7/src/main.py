import cv2
import sources
from tkinter import filedialog as fd

start_x = 0
start_y = 0

filename = fd.askopenfilename()

source = sources.sourceFabric(filename)

def clickEvent(event, x, y, flags, param):
    global start_x, start_y, source, frame
    if event == cv2.EVENT_LBUTTONUP and y + source.getHeight() < frame.shape[0] and x + source.getWidth() < frame.shape[1]:
        start_x = x
        start_y = y

def changeHeight(height):
    global start_x, start_y, source, frame
    if start_y + height < frame.shape[0]:
        source.setHeight(height)

def changeWidth(width):
    global start_x, start_y, source, frame
    if start_y + width < frame.shape[1]:
        source.setWidth(width)

vid = cv2.VideoCapture(0)

frame_name = 'frame'
vid_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
vid_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))

while source.getHeight() > vid_height or source.getWidth() > vid_width:
    source.setWidth(int(source.getWidth() / 2))
    source.setHeight(int(source.getHeight() / 2))

cv2.namedWindow(frame_name)
cv2.setMouseCallback(frame_name, clickEvent)
cv2.createTrackbar('height', frame_name, source.getHeight(), vid_height, changeHeight)
cv2.createTrackbar('width', frame_name, source.getWidth(), vid_width, changeWidth)


while(True):
    ret, frame = vid.read()

    frame[start_y:start_y+source.getHeight(),start_x:start_x+source.getWidth()] = source.getImage()

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()