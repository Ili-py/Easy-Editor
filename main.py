from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QApplication,QListWidget,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os

app =QApplication([])

win = QWidget()

win.setWindowTitle('Easy Editor')

btn_dir = QPushButton('Папка')

btn1 = QPushButton('Лево')
btn2 = QPushButton('Право')
btn3 = QPushButton('Зеркало')
btn4 = QPushButton('Размытие')
btn5 = QPushButton('Ч/Б')

win.resize(900,600)

label = QLabel('')

list1 = QListWidget()

QBox1 = QHBoxLayout()
QBox2 = QHBoxLayout()
QBox3 = QVBoxLayout()
QBox4 = QVBoxLayout()

QBox3.addWidget(btn_dir)
QBox3.addWidget(list1)

QBox1.addWidget(btn1)
QBox1.addWidget(btn2)
QBox1.addWidget(btn3)
QBox1.addWidget(btn4)
QBox1.addWidget(btn5)


QBox4.addWidget(label)
QBox4.addLayout(QBox1)

QBox2.addLayout(QBox3)
QBox2.addLayout(QBox4)

win.setLayout(QBox2)

workdir = 'Картинка'

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(filenames,extensions):
    m = []
    for file in filenames:
        for ext in extensions:
            if file.endswith(ext):
                m.append(file)
    return m
    
def showFilenameList():
    chooseWorkdir()
    list1.clear()
    extensions = ['.jpeg','.jpg','.png','.bmp']
    spisok = os.listdir(workdir)
    spisok2 = filter(spisok,extensions)
    for file in spisok:
        list1.addItem(file)

class ImageProcessor():
    def __init__(self):
        self.image = None 
        self.filename = None
        self.save_dir = 'modif/'
    def loadImage (self,filename):
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)
    def showImage(self,path):
        label.hide()
        pixmapimage = QPixmap(path)
        w,h = label.width(),label.height() 
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        label.setPixmap(pixmapimage)
        label.show()
    def saveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)
    def pic_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)
    def pic_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir, self.filename)
        self.showImage(image_path)
    
    
    

workimage = ImageProcessor()
def showChosenImage():
    if list1.currentRow() >= 0:
        filename =  list1.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir,workimage.filename)
        workimage.showImage(image_path)
list1.currentRowChanged.connect(showChosenImage)   

btn_dir.clicked.connect(showFilenameList)
btn1.clicked.connect(workimage.pic_left)
btn2.clicked.connect(workimage.pic_right)
btn3.clicked.connect(workimage.mirror)
btn4.clicked.connect(workimage.blur)
btn5.clicked.connect(workimage.do_bw)

win.show()

app.exec()