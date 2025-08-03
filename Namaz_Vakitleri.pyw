# Namaz Vakitleri
# v7.1
# 03.08.2025
# Çorum
# @Esofiso


# Gerekli kütüphaneler
import sys
import os
import json
import datetime
import locale
import calendar
from collections import namedtuple
from urllib.request import urlopen, URLError
from bs4 import BeautifulSoup

# PyQt5 ve Windows bildirim kütüphaneleri
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, Qt, QTimer, QTime, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QApplication
from win10toast import ToastNotifier

# Türkçe karakter ve tarih formatı için ayar
try:
    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')
    except locale.Error:
        print("Uyarı: Türkçe yerel ayarları yapılamadı. Tarih formatı İngilizce olabilir.")


# --- KONUM SEÇME PENCERESİNİN ARAYÜZÜ ---
class Ui_KonumSecimEkrani(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Pencere genişliği
        Form.resize(450, 156) 
        Form.setWindowTitle("Namaz Vakitleri | Konum Seçimi")
        Form.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:0.840909, y2:1, stop:0.460227 rgba(134, 207, 139, 255), stop:0.602273 rgba(86, 183, 159, 255), stop:0.761364 rgba(48, 153, 207, 255))")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ilce = QtWidgets.QLabel(Form)
        font = QtGui.QFont(); font.setFamily("TRT"); font.setPointSize(11)
        self.ilce.setFont(font)
        self.ilce.setStyleSheet("background:transparent;")
        self.ilce.setObjectName("ilce")
        self.gridLayout.addWidget(self.ilce, 2, 0, 1, 1)
        self.sehir_adi = QtWidgets.QComboBox(Form)
        self.sehir_adi.setStyleSheet("background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.142045 rgba(200, 200, 200, 255))")
        self.sehir_adi.setObjectName("sehir_adi")
        self.gridLayout.addWidget(self.sehir_adi, 1, 1, 1, 2)
        self.ulke = QtWidgets.QLabel(Form)
        font = QtGui.QFont(); font.setFamily("TRT"); font.setPointSize(11)
        self.ulke.setFont(font)
        self.ulke.setStyleSheet("background:transparent;")
        self.ulke.setObjectName("ulke")
        self.gridLayout.addWidget(self.ulke, 0, 0, 1, 1)
        self.sehir = QtWidgets.QLabel(Form)
        font = QtGui.QFont(); font.setFamily("TRT"); font.setPointSize(11)
        self.sehir.setFont(font)
        self.sehir.setStyleSheet("background:transparent;")
        self.sehir.setObjectName("sehir")
        self.gridLayout.addWidget(self.sehir, 1, 0, 1, 1)
        self.ulke_adi = QtWidgets.QComboBox(Form)
        self.ulke_adi.setStyleSheet("background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.142045 rgba(200, 200, 200, 255))")
        self.ulke_adi.setObjectName("ulke_adi")
        self.ulke_adi.setEnabled(False)
        self.gridLayout.addWidget(self.ulke_adi, 0, 1, 1, 2)
        self.ilce_adi = QtWidgets.QComboBox(Form)
        self.ilce_adi.setAutoFillBackground(False)
        self.ilce_adi.setStyleSheet("background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.142045 rgba(200, 200, 200, 255))")
        self.ilce_adi.setEditable(False)
        self.ilce_adi.setObjectName("ilce_adi")
        self.gridLayout.addWidget(self.ilce_adi, 2, 1, 1, 2)
        self.konum_sec_button = QtWidgets.QPushButton(Form)
        font = QtGui.QFont(); font.setFamily("TRT"); font.setPointSize(11)
        self.konum_sec_button.setFont(font)
        self.konum_sec_button.setStyleSheet("background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.142045 rgba(200, 200, 200, 255))")
        self.konum_sec_button.setObjectName("konum_sec_button")
        self.gridLayout.addWidget(self.konum_sec_button, 4, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.ilce.setText(_translate("Form", "<html><head/><body><p align=\"right\">İlçe:</p></body></html>"))
        self.ulke.setText(_translate("Form", "<html><head/><body><p align=\"right\">Ülke:</p></body></html>"))
        self.sehir.setText(_translate("Form", "<html><head/><body><p align=\"right\">Şehir:</p></body></html>"))
        self.konum_sec_button.setText(_translate("Form", "Seç"))
        self.ilce.hide()
        self.ilce_adi.hide()

# --- KONUM SEÇME PENCERESİ İŞLEYİŞİ ---
class KonumSecimDialog(QDialog):
    konumSecildi = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_KonumSecimEkrani()
        self.ui.setupUi(self)
        self.sehir_data = {
            "Adana": "adana", "Adıyaman": "adiyaman", "Afyonkarahisar": "afyonkarahisar", "Ağrı": "agri",
            "Amasya": "amasya", "Ankara": "ankara", "Antalya": "antalya", "Artvin": "artvin", "Aydın": "aydin",
            "Balıkesir": "balikesir", "Bilecik": "bilecik", "Bingöl": "bingol", "Bitlis": "bitlis", "Bolu": "bolu",
            "Burdur": "burdur", "Bursa": "bursa", "Çanakkale": "canakkale", "Çankırı": "cankiri", "Çorum": "corum",
            "Denizli": "denizli", "Diyarbakır": "diyarbakir", "Edirne": "edirne", "Elazığ": "elazig",
            "Erzincan": "erzincan", "Erzurum": "erzurum", "Eskişehir": "eskisehir", "Gaziantep": "gaziantep",
            "Giresun": "giresun", "Gümüşhane": "gumushane", "Hakkari": "hakkari", "Hatay": "hatay",
            "Isparta": "isparta", "Mersin": "mersin", "İstanbul": "istanbul", "İzmir": "izmir", "Kars": "kars",
            "Kastamonu": "kastamonu", "Kayseri": "kayseri", "Kırklareli": "kirklareli", "Kırşehir": "kirsehir",
            "Kocaeli": "kocaeli", "Konya": "konya", "Kütahya": "kutahya", "Malatya": "malatya",
            "Manisa": "manisa", "Kahramanmaraş": "kahramanmaras", "Mardin": "mardin", "Muğla": "mugla",
            "Muş": "mus", "Nevşehir": "nevsehir", "Niğde": "nigde", "Ordu": "ordu", "Rize": "rize",
            "Sakarya": "sakarya", "Samsun": "samsun", "Siirt": "siirt", "Sinop": "sinop", "Sivas": "sivas",
            "Tekirdağ": "tekirdag", "Tokat": "tokat", "Trabzon": "trabzon", "Tunceli": "tunceli",
            "Şanlıurfa": "sanliurfa", "Uşak": "usak", "Van": "van", "Yozgat": "yozgat",
            "Zonguldak": "zonguldak", "Aksaray": "aksaray", "Bayburt": "bayburt", "Karaman": "karaman",
            "Kırıkkale": "kirikkale", "Batman": "batman", "Şırnak": "sirnak", "Bartın": "bartin",
            "Ardahan": "ardahan", "Iğdır": "igdir", "Yalova": "yalova", "Karabük": "karabuk", "Kilis": "kilis",
            "Osmaniye": "osmaniye", "Düzce": "duzce"
        }
        self.ui.ulke_adi.addItems(["Türkiye"])
        self.ui.sehir_adi.addItems(sorted(self.sehir_data.keys()))
        self.ui.konum_sec_button.clicked.connect(self.konumu_onayla)

    def konumu_onayla(self):
        secili_sehir_gosterim = self.ui.sehir_adi.currentText()
        secili_sehir_id = self.sehir_data[secili_sehir_gosterim]
        self.konumSecildi.emit(secili_sehir_id)
        self.accept()
        
    def get_sehir_display_name(self, sehir_id):
        for display_name, id_name in self.sehir_data.items():
            if id_name == sehir_id:
                return display_name
        return sehir_id.capitalize()

# --- ANA PENCERENİN ARAYÜZÜ ---
class Ui_AnaPencere(QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 237)
        font = QtGui.QFont(); font.setFamily("Times New Roman"); font.setBold(False); font.setItalic(False); font.setWeight(50)
        Form.setFont(font)
        Form.setWindowOpacity(1.0)
        try:
            Form.setWindowIcon(QtGui.QIcon('cami_ikonu.png'))
        except:
            print("Uyarı: 'cami_ikonu.png' bulunamadı.")
            
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lab_namaz_vakitleri = QtWidgets.QLabel(Form)
        self.lab_namaz_vakitleri.setStyleSheet("background: transparent; font: 24pt \"TRT Medium Italic\"; color: black;")
        self.lab_namaz_vakitleri.setAlignment(Qt.AlignCenter)
        self.lab_namaz_vakitleri.setObjectName("lab_namaz_vakitleri")
        self.horizontalLayout_2.addWidget(self.lab_namaz_vakitleri)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontalLayout_2.addWidget(self.line_2)
        self.lab_tarih = QtWidgets.QLabel(Form)
        self.lab_tarih.setStyleSheet("background: transparent; font: 20pt \"TRT Medium\"; color: black;")
        self.lab_tarih.setObjectName("lab_tarih")
        self.horizontalLayout_2.addWidget(self.lab_tarih)
        self.verticalLayout_13.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.verticalLayout_13.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")


        def create_vakit_layout(name):
            layout = QtWidgets.QVBoxLayout()
            baslik = QtWidgets.QLabel(f"{name.capitalize()}", Form, font=QtGui.QFont("TRT Bold", 16), styleSheet="color: black;")
            vakit = QtWidgets.QLabel("--:--", Form, font=QtGui.QFont("Open Sans Light", 16), styleSheet="color: black;")
            layout.addWidget(baslik)
            layout.addWidget(vakit)
            return layout, baslik, vakit

        layouts = {}
        for name in ["imsak", "sabah", "ogle", "ikindi", "aksam", "yatsi"]:
            layouts[name] = create_vakit_layout(name)
            self.horizontalLayout.addLayout(layouts[name][0])
            if name != "yatsi":
                line = QtWidgets.QFrame(Form)
                line.setFrameShape(QtWidgets.QFrame.VLine)
                line.setFrameShadow(QtWidgets.QFrame.Plain)
                self.horizontalLayout.addWidget(line)

        self.imsak, self.imsak_vakti = layouts["imsak"][1], layouts["imsak"][2]
        self.sabah, self.sabah_vakti = layouts["sabah"][1], layouts["sabah"][2]
        self.ogle, self.ogle_vakti = layouts["ogle"][1], layouts["ogle"][2]
        self.ikindi, self.ikindi_vakti = layouts["ikindi"][1], layouts["ikindi"][2]
        self.aksam, self.aksam_vakti = layouts["aksam"][1], layouts["aksam"][2]
        self.yatsi, self.yatsi_vakti = layouts["yatsi"][1], layouts["yatsi"][2]

        self.imsak.setText(("İmsak"))
        self.sabah.setText(("Sabah"))
        self.ogle.setText(("Öğle"))
        self.ikindi.setText(("İkindi"))
        self.aksam.setText(("Akşam"))
        self.yatsi.setText(("Yatsı"))

        self.verticalLayout_13.addLayout(self.horizontalLayout)
        self.verticalLayout_7.addLayout(self.verticalLayout_13)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lab_vaktin_cikmasina = QtWidgets.QLabel(Form)
        self.lab_vaktin_cikmasina.setStyleSheet("font: 20pt \"TRT Bold\";\n"
"background:qradialgradient(spread:pad, cx:0.494, cy:0.505682, radius:0.5, fx:0.5, fy:0.517, stop:0 rgba(255, 188, 188, 0), stop:1 rgba(255, 255, 255, 0))")
        self.lab_vaktin_cikmasina.setObjectName("lab_vaktin_cikmasina")
        self.horizontalLayout_3.addWidget(self.lab_vaktin_cikmasina)
        self.kac_dakka_var_timeedit = QtWidgets.QTimeEdit(Form)
        self.kac_dakka_var_timeedit.setEnabled(False)
        self.kac_dakka_var_timeedit.setStyleSheet("font: 35pt \"TRT Bold\";\n"
"background:qradialgradient(spread:pad, cx:0.494, cy:0.505682, radius:0.5, fx:0.5, fy:0.517, stop:0 rgba(255, 188, 188, 0), stop:1 rgba(255, 255, 255, 0))")
        self.kac_dakka_var_timeedit.setFrame(False)
        self.kac_dakka_var_timeedit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.kac_dakka_var_timeedit.setObjectName("kac_dakka_var_timeedit")
        self.horizontalLayout_3.addWidget(self.kac_dakka_var_timeedit)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)

    def retranslateUi(self, Form, parent_app):
        an = datetime.datetime.now()
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Namaz Vakitleri"))
        self.kac_dakka_var_timeedit.setDisplayFormat(_translate("Form", "HH:mm:ss"))
        self.lab_vaktin_cikmasina.setText(_translate("Form", "     Vaktin Çıkmasına:"))
        display_name = parent_app.konum_penceresi.get_sehir_display_name(parent_app.sehir_id)
        self.lab_namaz_vakitleri.setText(_translate("Form", f"<html><head/><body><p>{display_name}</p></body></html>"))
        self.lab_tarih.setText(_translate("Form", f"<html><head/><body><p align=\"center\">{parent_app.tarih_ne('%d %B %A')}</p></body></html>"))
        self.sabah.setText("Güneş")

        sozluk = parent_app.vakitler_sozluk
        gun_str = str(an.day)
        if sozluk and gun_str in sozluk and sozluk[gun_str]["ims"]:
            gunlu = sozluk[gun_str]
            self.imsak_vakti.setText(f'{gunlu["ims"][0]}:{gunlu["ims"][1]}')
            self.sabah_vakti.setText(f'{gunlu["sab"][0]}:{gunlu["sab"][1]}')
            self.ogle_vakti.setText(f'{gunlu["ogl"][0]}:{gunlu["ogl"][1]}')
            self.ikindi_vakti.setText(f'{gunlu["iki"][0]}:{gunlu["iki"][1]}')
            self.aksam_vakti.setText(f'{gunlu["aks"][0]}:{gunlu["aks"][1]}')
            self.yatsi_vakti.setText(f'{gunlu["yat"][0]}:{gunlu["yat"][1]}')
        else:
            for vakit_label in [self.imsak_vakti, self.sabah_vakti, self.ogle_vakti, self.ikindi_vakti, self.aksam_vakti, self.yatsi_vakti]:
                vakit_label.setText("--:--")

