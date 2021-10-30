import sys
import os
import shutil
import cv2
import numpy as np

output_directory = "./output"
threshold = 5
margin_size = 20


def get_small_frame(frame):
    return frame[margin_size*2:-margin_size*2,margin_size*2:-margin_size*2]


def save_frame(frame, small_frame_old):
    if (np.sum(frame[0:margin_size, :, 0] != 255) > 0.1 * margin_size * frame.shape[1]):
        return False
    small_frame = get_small_frame(frame)
    diff = cv2.absdiff(small_frame, small_frame_old)
    difft = diff > threshold
    perc = np.sum(np.any(difft, 2)) / (difft.shape[0] * difft.shape[1])
    if (perc < 0.05):
        return False
    
    small_frame_conv = (small_frame[:-1,:-1] + small_frame[1:,:-1] + \
                        small_frame[:-1,1:] + small_frame[1:,1:]) / 4
    norm = (np.sum((small_frame_conv - small_frame_old[:-1,:-1])**2) \
            /small_frame_conv.shape[0]/small_frame_conv.shape[1]/small_frame_conv.shape[2])**0.5
    print(norm)
    return norm > 180

if len(sys.argv) < 2:
    print("ERROR: no input file")
    sys.exit()

shutil.rmtree(output_directory)
os.mkdir(output_directory)

capture = cv2.VideoCapture(sys.argv[1])
count = 0
small_frame_old = ''
perc = 0
while (capture.isOpened()):
    result, frame = capture.read()
    if result == False:
        break

    # algorithm
    save = False
    if (count != 0):
        save = save_frame(frame, small_frame_old)

    if ((count == 0) or save):
        print("save")
        cv2.imwrite(output_directory + '/' + str(count) + '.jpg', frame)
    count += 1
    print("img ", count)
    small_frame_old = get_small_frame(frame)

capture.release()
cv2.destroyAllWindows()
