import sys
import os
import shutil
import cv2
import numpy as np
import numpy.typing as npt

# ----------------------------------------------------------------------------------------------
# config

output_directory = "./output"
threshold = 5
margin_size = 20
glob_perc = 0.05

# ----------------------------------------------------------------------------------------------
# functions

def get_small_frame(frame):
    """ Returns a small frame from input frame

    :param frame: the input frame
    :type frame: npt.ArrayLike
    :return: small frame
    :rtype: npt.ArryaLike
    """
    return frame[margin_size*2:-margin_size*2,margin_size*2:-margin_size*2]

def check_is_slide(frame: np.ndarray) -> bool:
    """ Check if the input frame is a slide (from margin)

    :param frame: the input frame
    :return: value true if frame is a slide
    """
    if (np.sum(frame[0:margin_size, :, 0] != 255) > 0.1 * margin_size * frame.shape[1]):
        return False
    return True

def save_frame(frame: np.ndarray, small_frame_old: np.ndarray) -> bool:
    """ Returns a boolean value saying if the frame should be saved

    :param frame: the input current frame
    :param small_frame_old: small frame computed from old frame
    :return: value true if frame should be saved
    """
    small_frame = get_small_frame(frame)
    diff = cv2.absdiff(small_frame, small_frame_old)
    difft = diff > threshold
    perc = np.sum(np.any(difft, 2)) / (difft.shape[0] * difft.shape[1])
    if (perc > glob_perc):
        return False
    return True

# ----------------------------------------------------------------------------------------------

if __name__ == "__main__":
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

        if (index % 2) == 0:
            continue

        if (index != 1) and (not check_is_slide(frame)):
            continue

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
