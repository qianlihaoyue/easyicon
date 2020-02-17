#简单加了一个UI
#代码来自于 https://blog.csdn.net/jia666666/article/details/81875126  &&  https://blog.csdn.net/MemoryD/article/details/83147300
#感谢博主 jia666666 && MemoryD
#双击即可关闭


import sys,os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal

from memory_pic import *
from base64 import b64decode

import easyicon

def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(b64decode(pic_code))
    image.close()

class ShapeWidget(QWidget):
    def __init__(self,parent=None):
        super(ShapeWidget, self).__init__(parent)
        self.mypix()

        self.mythread = MyThread()  # 实例化自己建立的任务线程类
        self.mythread.start()  # 启动任务线程

    #显示不规则图片
    def mypix(self):
        self.update()
        get_pic(panda_png,'panda.png')  ############
        self.mypic ='panda.png'
        self.pix=QPixmap(self.mypic,'0',Qt.AvoidDither|Qt.ThresholdAlphaDither|Qt.ThresholdDither)
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())
        self.dragPosition=None

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=QMouseEvent.globalPos()-self.pos()
            QMouseEvent.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def paintEvent(self, QPaintEvent):
        painter=QPainter(self)
        painter.drawPixmap(0,0,self.pix.width(),self.pix.height(),self.pix)

    def mouseDoubleClickEvent(self, QMouseEvent): #双击关闭
        os.remove('panda.png')
        sys.exit(app.exec_())

class MyThread(QThread): # 建立一个任务线程类
    def __init__(self):
        super(MyThread, self).__init__()
    def run(self): # 在启动线程后任务从这个函数里面开始执行
        easyicon.main()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=ShapeWidget()
    form.show()
    sys.exit(app.exec_())
