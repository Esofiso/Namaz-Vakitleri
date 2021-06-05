import datetime
import json
import locale


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, Qt

locale.setlocale(locale.LC_ALL, '')

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(642, 237)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        Form.setFont(font)
        Form.setWindowOpacity(1.0)
        Form.setStyleSheet("background:qconicalgradient(cx:0, cy:0, angle:135, stop:0.0738636 rgba(171, 200, 135, 255), stop:0.409091 rgba(3, 81, 117, 250), stop:0.551136 rgba(67, 118, 178, 255), stop:0.568182 rgba(0, 0, 0, 0), stop:0.579545 rgba(0, 49, 99, 208), stop:1 rgba(0, 55, 153, 69))")
        Form.setWindowIcon(QtGui.QIcon('cami_ikonu.png'))
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lab_namaz_vakitleri = QtWidgets.QLabel(Form)
        self.lab_namaz_vakitleri.setStyleSheet("font: 30pt \"Pristina\";\n"
"")
        self.lab_namaz_vakitleri.setObjectName("lab_namaz_vakitleri")
        self.horizontalLayout_2.addWidget(self.lab_namaz_vakitleri)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(1)
        self.line_2.setMidLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.lab_tarih = QtWidgets.QLabel(Form)
        self.lab_tarih.setStyleSheet("font: 20pt \"Times New Roman\";")
        self.lab_tarih.setObjectName("lab_tarih")
        self.horizontalLayout_2.addWidget(self.lab_tarih)
        self.verticalLayout_13.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_13.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.imsak = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.imsak.setFont(font)
        self.imsak.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
        self.imsak.setObjectName("imsak")
        self.verticalLayout_6.addWidget(self.imsak)
        self.imsak_vakti = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.imsak_vakti.setFont(font)
        self.imsak_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))\n"
