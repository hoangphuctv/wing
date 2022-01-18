import cv2
import glob
import ctypes
import sys
import os


def mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def is_image(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))


def list_all_files(dirname):
    return glob.glob(dirname + '/*')


KEY_ESC = 27
WIN_NAME = 'Image viewer'
WIN_PADDING_IMG = 100


def main(argv):
    dir = os.getcwd()

    if len(argv) > 0:
        dir = argv[0]

    # print('run dir ', dir)

    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


    all_images = []
    for file in list_all_files(dir):
        if not is_image(file):
            continue
        all_images.append(file)

    if not all_images:
        mbox('Warning', 'No file in this folder', 1)
        quit()


    key = 0
    index = 0

    screen_width = screen_width - WIN_PADDING_IMG
    screen_height = screen_height - WIN_PADDING_IMG
    # print('screen_height ', screen_height)

    while key != KEY_ESC:
        index = index + 1
        if index > len(all_images) - 1:
            index = 0
        filename = all_images[index]
        img = cv2.imread(filename, -1)

        height, width, channels = img.shape

        new_width = width
        new_height = height
        resize = False
        if screen_height < height:
            ratio = (screen_height / height)
            # print("ratio", ratio)
            height = int(height * ratio)
            width = int(width * ratio)
            resize = True

        if screen_width < width:
            ratio = (screen_width / width)
            width = int(width * ratio)
            height = int(height * ratio)
            resize = True

        if resize:
            # print("new wh", width, height)
            # print("ratio", ratio)
            new_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)
            img = new_img

        cv2.imshow(WIN_NAME, img)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        cv2.moveWindow(WIN_NAME, x, y)
        key = cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except:
        pass
