import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import QUrl
from pyqtgraph import PlotWidget, plot
import numpy as np
import scipy.fftpack
import librosa

#导入designer工具生成的login模块
from ui.dspCfg import Ui_Dspcfg
from deal.dsp_cfg_Packet import dsp_cfg_Packet
from deal.dsp_cfg_rbl import MyPacket
from deal.dsp_cfg_creat import hex_to_bin_file
from deal.cfg import creat_cfg, read_json_from_file, write_json_to_file

class MyMainForm(QMainWindow, Ui_Dspcfg):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #添加登录按钮信号和槽
        self.btn_datPath.clicked.connect(self.select_datPath)
        self.btn_generatPath.clicked.connect(self.select_generat)
        self.btn_all.clicked.connect(self.generat_all)
        self.btn_SaveCfg.clicked.connect(self.save_cfg)
        self.btn_OpenCfg.clicked.connect(self.open_cfg)
    def select_datPath(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select dat Path")
        self.lineEdit_datPath.setText(file_path)        
    def select_generat(self):
        file_path = QFileDialog.getExistingDirectory(self, "Select generat")
        self.lineEdit_generatPath.setText(file_path)        
    def save_cfg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select json")
        cfg_json = creat_cfg(self.lineEdit_datPath.text(),
                  self.lineEdit_generatPath.text(), self.lineEdit_outName.text(), 
                  self.lineEdit_type.text(), self.lineEdit_algo.text(), self.lineEdit_algo2.text(),
                  self.lineEdit_part.text(), self.lineEdit_fwVer.text(), self.lineEdit_productCode.text())
        write_json_to_file(file_path, cfg_json)
    def open_cfg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select json")
        cfg_json = read_json_from_file(file_path)
        if cfg_json["name"] == "dspCfg":
            self.lineEdit_datPath.setText(cfg_json["Source"]["datPath"])
            self.lineEdit_generatPath.setText(cfg_json["Source"]["generatPath"])
            self.lineEdit_outName.setText(cfg_json["generatName"])
            self.lineEdit_type.setText(cfg_json["RBL"]["type"])
            self.lineEdit_algo.setText(cfg_json["RBL"]["algo"])
            self.lineEdit_algo2.setText(cfg_json["RBL"]["algo2"])
            self.lineEdit_part.setText(cfg_json["RBL"]["part"])
            self.lineEdit_fwVer.setText(cfg_json["RBL"]["fw_version"])
            self.lineEdit_productCode.setText(cfg_json["RBL"]["product_code"])
        else:
            print("Json Key Not match")        
    def generat_all(self):
        # 合并文件
        hex_to_bin_file(self.lineEdit_datPath.text(), self.lineEdit_generatPath.text(), self.lineEdit_outName.text(), self.lineEdit_type.text(), self.lineEdit_algo.text(), self.lineEdit_algo2.text(),
                      self.lineEdit_part.text(), self.lineEdit_fwVer.text(), self.lineEdit_productCode.text())
        print("dsp_cfg creat finished! ok")

if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