"")
        self.imsak_vakti.setObjectName("imsak_vakti")
        self.verticalLayout_6.addWidget(self.imsak_vakti)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(1)
        self.line_3.setMidLineWidth(2)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sabah = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.sabah.setFont(font)
        self.sabah.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
        self.sabah.setObjectName("sabah")
        self.verticalLayout.addWidget(self.sabah)
        self.sabah_vakti = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.sabah_vakti.setFont(font)
        self.sabah_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
        self.sabah_vakti.setObjectName("sabah_vakti")
        self.verticalLayout.addWidget(self.sabah_vakti)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line_5 = QtWidgets.QFrame(Form)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_5.setLineWidth(1)
        self.line_5.setMidLineWidth(2)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout.addWidget(self.line_5)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ogle = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.ogle.setFont(font)
        self.ogle.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
        self.ogle.setObjectName("ogle")
        self.verticalLayout_5.addWidget(self.ogle)
        self.ogle_vakti = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.ogle_vakti.setFont(font)
        self.ogle_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
        self.ogle_vakti.setObjectName("ogle_vakti")
        self.verticalLayout_5.addWidget(self.ogle_vakti)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(1)
        self.line_4.setMidLineWidth(2)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ikindi = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.ikindi.setFont(font)
        self.ikindi.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        self.ikindi.setObjectName("ikindi")
        self.verticalLayout_4.addWidget(self.ikindi)
        self.ikindi_vakti = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.ikindi_vakti.setFont(font)
        self.ikindi_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        self.ikindi_vakti.setObjectName("ikindi_vakti")
        self.verticalLayout_4.addWidget(self.ikindi_vakti)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.line_6 = QtWidgets.QFrame(Form)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_6.setLineWidth(1)
        self.line_6.setMidLineWidth(2)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout.addWidget(self.line_6)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.aksam = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.aksam.setFont(font)
        self.aksam.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
        self.aksam.setObjectName("aksam")
        self.verticalLayout_3.addWidget(self.aksam)
        self.aksam_vakti = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.aksam_vakti.setFont(font)
        self.aksam_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
        self.aksam_vakti.setObjectName("aksam_vakti")
        self.verticalLayout_3.addWidget(self.aksam_vakti)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.line_7 = QtWidgets.QFrame(Form)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_7.setLineWidth(1)
        self.line_7.setMidLineWidth(2)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout.addWidget(self.line_7)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.yatsi = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.yatsi.setFont(font)
        self.yatsi.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
        self.yatsi.setObjectName("yatsi")
        self.verticalLayout_2.addWidget(self.yatsi)
        self.yatsi_vakti = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans Light")
        font.setPointSize(16)
        self.yatsi_vakti.setFont(font)
        self.yatsi_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
        self.yatsi_vakti.setObjectName("yatsi_vakti")
        self.verticalLayout_2.addWidget(self.yatsi_vakti)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_13.addLayout(self.horizontalLayout)
        self.verticalLayout_7.addLayout(self.verticalLayout_13)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lab_vaktin_cikmasina = QtWidgets.QLabel(Form)
        self.lab_vaktin_cikmasina.setStyleSheet("font: 22pt \"Times New Roman\";\n"
"background:qradialgradient(spread:pad, cx:0.494, cy:0.505682, radius:0.5, fx:0.5, fy:0.517, stop:0 rgba(255, 188, 188, 0), stop:1 rgba(255, 255, 255, 0))")
        self.lab_vaktin_cikmasina.setObjectName("lab_vaktin_cikmasina")
        self.horizontalLayout_3.addWidget(self.lab_vaktin_cikmasina)
        self.kac_dakka_var = QtWidgets.QTimeEdit(Form)
        self.kac_dakka_var.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setPointSize(35)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.kac_dakka_var.setFont(font)
        self.kac_dakka_var.setStyleSheet("font: 35pt \"Lucida Sans\";\n"
"background:qradialgradient(spread:pad, cx:0.494, cy:0.505682, radius:0.5, fx:0.5, fy:0.517, stop:0 rgba(255, 188, 188, 0), stop:1 rgba(255, 255, 255, 0))")
        self.kac_dakka_var.setFrame(False)
        self.kac_dakka_var.setReadOnly(True)
        self.kac_dakka_var.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.kac_dakka_var.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.kac_dakka_var.setCalendarPopup(True)
        self.kac_dakka_var.setObjectName("kac_dakka_var")
        self.horizontalLayout_3.addWidget(self.kac_dakka_var)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        an = datetime.datetime.now()
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Namaz Vakitleri"))
        self.kac_dakka_var.setDisplayFormat(_translate("Form", "HH:mm:ss"))
        self.lab_vaktin_cikmasina.setText(_translate("Form", "     Vaktin Çıkmasına:"))
        self.lab_namaz_vakitleri.setText(_translate("Form", "<html><head/><body><p>Namaz Vakitleri</p></body></html>"))
        self.lab_tarih.setText(_translate("Form", f"<html><head/><body><p align=\"center\">{tarih_ne(self, '%d %B %A')}</p></body></html>"))
        self.imsak.setText(_translate("Form", "İmsak"))
        self.sabah.setText(_translate("Form", "Sabah"))
        self.ogle.setText(_translate("Form", "Öğle"))
        self.ikindi.setText(_translate("Form", "İkindi"))
        self.aksam.setText(_translate("Form", "Akşam"))
        self.yatsi.setText(_translate("Form", "Yatsı"))
        sozluk = vakitleri_getir()
        gunlu = sozluk[f"{an.day}"]
        self.imsak_vakti.setText(_translate("Form", f'{gunlu["ims"][0]}.{gunlu["ims"][1]}'))
        self.sabah_vakti.setText(_translate("Form", f'{gunlu["sab"][0]}.{gunlu["sab"][1]}'))
        self.ogle_vakti.setText(_translate("Form", f'{gunlu["ogl"][0]}.{gunlu["ogl"][1]}'))
        self.ikindi_vakti.setText(_translate("Form", f'{gunlu["iki"][0]}.{gunlu["iki"][1]}'))
        self.aksam_vakti.setText(_translate("Form", f'{gunlu["aks"][0]}.{gunlu["aks"][1]}'))
        self.yatsi_vakti.setText(_translate("Form", f'{gunlu["yat"][0]}.{gunlu["yat"][1]}'))


