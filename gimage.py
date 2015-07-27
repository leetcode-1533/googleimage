import json
import os
import time
import requests
from PIL import Image, ImageQt

from StringIO import StringIO
from requests.exceptions import ConnectionError

import sys
from PyQt4 import QtGui, QtCore

import socks
import socket



def go(query):

    imagelist = []

    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + query + '&start=%d'


    start = 0  # Google's start query string parameter for pagination.
    # while start < 60: # Google will only return a max of 56 results.
    r = requests.get(BASE_URL % start)

    for image_info in json.loads(r.text)['responseData']['results']:
        url = image_info['unescapedUrl']
        try:
            image_r = requests.get(url)
        except ConnectionError, e:
            print 'could not download %s' % url
            continue

        # Remove file-system path characters from name.
        title = image_info['titleNoFormatting'].replace('/', '').replace('\\', '')
        print title

        try:
            test = Image.open(StringIO(image_r.content))
            imagelist.append(test)
        except IOError, e:
            # Throw away some gifs...blegh.
            print 'could not save %s' % url
            continue

    return imagelist



class Example(QtGui.QWidget):

    def __init__(self,urlimage):
        super(Example, self).__init__()
        self.initUI(urlimage)
        self.resize(350, 140)
        self.show()


    def initUI(self,urlimage):

        hbox = QtGui.QHBoxLayout(self)

        for item in urlimage:
            qimage = ImageQt.ImageQt(item)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            pixmap = pixmap.scaled(60,50, QtCore.Qt.KeepAspectRatio)
            lbl = QtGui.QLabel(self)
            lbl.setScaledContents(True)
            lbl.setPixmap(pixmap)
            lbl.resize(20,20)
            hbox.addWidget(lbl)
        self.setLayout(hbox)

if __name__ == "__main__":

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket

    imagelist = go('landscape')
    app = QtGui.QApplication(sys.argv)
    ex = Example(imagelist)
    sys.exit(app.exec_())
