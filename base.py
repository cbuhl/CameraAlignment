import cv2
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene
from PyQt5 import uic
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self,  fps=100):
        super(MainWindow, self).__init__()
        uic.loadUi('gui.ui', self)
        self.show()

        self.indexApos = 2
        self.indexBpos = 1

        self.set_inputs(self.indexApos, self.indexBpos)

        #I use a lambda function to pass camera specifier arguments to the sanitizer function
        self.indexA.valueChanged.connect(lambda: self.sanitize_spinbox_input('A'))
        self.indexB.valueChanged.connect(lambda: self.sanitize_spinbox_input('B'))


        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)


        self.view.setScene(scene)


        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

    def sanitize_spinbox_input(self, camera):
        def testDevice(source):
            cap = cv2.VideoCapture(source) 
            if cap is None or not cap.isOpened():
                print('Warning: unable to open video source: ', source, 'for camera', camera)
                return False
            else:
                return True

        if camera == 'A':
            #if the new value for the spinbox position is sane:
            if testDevice(self.indexA.value()):
                self.indexApos = self.indexA.value()
                self.set_inputs(self.indexApos, self.indexBpos)

        elif camera == 'B':
            #if the new value for the spinbox position is sane:
            if testDevice(self.indexA.value()):
                self.indexBpos = self.indexB.value()
                self.set_inputs(self.indexApos, self.indexBpos)


    def set_inputs(self, Apos, Bpos):
        #I need a function that is called when either of the index spinboxes are changed.
        self.captureA = cv2.VideoCapture(Apos)
        self.captureB = cv2.VideoCapture(Bpos)
        self.indexA.setValue(Apos)
        self.indexB.setValue(Bpos)

        self.dimensions = self.captureA.read()[1].shape[1::-1]

    def get_frame(self):
        _, frameA = self.captureA.read()
        _, frameB = self.captureB.read()

        #Flip input A if necessary (it is - hence the 'not statement.):
        if not self.flipA.isChecked():
            frameA = cv2.flip(frameA, 1)


        #rescale to frameA's resolution to ensure compatibility between cameras:
        #frameB = cv2.resize(frameB, frameA.shape, interpolation=cv2.INTER_NEAREST)
        frameB = cv2.resize(frameB, self.dimensions, interpolation=cv2.INTER_NEAREST)

        alpha = self.balanceSlider.value()/100
        
        #This does not work for now.
        meanFrame = cv2.addWeighted(frameA, alpha, frameB, 1.0-alpha, 0.0)


        image = QImage(meanFrame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()

    sys.exit(0)