def vakitler():
    """
    <<Çorumun 1 aylık namaz vakitlerini elde etmeye çalışıyoruz>>
    Started on Sat Apr 24 18:36:41 2021
    @Author: ESAD
    """
    import calendar
    import itertools as it
    import json
    import re
    from collections import namedtuple
    from datetime import datetime as dt
    from urllib.request import urlopen

    from bs4 import BeautifulSoup

    sehirler = ["corum"]

    bes_vakit = ("ims", "sab", "ogl", "iki", "aks", "yat")

    Saat = namedtuple("Saat", ["hour", "minute"], defaults=["00", "00"])

    # number of days in the current month
    num_days = calendar.monthrange(dt.now().year, dt.now().month)[1]

    # bugün ayın kaçı?
    today = dt.now().day

    vakit_dict = dict.fromkeys(bes_vakit, None)
    days_dict = dict.fromkeys(range(1, num_days + 1), vakit_dict)
    cities_dict = dict.fromkeys(sehirler, days_dict)

    # WARNING: sehirler slice-by-slice process edilebilir hata verirse
    # (e.g. 25 vilayet at a time)
    for sehir in sehirler:
        site = f"https://www.haberturk.com/namaz-vakitleri/{sehir}"
        html_source = urlopen(site)

        soup = BeautifulSoup(html_source, 'html.parser')

        imsakiye_table = soup.find(id="imsakiye-table")

        # skipping \n, thead and \n
        imsakiye_body = imsakiye_table.contents[3]
        imsakiye_contents = (
                            "".join(str(ibc).split("\n"))
                            for ibc in imsakiye_body.children
                            if ibc != "\n"
                            )
        vakitler = [(Saat(*vakit)
                    for vakit in re.findall(r">\s*(\d{2}):(\d{2})\s*</",
                                            content)[:])
                    for content in imsakiye_contents]

        sehir_aylik = cities_dict[sehir]

        # if wanted from today, make it <today-1>
        starting_day = 0
        for day in it.islice(sehir_aylik, starting_day, num_days):
            sehir_aylik[day] = dict(zip(bes_vakit, vakitler[day-1]))

        with open(f"corum.txt", mode="w") as f:
            f.write(json.dumps(sehir_aylik, indent=4))

        print(f"{sehir} processed.")


    with open("en_son_ne_zaman_calisti.txt", "w") as file:
        file.write(dt.now().strftime("%Y\n%m"))

def en_son_ne_zaman_calisti():
    an = datetime.datetime.now()
    with open("en_son_ne_zaman_calisti.txt", "r") as file:
        yıl, ay = file.readlines()

    yıl = int(yıl.strip())
    ay = int(ay)

    if ay != an.month or yıl != an.year:
        vakitler()
    
def vakitleri_getir():
    with open("corum.txt", "r") as file:
        vakitler = json.load(file)
    return vakitler

def tarih_ne(self, istek):
        an = datetime.datetime.now()
        return datetime.datetime.strftime(an, istek)

gunler = []
for gun in vakitleri_getir():
    gunler.append(int(gun))

