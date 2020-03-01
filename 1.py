from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from segment import Ui_Form
import csv
from HHO import hho
from PIL import ImageQt
# from DHHO import dhho
# from MDHHO import mdhho

class mywindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.groupBox.setStyleSheet("background-image:url(background3.jpg)")
        self.Button_loadimage.clicked.connect(self.image_select)
        self.comboBox.activated.connect(self.choice_algorithm)
        self.Button_start.clicked.connect(self.image_display)
        self.Button_datasave.clicked.connect(self.data_save)
        self.Button_save.clicked.connect(self.image_save)
        self.Button_loadimage.clicked.connect(self.image_select())

    def choice_algorithm(self):
        algorithm = self.comboBox.currentText()
        self.iteration_times = self.lineEdit_maxinte.text()
        self.population_number = self.lineEdit_popnumber.text()
        # print(type(light_intensity))
        if str(algorithm) == 'HHO-3DPCNN':
            self.flage=0
        elif str(algorithm) == 'DHHO-3DPCNN':
            self.flage=1
        elif str(algorithm) == 'MDHHO-3DPCNN':
            self.flage=2

    def image_select(self):
        self.filename = QFileDialog.getOpenFileName(self,'选择图像','','JPG files(*.jpg ,)')
        # print(self.filename)
        if self.filename==('',''):
            QMessageBox.warning(self,"未选择图像","您未选择图像！")
        else:
            self.textEdit_load.setPlainText(str(self.filename[0]))

    def start(self):
        if self.flage==0:
            self.h = hho(str(self.filename[0]), self.iteration_times, self.population_number)
        elif self.flage==1:
            self.h = dhho(str(self.filename[0]), self.iteration_times, self.population_number)
        elif self.flage==1:
            self.h = mdhho(str(self.filename[0]), self.iteration_times, self.population_number)

    def image_display(self):
         pixmap1 = QtGui.QPixmap(self.filename[0])
         self.label_origimage.setPixmap(pixmap1)
         self.label_origimage.setScaledContents(True)  # 原始图像自适应label大小
         pixmap2 = QtGui.QPixmap(self.h[0])
         self.label_segmentimage.setPixmap(pixmap2)
         self.label_segmentimage.setScaledContents(True) # 原始图像自适应label大小

    def data(self):
        self.lcdNumber.display(self.h[1])
        self.lineEdit_lianjeiqiangdu.setText(self.h[2])
        self.lineEdit_shuaijianxishu.setText(self.h[3])
        self.lineEdit_yuzhifangda.setText(self.h[4])

    def evaluation(self):
        self.lineEdit_psnr.setText(self.h[5])
        self.lineEdit_mse.setText(self.h[6])
        self.lineEdit_ssim.setText(self.h[7])
        self.lineEdit_fsim.setText(self.h[8])

    def data_save(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
        self.textEdit_datasave.setPlainText(str(path[0]))
        with open(path[0], 'a', newline='') as stream:
            writer = csv.writer(stream)
            for line in self.table1:
                writer.writerow(line)

    def image_save(self):
        image = ImageQt.fromqpixmap(self.label_segmentimage.pixmap())
        path = QFileDialog.getSaveFileName(self, '保存图像', '','JPG files(*.jpg)')
        self.textEdit_save.setPlainText(str(path[0]))
        image.save(str(path[0]))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