# --- ANA PENCERENİN İŞLEYİŞİ ---
class AnaPencere(QWidget):
    CONFIG_FILE = "last_location.cfg"

    def __init__(self):
        super().__init__()
        self.ui = Ui_AnaPencere()
        self.ui.setupUi(self)

        # İlk çalıştırmada konum seçilip seçilmediğini kontrol eder
        self.konum_basariyla_yuklendi = True

        self.simdiki_vakit_adi = "shezmI"
        self.vakitler_sozluk = {}
        self.window_minimized = False
        
        self.konum_penceresi = KonumSecimDialog(self)
        self.toaster = ToastNotifier()

        # En son konumu yükle
        self.load_last_location()

        # Eğer ilk çalıştırmada kullanıcı konum seçmeden çıkarsa, devam etme
        if not self.konum_basariyla_yuklendi:
            return

        self.ui.lab_namaz_vakitleri.installEventFilter(self)
        self.konum_penceresi.konumSecildi.connect(self.konumuGuncelle)
        
        self.ui.lab_namaz_vakitleri.setWordWrap(False)

        self.en_son_ne_zaman_calisti()
        self.ui.retranslateUi(self, self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

        self.kac_dakka_var_hesapla()

    def load_last_location(self):
        # Eğer config dosyası yoksa veya boşsa, ilk çalıştırma olarak kabul et
        if not os.path.exists(self.CONFIG_FILE) or os.path.getsize(self.CONFIG_FILE) == 0:
            # Konum seçme penceresini zorunlu olarak aç
            # Kullanıcı "Seç" butonuna basarsa QDialog.Accepted döner
            if self.konum_penceresi.exec_() == QDialog.Accepted:
                # Seçilen konumu al ve sehir_id'ye ata
                secili_sehir_gosterim = self.konum_penceresi.ui.sehir_adi.currentText()
                secili_sehir_id = self.konum_penceresi.sehir_data[secili_sehir_gosterim]
                self.sehir_id = secili_sehir_id
                self.save_last_location() # Gelecek sefer için kaydet
            else:
                # Kullanıcı pencereyi seçmeden kapatırsa, bayrağı False yap
                self.konum_basariyla_yuklendi = False
                return
        else:
            # Eğer config dosyası varsa, normal şekilde oku
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    last_sehir = f.read().strip()
                    if last_sehir:
                        self.sehir_id = last_sehir
                    else: # Dosya var ama içi boşsa yine seçim ekranını aç
                        self.load_last_location()
            except Exception as e:
                print(f"Son konum yüklenirken hata oluştu: {e}")
                self.konum_basariyla_yuklendi = False

    def save_last_location(self):
        try:
            with open(self.CONFIG_FILE, "w") as f:
                f.write(self.sehir_id)
        except Exception as e:
            print(f"Son konum kaydedilirken hata oluştu: {e}")

    def vakits(self, sehir_id_to_fetch):
        display_name = self.konum_penceresi.get_sehir_display_name(sehir_id_to_fetch)
        self.ui.lab_namaz_vakitleri.setWordWrap(True)
        self.ui.lab_namaz_vakitleri.setText(f"'{display_name}' ...")
        QApplication.processEvents()

        bes_vakit = ("ims", "sab", "ogl", "iki", "aks", "yat")
        Saat = namedtuple("Saat", ["hour", "minute"], defaults=["00", "00"])
        now = datetime.datetime.now()
        num_days = calendar.monthrange(now.year, now.month)[1]
        days_dict = {str(i): {} for i in range(1, num_days + 1)}

        try:
            site = f"https://www.haberturk.com/namaz-vakitleri/{sehir_id_to_fetch}"
            html_source = urlopen(site, timeout=15)
            soup = BeautifulSoup(html_source, 'html.parser')
            imsakiye_table = soup.find("table")
            if not imsakiye_table: raise ValueError("İmsakiye tablosu bulunamadı.")
            rows = imsakiye_table.find("tbody").find_all("tr")
            for i, row in enumerate(rows):
                day_num = i + 1
                if str(day_num) in days_dict:
                    vakitler_raw = [td.text.strip() for td in row.find_all("td")[1:]]
                    if len(vakitler_raw) == len(bes_vakit):
                        vakitler_formatted = [Saat(*v.split(':')) for v in vakitler_raw]
                        days_dict[str(day_num)] = dict(zip(bes_vakit, vakitler_formatted))
            with open(f"{sehir_id_to_fetch}.txt", mode="w", encoding="utf-8") as f:
                json.dump(days_dict, f, indent=4)
            with open(f"en_son_ne_zaman_calisti_{sehir_id_to_fetch}.txt", "w") as file:
                file.write(now.strftime("%Y\n%m"))
            self.vakitler_sozluk = days_dict
        except (URLError, ValueError) as e:
            print(f"Hata: {e}")
            self.ui.lab_namaz_vakitleri.setText(f"İnternet Hatası veya\nGeçersiz Şehir!")
        except Exception as e:
            print(f"Beklenmedik hata: {e}")
            self.ui.lab_namaz_vakitleri.setText("Bilinmeyen Hata!")
        finally:
            self.ui.lab_namaz_vakitleri.setWordWrap(False)

    def en_son_ne_zaman_calisti(self):
        now = datetime.datetime.now()
        check_file = f"en_son_ne_zaman_calisti_{self.sehir_id}.txt"
        needs_update = True
        if os.path.exists(check_file) and os.path.exists(f"{self.sehir_id}.txt"):
            try:
                with open(check_file, "r") as file:
                    yıl, ay = file.read().strip().split("\n")
                    if int(yıl) == now.year and int(ay) == now.month:
                        needs_update = False
            except Exception: needs_update = True
        if needs_update: self.vakits(self.sehir_id)
        else: self.vakitleri_getir()

    def vakitleri_getir(self):
        try:
            with open(f"{self.sehir_id}.txt", "r") as file:
                self.vakitler_sozluk = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.vakits(self.sehir_id)

    def tarih_ne(self, istek):
        return datetime.datetime.strftime(datetime.datetime.now(), istek)

    def timerEvent(self):
            time_obj = self.ui.kac_dakka_var_timeedit.time()

            if time_obj.hour() == 0 and time_obj.minute() == 0 and time_obj.second() == 0:
                self.kac_dakka_var_hesapla()
            else:
                time_obj = time_obj.addSecs(-1)
                self.ui.kac_dakka_var_timeedit.setTime(time_obj)

                if self.window_minimized:
                    self.setWindowTitle(f"{self.simdiki_vakit_adi} {time_obj.toString()}")
                
                # --- BİLDİRİM KONTROLÜ ---
                if time_obj.hour() == 0 and time_obj.minute() == 15 and time_obj.second() == 0:
                    self.bildirim_gonder(f"{self.simdiki_vakit_adi} Vaktinin Çıkmasına", "Son 15 Dakika", 5)
                elif time_obj.hour() == 0 and time_obj.minute() == 7:
                    self.bildirim_gonder(f"{self.simdiki_vakit_adi} Vaktinin Çıkmasına", "Son 7 Dakika", 5)


    def yatsi_vakti_gosterimini_guncelle(self, bugunun_verileri, yarin_verileri):
        """Yatsı vaktine girildiğinde arayüzü kaydırarak günceller."""
        _translate = QtCore.QCoreApplication.translate

        # Arayüzdeki etiket ve vakit widget'larını bir listeye alalım
        etiket_widgetleri = [self.ui.imsak, self.ui.sabah, self.ui.ogle, self.ui.ikindi, self.ui.aksam, self.ui.yatsi]
        vakit_widgetleri = [self.ui.imsak_vakti, self.ui.sabah_vakti, self.ui.ogle_vakti, self.ui.ikindi_vakti, self.ui.aksam_vakti, self.ui.yatsi_vakti]

        # Yeni sıralamaya göre etiketler
        yeni_etiketler = ["Yatsı", "İmsak", "Güneş", "Öğle", "İkindi", "Akşam"]
        
        # Yarının vakitleri için kullanılacak anahtarlar
        yarin_vakit_anahtarlari = ["ims", "sab", "ogl", "iki", "aks"]

        # 1. Slot: Bugünün Yatsı Vakti
        etiket_widgetleri[0].setText(_translate("Form", yeni_etiketler[0]))
        vakit_widgetleri[0].setText(f'{bugunun_verileri["yat"][0]}:{bugunun_verileri["yat"][1]}')

        # Sonraki 5 slot: Yarının Vakitleri
        for i in range(1, 6):
            etiket_widgetleri[i].setText(_translate("Form", yeni_etiketler[i]))
            
            # Yarının verisinden ilgili vakti al
            vakit_anahtari = yarin_vakit_anahtarlari[i-1]
            vakit_degeri = yarin_verileri.get(vakit_anahtari)
            
            if vakit_degeri:
                vakit_widgetleri[i].setText(f'{vakit_degeri[0]}:{vakit_degeri[1]}')
            else:
                vakit_widgetleri[i].setText("--:--")

    def kac_dakka_var_hesapla(self):
        _translate = QtCore.QCoreApplication.translate
        an = datetime.datetime.now()

        # Gündüz vakitleri için orijinal yeşil arkaplan
        arkaplan_gunduz = "background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.018, fx:0, fy:0.014, stop:0.15894 rgba(5, 82, 45, 248), stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(3, 12, 18, 255))"
        # Akşam ve Yatsı için istenen mavimsi arkaplan
        arkaplan_gece = "background:qradialgradient(spread:pad, cx:0.583, cy:0.602881, radius:0.971914, fx:0.006, fy:0.0181152, stop:0.0431548 rgba(18, 25, 85, 253), stop:0.169643 rgba(29, 38, 198, 248), stop:0.375 rgba(57, 60, 255, 248), stop:0.770833 rgba(3, 12, 18, 255))"

        # Stil tanımlamaları
        stil_gecmis_baslik = "background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))"
        stil_gecmis_vakit = "background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255))"
        stil_aktif_baslik = "background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250)); color:rgb(227, 227, 227);"
        stil_aktif_vakit = "background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250)); color:rgb(227, 227, 227);"
        stil_normal_baslik = "background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255)); color: black;"
        stil_normal_vakit = "background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255)); color: black;"
        
        self.ui.retranslateUi(self, self)

        all_widgets = [self.ui.imsak, self.ui.sabah, self.ui.ogle, self.ui.ikindi, self.ui.aksam, self.ui.yatsi]
        all_vakit_widgets = [self.ui.imsak_vakti, self.ui.sabah_vakti, self.ui.ogle_vakti, self.ui.ikindi_vakti, self.ui.aksam_vakti, self.ui.yatsi_vakti]
        
        for w in all_widgets: w.setStyleSheet(stil_normal_baslik)
        for w in all_vakit_widgets: w.setStyleSheet(stil_normal_vakit)
        
        gun_str = str(an.day)
        if not self.vakitler_sozluk or gun_str not in self.vakitler_sozluk or not self.vakitler_sozluk[gun_str]:
            self.ui.lab_vaktin_cikmasina.setText("Veri bekleniyor...")
            return

        gunun_verileri = self.vakitler_sozluk[gun_str]
        toplam_saniye = an.hour * 3600 + an.minute * 60 + an.second
        
        try:
            vakit_saniyeleri = {k: int(v[0]) * 3600 + int(v[1]) * 60 for k, v in gunun_verileri.items()}
        except (ValueError, TypeError, KeyError):
            self.ui.lab_vaktin_cikmasina.setText("Hatalı veri..."); return

        kalan = 0
        sonraki_vakit_adi = ""

        def set_styles(aktif_index):
            for i in range(aktif_index):
                all_widgets[i].setStyleSheet(stil_gecmis_baslik)
                all_vakit_widgets[i].setStyleSheet(stil_gecmis_vakit)
            if aktif_index >= 0 and aktif_index < len(all_widgets):
                all_widgets[aktif_index].setStyleSheet(stil_aktif_baslik)
                all_vakit_widgets[aktif_index].setStyleSheet(stil_aktif_vakit)

        if toplam_saniye < vakit_saniyeleri["ims"]:
            self.simdiki_vakit_adi = "Yatsı" # Önceki günden kalan
            sonraki_vakit_adi = "İmsak"
            kalan = vakit_saniyeleri["ims"] - toplam_saniye
            set_styles(-1)
        elif toplam_saniye < vakit_saniyeleri["sab"]:
            self.simdiki_vakit_adi = "İmsak"
            sonraki_vakit_adi = "Güneş"
            kalan = vakit_saniyeleri["sab"] - toplam_saniye
            set_styles(0)
        elif toplam_saniye < vakit_saniyeleri["ogl"]:
            self.simdiki_vakit_adi = "Güneş"
            sonraki_vakit_adi = "Öğle"
            kalan = vakit_saniyeleri["ogl"] - toplam_saniye
            set_styles(1)
        elif toplam_saniye < vakit_saniyeleri["iki"]:
            self.simdiki_vakit_adi = "Öğle"
            sonraki_vakit_adi = "İkindi"
            kalan = vakit_saniyeleri["iki"] - toplam_saniye
            set_styles(2)
        elif toplam_saniye < vakit_saniyeleri["aks"]:
            self.simdiki_vakit_adi = "İkindi"
            sonraki_vakit_adi = "Akşam"
            kalan = vakit_saniyeleri["aks"] - toplam_saniye
            set_styles(3)
        elif toplam_saniye < vakit_saniyeleri["yat"]:
            self.simdiki_vakit_adi = "Akşam"
            sonraki_vakit_adi = "Yatsı"
            kalan = vakit_saniyeleri["yat"] - toplam_saniye
            set_styles(4)

        else: # Yatsı vakti ve sonrası
            self.simdiki_vakit_adi = "Yatsı"
            sonraki_vakit_adi = "İmsak"

            # Ay sonu hatalarını önlemek için timedelta kullanmak daha güvenlidir
            sonraki_gun = an + datetime.timedelta(days=1)
            sonraki_gun_str = str(sonraki_gun.day)
            
            # Eğer ay sonu değilse ve sonraki günün verisi mevcutsa...
            if sonraki_gun_str in self.vakitler_sozluk and self.vakitler_sozluk[sonraki_gun_str].get("ims"):
                sonraki_gun_verileri = self.vakitler_sozluk[sonraki_gun_str]
                
                # 1. ADIM: Arayüzü yeni kaydırılmış düzene göre güncelle
                self.yatsi_vakti_gosterimini_guncelle(gunun_verileri, sonraki_gun_verileri)

                # 2. ADIM: Kalan zamanı yarının imsak vaktine göre hesapla (Bu kısım aynı kalıyor)
                ims_sonraki = int(sonraki_gun_verileri["ims"][0]) * 3600 + int(sonraki_gun_verileri["ims"][1]) * 60
                kalan = (24 * 3600 - toplam_saniye) + ims_sonraki
                
                # 3. ADIM: Stilleri yeni düzene göre ayarla
                # Önce tüm stilleri normale çevir.
                for i in range(len(all_widgets)):
                    all_widgets[i].setStyleSheet(stil_normal_baslik)
                    all_vakit_widgets[i].setStyleSheet(stil_normal_vakit)
                
                # Şimdi aktif olan Yatsı vakti ilk slotta olduğu için ilk slotu "aktif" yap.
                self.ui.imsak.setStyleSheet(stil_aktif_baslik)
                self.ui.imsak_vakti.setStyleSheet(stil_aktif_vakit)

            else: # Ay sonu ise (orijinal davranış korunuyor)
                kalan = (24 * 3600) - toplam_saniye
                sonraki_vakit_adi = "Yeni Ay" # Ay sonu özel durumu
                set_styles(5) # Normal düzende Yatsı'yı (son slot) aktif yap



        # --- ARKA PLAN DEĞİŞİM İŞLEYİŞİ ---
        # Mevcut vaktin adı 'Akşam' veya 'Yatsı' ise gece arkaplanını, değilse gündüz arkaplanını ayarla
        if self.simdiki_vakit_adi in ["Akşam", "Yatsı"]:
            self.setStyleSheet(arkaplan_gece)
        else:
            self.setStyleSheet(arkaplan_gunduz)


        # Geri sayım etiketini bir sonraki vaktin adına göre ayarla
        self.ui.lab_vaktin_cikmasina.setText(f'<html><head/><body><p align="right">{sonraki_vakit_adi} Vaktine: </p></body></html>')

        kalan_saat, kalan_saniye_rem = divmod(kalan, 3600)
        kalan_dakika, kalan_saniye = divmod(kalan_saniye_rem, 60)
        self.ui.kac_dakka_var_timeedit.setTime(QTime(kalan_saat, kalan_dakika, kalan_saniye))        

    @pyqtSlot(str)
    def konumuGuncelle(self, yeni_sehir_id):
        """
        Konum seçme penceresinden gelen sinyali yakalar,
        yeni seçilen şehre göre verileri ve arayüzü günceller.
        """
        if self.sehir_id != yeni_sehir_id:
            self.sehir_id = yeni_sehir_id
            # Yeni şehir için vakitleri internetten veya dosyadan tekrar yükle
            self.en_son_ne_zaman_calisti()
            # Arayüzdeki şehir adı gibi metinleri yenile
            self.ui.retranslateUi(self, self)
            # Yeni vakitlere göre sayacı ve stilleri yeniden hesapla
            self.kac_dakka_var_hesapla()
            # Son seçilen konumu ileride kullanmak üzere kaydet
            self.save_last_location()
        
    def bildirim_gonder(self, baslik, mesaj, sure):
        try: 
            self.toaster.show_toast(baslik, mesaj, duration=sure, threaded=True)
        except Exception as e: 
            print(f"Bildirim hatası: {e}")

    def eventFilter(self, source, event):
        if source is self.ui.lab_namaz_vakitleri and event.type() == QEvent.MouseButtonDblClick:
            self.konum_penceresi.exec_()
            return True
        return super().eventFilter(source, event)
    
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized(): 
                self.window_minimized = True
            elif event.oldState() & Qt.WindowMinimized:
                self.window_minimized = False
                self.setWindowTitle("Namaz Vakitleri")
        super().changeEvent(event)
        
# --- UYGULAMAYI BAŞLAT ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()

    # Eğer konum başarıyla yüklendiyse (veya ilk seferde seçildiyse) pencereyi göster
    if ana_pencere.konum_basariyla_yuklendi:
        ana_pencere.show()
        sys.exit(app.exec_())
    # Aksi halde (kullanıcı ilk seçim ekranını kapattıysa) uygulama sessizce sonlanır