def kac_dakka_var():
    global time, simdiki_vakit

    _translate = QtCore.QCoreApplication.translate
    an = datetime.datetime.now()

    ui.imsak.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
    ui.imsak_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
    ui.sabah.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
    ui.sabah_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
    ui.ogle.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
    ui.ogle_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
    ui.ikindi.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
    ui.ikindi_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
    ui.aksam.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
    ui.aksam_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")
    ui.yatsi.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255))")
    ui.yatsi_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255))")

    ui.imsak.setText(_translate("Form", "İmsak"))
    ui.sabah.setText(_translate("Form", "Sabah"))
    ui.ogle.setText(_translate("Form", "Öğle"))
    ui.ikindi.setText(_translate("Form", "İkindi"))
    ui.aksam.setText(_translate("Form", "Akşam"))
    ui.yatsi.setText(_translate("Form", "Yatsı"))

    ay     = an.month
    gun    = an.day
    saat   = an.hour
    dakika = an.minute
    saniye = an.second

    if gunler[0] == gun:
        en_son_ne_zaman_calisti()

    sozluk = vakitleri_getir()
    gunlu = sozluk[f"{an.day}"]

    ui.imsak_vakti.setText(_translate("Form", f'{gunlu["ims"][0]}.{gunlu["ims"][1]}'))
    ui.sabah_vakti.setText(_translate("Form", f'{gunlu["sab"][0]}.{gunlu["sab"][1]}'))
    ui.ogle_vakti.setText(_translate("Form", f'{gunlu["ogl"][0]}.{gunlu["ogl"][1]}'))
    ui.ikindi_vakti.setText(_translate("Form", f'{gunlu["iki"][0]}.{gunlu["iki"][1]}'))
    ui.aksam_vakti.setText(_translate("Form", f'{gunlu["aks"][0]}.{gunlu["aks"][1]}'))
    ui.yatsi_vakti.setText(_translate("Form", f'{gunlu["yat"][0]}.{gunlu["yat"][1]}'))
    
    toplam = saat*3600 + dakika*60 + saniye
    saat24 = 24*3600

    ui.lab_tarih.setText(_translate("Form", f"<html><head/><body><p align=\"center\">{tarih_ne(ui, '%d %B %A')}</p></body></html>"))

    ims = int(gunlu["ims"][0])*3600 + int(gunlu["ims"][1])*60
    sab = int(gunlu["sab"][0])*3600 + int(gunlu["sab"][1])*60
    ogl = int(gunlu["ogl"][0])*3600 + int(gunlu["ogl"][1])*60
    iki = int(gunlu["iki"][0])*3600 + int(gunlu["iki"][1])*60
    aks = int(gunlu["aks"][0])*3600 + int(gunlu["aks"][1])*60
    yat = int(gunlu["yat"][0])*3600 + int(gunlu["yat"][1])*60

    if toplam < ims:
        ui.imsak.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.imsak_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        kalan = ims - toplam
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", "<html><head/><body><p align=\"right\">İmsak'ın Çıkmasına:  </p></body></html>"))
        simdiki_vakit = "İmsak'a"

    elif toplam < sab:
        ui.imsak.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.imsak_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        kalan = sab - toplam
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", "<html><head/><body><p align=\"right\">İmsak'ın Çıkmasına:  </p></body></html>"))
        simdiki_vakit = "İmsak'a"

    elif toplam < ogl:
        ui.sabah.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.sabah_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        ui.imsak.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        kalan = ogl - toplam
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", "<html><head/><body><p align=\"right\">Öğle Ezanı'na:  </p></body></html>"))
        simdiki_vakit = "Ezan'a"

    elif toplam < iki:
        ui.ogle.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.ogle_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        ui.sabah.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.sabah_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        kalan = iki - toplam
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", "<html><head/><body><p align=\"right\">Öğle'nin Çıkmasına:  </p></body></html>"))
        simdiki_vakit = "Öğle'ye"

    elif toplam < aks:
        ui.ikindi.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.ikindi_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        ui.ogle.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ogle_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.sabah.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.sabah_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        kalan = aks - toplam
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", "<html><head/><body><p align=\"right\">İkindi'nin Çıkmasına:  </p></body></html>"))
        simdiki_vakit = "İkindi'ye"

    elif toplam < yat:
        ui.aksam.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.aksam_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        ui.ikindi.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ikindi_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ogle.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ogle_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.sabah.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.sabah_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        kalan = yat - toplam
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", "<html><head/><body><p align=\"right\">Akşam'ın Çıkmasına:  </p></body></html>"))
        simdiki_vakit = "Akşam'a"
    
    elif toplam > yat and int(gunler[-1]) == gun:
        ui.yatsi.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.yatsi_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        ui.aksam.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.aksam_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ikindi.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ikindi_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ogle.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.ogle_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.sabah.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.sabah_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak.setStyleSheet("background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        ui.imsak_vakti.setStyleSheet("background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))")
        kalan = saat24 - toplam
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", f"<html><head/><body><p align=\"right\">{tarih_ne(ui, '%B')} Ayı'nın Sonuna:  </p></body></html>"))
        simdiki_vakit = "Yeni Ay'a"

    elif toplam >= yat:
        ui.imsak.setText(_translate("Form",  "Yatsı"))
        ui.sabah.setText(_translate("Form",  "İmsak"))
        ui.ogle.setText(_translate("Form",   "Sabah"))
        ui.ikindi.setText(_translate("Form", "Öğle"))
        ui.aksam.setText(_translate("Form",  "İkindi"))
        ui.yatsi.setText(_translate("Form",  "Akşam"))

        ui.imsak_vakti.setText(_translate("Form", f'{gunlu["yat"][0]}.{gunlu["yat"][1]}'))
        gunlu = sozluk[f"{an.day+1}"]
        ui.sabah_vakti.setText(_translate("Form", f'{gunlu["ims"][0]}.{gunlu["ims"][1]}'))
        ui.ogle_vakti.setText(_translate("Form", f'{gunlu["sab"][0]}.{gunlu["sab"][1]}'))
        ui.ikindi_vakti.setText(_translate("Form", f'{gunlu["ogl"][0]}.{gunlu["ogl"][1]}'))
        ui.aksam_vakti.setText(_translate("Form", f'{gunlu["iki"][0]}.{gunlu["iki"][1]}'))
        ui.yatsi_vakti.setText(_translate("Form", f'{gunlu["aks"][0]}.{gunlu["aks"][1]}'))

        an = datetime.datetime.now()

        ui.lab_tarih.setText(_translate("Form", f"<html><head/><body><p align=\"center\">{tarih_ne(ui, f'{an.day}-{an.day+1} %B %Y')}</p></body></html>"))
        ui.imsak.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250));\ncolor:rgb(227, 227, 227)")
        ui.imsak_vakti.setStyleSheet("background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250));\ncolor:rgb(227, 227, 227)")
        
        kalan = (saat24 - toplam) + ims
        kalan_saat = kalan//3600
        kalan = kalan % 3600
        kalan_dakika = kalan//60
        kalan = kalan % 60
        kalan_saniye = kalan
        ui.lab_vaktin_cikmasina.setText(_translate("Form", "<html><head/><body><p align=\"right\">İmsak'ın Çıkmasına:  </p></body></html>"))
        simdiki_vakit = "İmsak'a"

    kuculduyse()
    time = QtCore.QTime(kalan_saat, kalan_dakika, kalan_saniye)

