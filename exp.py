import sys
import os
import shutil
import cv2
import numpy as np

# ----------------------------------------------------------------------------------------------
# config

output_directory = "./output"
threshold = 5
margin_size = 20
glob_perc = 0.05

# ----------------------------------------------------------------------------------------------
# functions

def get_small_frame(frame):
    return frame[margin_size*2:-margin_size*2,margin_size*2:-margin_size*2]

def save_frame(frame, small_frame_old):
    if (np.sum(frame[0:margin_size, :, 0] != 255) > 0.1 * margin_size * frame.shape[1]):
        return False
    small_frame = get_small_frame(frame)
    diff = cv2.absdiff(small_frame, small_frame_old)
    difft = diff > threshold
    perc = np.sum(np.any(difft, 2)) / (difft.shape[0] * difft.shape[1])
    if (perc > glob_perc):
        return False
    return True

# ----------------------------------------------------------------------------------------------
# environment
shutil.rmtree(output_directory)
os.mkdir(output_directory)

# parsing command arguments
if len(sys.argv) < 2:
    print("ERROR: no input file")
    sys.exit()
capture = cv2.VideoCapture(sys.argv[1])

# init loop
index = 0
small_frame_old = ''
saved_old = False
while (capture.isOpened()):
    index += 1
    result, frame = capture.read()
    if result == False:
        break

    if ((index % 2) == 0):
        pass

    # algorithm
    save = False
    if (index != 1):
        save = save_frame(frame, small_frame_old)

    if (save and (not save_old)):
        cv2.imwrite(output_directory + '/' + str(index) + '.jpg', frame)

    save_old = save
    small_frame_old = get_small_frame(frame)

capture.release()
cv2.destroyAllWindows()
