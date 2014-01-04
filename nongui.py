import sys
import os

from utils import get_all_images, calc_similar_by_path


THRESHOLD_SIMLARITY = 0.7

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def open_image(image_name):
    cmd = os.popen('''which op xdg-open exo-open gnome-open kfmclient open | head -n1 |  sed "s/$/ '%s' \&/;
    s/kfmclient/kfmclient exec/"
    ''').read()
    if os.name == 'nt':
        cmd = 'start %s'
    print cmd % image_name
    os.popen(cmd % image_name)

if __name__ == '__main__':
    path = os.getcwd()
    if len(sys.argv) == 1:
        print 'Please input the image and directory you want to search, default directory is this folder.'
    else:
        img = sys.argv[1]
        if len(sys.argv) == 3:
            try:
                THRESHOLD_SIMLARITY = float(sys.argv[2])
                assert 0 < THRESHOLD_SIMLARITY < 1
            except AssertionError:
                print 'Similariy must be between 0 and 1.'
                exit()
            except ValueError:
                path = sys.argv[2]
        if len(sys.argv) == 4:
            path = sys.argv[2]
            THRESHOLD_SIMLARITY = sys.argv[3]
            
        images = get_all_images(path)
        similar_images = []
        for image in images:
            if calc_similar_by_path(img, image) > THRESHOLD_SIMLARITY:
                similar_images.append(image)
        if similar_images:
            print 'The similar img(s) are below:'
            for item in similar_images:
                print item
            print 'You can input "o" to open all the similar images, or imput any other key to quit'
            command = getch()
            if command == 'o':
                for item in similar_images:
                    open(item)
            else:
                exit()
        else:
            print "Can't find any similar image here!"