def kuculduyse():
    _translate = QtCore.QCoreApplication.translate
    if window_minimized == True:
        Form.setWindowTitle(_translate("Form", f"{simdiki_vakit} {str(time.hour()).zfill(2)}:{str(time.minute()).zfill(2)}:{str(time.second()).zfill(2)}"))

def timerEvent():
    global time
    kac_dakka_var()
        
    time = time.addSecs(-1)
    ui.kac_dakka_var.setTime(time)    

if __name__ == "__main__":
    global window_minimized

    window_minimized = False
    
    def changeEvent(event):
        global window_minimized
        
        if event.type() == QEvent.WindowStateChange:
            _translate = QtCore.QCoreApplication.translate

            if Form.windowState() & Qt.WindowMinimized:
                # minimized
                window_minimized = True
                kuculduyse()

            elif event.oldState() & Qt.WindowMinimized:
                # TEKRAR YUKSELDI
                window_minimized = False
                Form.setWindowTitle(_translate("Form", "Namaz Vakitleri"))


    import sys
    en_son_ne_zaman_calisti()
    vakitler = vakitleri_getir()

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    
    Form.changeEvent = changeEvent
    
    ui.setupUi(Form)
    kac_dakka_var()
    Form.show()


    timer = QtCore.QTimer()
    timer.timeout.connect(timerEvent)
    timer.start(1000)

    # while True:
    #     Beep(500, 1000)

    sys.exit(app.exec_())

# %a
# hafta gününün kısaltılmış adı

# %A
# hafta gününün tam adı

# %b
# ayın kısaltılmış adı

# %B
# ayın tam adı

# %c
# tam tarih, saat ve zaman bilgisi

# %d
# sayı değerli bir karakter dizisi olarak gün

# %j
# belli bir tarihin, yılın kaçıncı gününe denk geldiğini gösteren 1-366 arası bir sayı

# %m
# sayı değerli bir karakter dizisi olarak ay

# %U
# belli bir tarihin yılın kaçıncı haftasına geldiğini gösteren 0-53 arası bir sayı

# %y
# yılın son iki rakamı

# %Y
# yılın dört haneli tam hali

# %x
# tam tarih bilgisi

# %X
# tam saat bilgisi
