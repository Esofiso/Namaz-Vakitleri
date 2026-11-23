# Namaz-Vakitleri
# v10 Twilight (Karanlık Tema, Dinamik Temalar, Hicri Tarih, Anımsatıcılar, Grafik, Hadis)
# 23.11.2026
# Ankara
# @Esofiso

# Gerekli kütüphaneler
import sys
import os
import json
import random
import datetime
import locale
import calendar
from collections import namedtuple
from urllib.request import urlopen, URLError
from bs4 import BeautifulSoup

# PyQt5 ve Windows bildirim kütüphaneleri
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, Qt, QTimer, QTime, pyqtSlot, pyqtSignal, QPoint, QPointF, QRectF
from PyQt5.QtWidgets import (
    QWidget, QDialog, QApplication, QPushButton, QFrame, QLabel,
    QVBoxLayout, QHBoxLayout, QListWidget, QSpinBox, QRadioButton,
    QButtonGroup, QMenu, QAction
)

try:
    from win10toast import ToastNotifier
except ImportError:
    ToastNotifier = None

# Türkçe karakter ve tarih formatı için ayar
try:
    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')
    except locale.Error:
        print("Uyarı: Türkçe yerel ayarları yapılamadı. Tarih formatı İngilizce olabilir.")


# --- Hicri Tarih ve Özel Gün Hesaplama Yardımcıları ---
HICRI_AYLAR = [
    "", "Muharrem", "Safer", "Rebiülevvel", "Rebiülahir",
    "Cemaziyelevvel", "Cemaziyelahir", "Recep", "Şaban",
    "Ramazan", "Şevval", "Zilkade", "Zilhicce"
]

def miladi_to_jdn(yil, ay, gun):
    a = (14 - ay) // 12
    y = yil + 4800 - a
    m = ay + 12 * a - 3
    return gun + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

def miladi_to_hicri(yil, ay, gun):
    jd = miladi_to_jdn(yil, ay, gun)
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    h_ay = (24 * l) // 709
    h_gun = l - (709 * h_ay) // 24
    h_yil = 30 * n + j - 30
    return h_yil, h_ay, h_gun

def hicri_tarih_metni(an):
    h_yil, h_ay, h_gun = miladi_to_hicri(an.year, an.month, an.day)
    ay_adi = HICRI_AYLAR[h_ay] if 1 <= h_ay <= 12 else ""
    return f"{h_gun} {ay_adi} {h_yil}"

def ozel_gun_bul(an, aksam_sonrasi=False):
    # Akşam ezanından sonra Hicri gece bir sonraki güne geçer
    kontrol_tarihi = an + datetime.timedelta(days=1) if aksam_sonrasi else an
    _, h_ay, h_gun = miladi_to_hicri(kontrol_tarihi.year, kontrol_tarihi.month, kontrol_tarihi.day)

    # Bayramlar
    if h_ay == 10 and h_gun in (1, 2, 3):
        return "Ramazan Bayramı"
    if h_ay == 12 and h_gun in (10, 11, 12, 13):
        return "Kurban Bayramı"

    # Kandil geceleri
    if h_ay == 9 and h_gun == 27:
        return "Kadir Gecesi"
    if h_ay == 3 and h_gun == 12:
        return "Mevlid Kandili"
    if h_ay == 7 and h_gun == 27:
        return "Miraç Kandili"
    if h_ay == 8 and h_gun == 15:
        return "Berat Kandili"
    # Regaip Kandili: Recep ayının ilk cuma gecesi (Perşembe akşamı / ilk cuma)
    if h_ay == 7 and h_gun <= 7 and kontrol_tarihi.weekday() == 4:
        return "Regaip Kandili"

    # Ramazan Ayı
    if h_ay == 9:
        return "Ramazan Ayı"

    # Cuma Günü (Perşembe akşamından Cuma akşamına kadar)
    if (an.weekday() == 4 and not aksam_sonrasi) or (an.weekday() == 3 and aksam_sonrasi):
        return "Hayırlı Cumalar"

    return None


# --- Varsayılan Hadis Veri Tabanı ---
VARSAYILAN_HADISLER = [
    {"metin": "Namaz Vakitleri v10 · Twilight · @esofiso · 23.11.2026 | All Rights Reserved."}
]

VARSAYILAN_ANIMSATICILAR = {
    vakit: [
        {"dakika": 15, "tip": "tek"},
        {"dakika": 7, "tip": "bir_dakika"}
    ]
    for vakit in ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]
}

VAKIT_AD_TO_KEY = {
    "İmsak": "ims",
    "Güneş": "sab",
    "Sabah": "sab",
    "Öğle": "ogl",
    "İkindi": "iki",
    "Akşam": "aks",
    "Yatsı": "yat"
}

VAKIT_KEY_TO_AD = {
    "ims": "İmsak",
    "sab": "Güneş",
    "ogl": "Öğle",
    "iki": "İkindi",
    "aks": "Akşam",
    "yat": "Yatsı"
}


# --- Kompakt/Pinlenmiş Pencere Sınıfı ---
class KompaktPencere(QWidget):
    tamGorunumeGecSignal = pyqtSignal()
    uygulamayiKapatSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.dragPos = QPoint()

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.unpinButton = QPushButton("📌", self)
        self.unpinButton.setFixedSize(20, 20)
        self.unpinButton.setStyleSheet(
            "QPushButton { background-color: #22c55e; border-radius: 10px; border: 1px solid #16a34a; } "
            "QPushButton:hover { background-color: #34d399; }"
        )
        self.unpinButton.setToolTip("Tam Görünüme Geç")
        self.unpinButton.clicked.connect(self.tamGorunumeGecSignal.emit)

        self.closeButton = QPushButton("×", self)
        self.closeButton.setFixedSize(20, 20)
        self.closeButton.setStyleSheet(
            "QPushButton { background-color: #f87171; border-radius: 10px; border: 1px solid #dc2626; font-weight: bold; } "
            "QPushButton:hover { background-color: #fca5a5; }"
        )
        self.closeButton.setToolTip("Kapat")
        self.closeButton.clicked.connect(self.uygulamayiKapatSignal.emit)

        self.vakit_adi = QLabel("Vakit")
        self.vakit_saati = QLabel("00:00")

        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setEnabled(False)
        self.time_edit.setStyleSheet('font: 28pt "TRT Bold"; background: transparent;')
        self.time_edit.setFrame(False)
        self.time_edit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.time_edit.setDisplayFormat("H:mm:ss")

        layout.addWidget(self.closeButton)
        layout.addWidget(self.unpinButton)
        layout.addWidget(self.vakit_adi)
        layout.addWidget(self.vakit_saati)
        layout.addWidget(self.time_edit)

    def guncelle(self, ad, saat, stil_ad, stil_saat, font_ad, font_saat, time_obj, dark_mode=False):
        self.vakit_adi.setText(ad)
        self.vakit_saati.setText(saat)
        self.vakit_adi.setStyleSheet(stil_ad)
        self.vakit_saati.setStyleSheet(stil_saat)
        self.vakit_adi.setFont(font_ad)
        self.vakit_saati.setFont(font_saat)
        self.time_edit.setTime(time_obj)
        if dark_mode:
            self.time_edit.setStyleSheet('font: 28pt "TRT Bold"; background: transparent; color: #f3f4f6;')
        else:
            self.time_edit.setStyleSheet('font: 28pt "TRT Bold"; background: transparent;')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


# --- Anımsatıcı Second Layer (Aynı Pencere İçinde Katman) ---
class AnimsaticiKatmani(QFrame):
    animsaticiDegisti = pyqtSignal()

    def __init__(self, parent_app, parent_widget):
        super().__init__(parent_widget)
        self.parent_app = parent_app
        self.aktif_vakit = "İmsak"
        self.secili_index = None

        self.setObjectName("animsatici_overlay")
        self.setStyleSheet("QFrame#animsatici_overlay { background-color: rgba(0, 0, 0, 175); border-radius: 10px; }")
        self.hide()

        dis_layout = QVBoxLayout(self)
        dis_layout.setContentsMargins(20, 12, 20, 12)
        dis_layout.setAlignment(Qt.AlignCenter)

        self.kart = QFrame(self)
        self.kart.setObjectName("animsatici_kart")
        self.kart.setFixedWidth(560)
        self.kart.setMaximumHeight(225)
        dis_layout.addWidget(self.kart)

        kart_layout = QVBoxLayout(self.kart)
        kart_layout.setContentsMargins(14, 10, 14, 10)
        kart_layout.setSpacing(8)

        # Üst başlık satırı
        ust_row = QHBoxLayout()
        self.baslik_lbl = QLabel("Anımsatıcılar", self.kart)
        self.baslik_lbl.setFont(QtGui.QFont("TRT Bold", 12))
        ust_row.addWidget(self.baslik_lbl)
        ust_row.addStretch()

        self.kapat_btn = QPushButton("×", self.kart)
        self.kapat_btn.setFixedSize(22, 22)
        self.kapat_btn.setStyleSheet(
            "QPushButton { background-color: #ef4444; color: white; border-radius: 11px; border: none; font-weight: bold; } "
            "QPushButton:hover { background-color: #f87171; }"
        )
        self.kapat_btn.clicked.connect(self.hide)
        ust_row.addWidget(self.kapat_btn)
        kart_layout.addLayout(ust_row)

        # İçerik: Sol liste, sağ düzenleme formu
        icerik_row = QHBoxLayout()
        icerik_row.setSpacing(12)

        self.liste = QListWidget(self.kart)
        self.liste.setFont(QtGui.QFont("TRT Medium", 10))
        self.liste.itemClicked.connect(self._ogeye_tiklandi)
        icerik_row.addWidget(self.liste, 3)

        form_col = QVBoxLayout()
        form_col.setSpacing(6)

        dk_row = QHBoxLayout()
        self.dk_lbl = QLabel("Çıkmasına (dk):", self.kart)
        self.dk_lbl.setFont(QtGui.QFont("TRT Medium", 10))
        self.dk_spin = QSpinBox(self.kart)
        self.dk_spin.setRange(1, 180)
        self.dk_spin.setValue(10)
        self.dk_spin.setFont(QtGui.QFont("TRT Medium", 10))
        dk_row.addWidget(self.dk_lbl)
        dk_row.addWidget(self.dk_spin)
        form_col.addLayout(dk_row)

        self.rb_tek = QRadioButton("Tek Bildirim", self.kart)
        self.rb_bir_dk = QRadioButton("1 Dakikalık Bildirim", self.kart)
        self.rb_tek.setFont(QtGui.QFont("TRT Medium", 9))
        self.rb_bir_dk.setFont(QtGui.QFont("TRT Medium", 9))
        self.rb_tek.setChecked(True)

        self.rb_grup = QButtonGroup(self.kart)
        self.rb_grup.addButton(self.rb_tek)
        self.rb_grup.addButton(self.rb_bir_dk)
        form_col.addWidget(self.rb_tek)
        form_col.addWidget(self.rb_bir_dk)

        form_col.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        self.kaydet_btn = QPushButton("Ekle", self.kart)
        self.kaydet_btn.setFont(QtGui.QFont("TRT Bold", 9))
        self.kaydet_btn.clicked.connect(self._ekle_veya_guncelle)

        self.sil_btn = QPushButton("Sil", self.kart)
        self.sil_btn.setFont(QtGui.QFont("TRT Bold", 9))
        self.sil_btn.clicked.connect(self._secili_sil)

        self.yeni_btn = QPushButton("Yeni", self.kart)
        self.yeni_btn.setFont(QtGui.QFont("TRT Medium", 9))
        self.yeni_btn.clicked.connect(self._formu_sifirla)

        btn_row.addWidget(self.kaydet_btn)
        btn_row.addWidget(self.sil_btn)
        btn_row.addWidget(self.yeni_btn)
        form_col.addLayout(btn_row)

        icerik_row.addLayout(form_col, 2)
        kart_layout.addLayout(icerik_row)

        self.tema_uygula(False)

    def tema_uygula(self, dark_mode):
        if dark_mode:
            self.kart.setStyleSheet("""
                QFrame#animsatici_kart {
                    background-color: #181b20;
                    border: 1px solid #303642;
                    border-radius: 10px;
                }
                QLabel, QRadioButton { color: #e5e7eb; background: transparent; }
                QListWidget {
                    background-color: #101216;
                    color: #e5e7eb;
                    border: 1px solid #2b313c;
                    border-radius: 6px;
                    padding: 3px;
                }
                QListWidget::item:selected { background-color: #2563eb; color: #ffffff; border-radius: 4px; }
                QSpinBox {
                    background-color: #101216;
                    color: #f3f4f6;
                    border: 1px solid #2b313c;
                    border-radius: 4px;
                    padding: 2px 4px;
                }
                QPushButton {
                    background-color: #262c36;
                    color: #f3f4f6;
                    border: 1px solid #3a4252;
                    border-radius: 5px;
                    padding: 4px 8px;
                }
                QPushButton:hover { background-color: #333b49; }
            """)
        else:
            self.kart.setStyleSheet("""
                QFrame#animsatici_kart {
                    background-color: #f8fafc;
                    border: 1px solid #cbd5e1;
                    border-radius: 10px;
                }
                QLabel, QRadioButton { color: #0f172a; background: transparent; }
                QListWidget {
                    background-color: #ffffff;
                    color: #0f172a;
                    border: 1px solid #cbd5e1;
                    border-radius: 6px;
                    padding: 3px;
                }
                QListWidget::item:selected { background-color: #0d9488; color: #ffffff; border-radius: 4px; }
                QSpinBox {
                    background-color: #ffffff;
                    color: #0f172a;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    padding: 2px 4px;
                }
                QPushButton {
                    background-color: #e2e8f0;
                    color: #0f172a;
                    border: 1px solid #94a3b8;
                    border-radius: 5px;
                    padding: 4px 8px;
                }
                QPushButton:hover { background-color: #cbd5e1; }
            """)
        self.kapat_btn.setStyleSheet(
            "QPushButton { background-color: #ef4444; color: white; border-radius: 11px; border: none; font-weight: bold; padding: 0px; } "
            "QPushButton:hover { background-color: #f87171; }"
        )

    def ac(self, vakit_adi):
        self.aktif_vakit = vakit_adi
        self.baslik_lbl.setText(f"{vakit_adi} Vakti Anımsatıcıları")
        self.tema_uygula(self.parent_app.dark_mode)
        self._formu_sifirla()
        self._listeyi_yenile()
        self.setGeometry(self.parentWidget().rect())
        self.raise_()
        self.show()

    def _listeyi_yenile(self):
        self.liste.clear()
        kayitlar = self.parent_app.animsaticilar.get(self.aktif_vakit, [])
        kayitlar.sort(key=lambda x: x["dakika"], reverse=True)
        for item in kayitlar:
            tip_str = "Tek Bildirim" if item["tip"] == "tek" else "1 Dakikalık Bildirim"
            self.liste.addItem(f'{item["dakika"]} dk önce  —  {tip_str}')

    def _ogeye_tiklandi(self, _item):
        row = self.liste.currentRow()
        kayitlar = self.parent_app.animsaticilar.get(self.aktif_vakit, [])
        if 0 <= row < len(kayitlar):
            self.secili_index = row
            secilen = kayitlar[row]
            self.dk_spin.setValue(int(secilen["dakika"]))
            if secilen["tip"] == "tek":
                self.rb_tek.setChecked(True)
            else:
                self.rb_bir_dk.setChecked(True)
            self.kaydet_btn.setText("Güncelle")

    def _formu_sifirla(self):
        self.secili_index = None
        self.liste.clearSelection()
        self.dk_spin.setValue(10)
        self.rb_tek.setChecked(True)
        self.kaydet_btn.setText("Ekle")

    def _ekle_veya_guncelle(self):
        dk = int(self.dk_spin.value())
        tip = "tek" if self.rb_tek.isChecked() else "bir_dakika"
        kayitlar = self.parent_app.animsaticilar.setdefault(self.aktif_vakit, [])

        if self.secili_index is not None and 0 <= self.secili_index < len(kayitlar):
            kayitlar[self.secili_index] = {"dakika": dk, "tip": tip}
        else:
            kayitlar.append({"dakika": dk, "tip": tip})

        self.parent_app.animsaticilari_kaydet()
        self._listeyi_yenile()
        self._formu_sifirla()
        self.animsaticiDegisti.emit()

    def _secili_sil(self):
        row = self.liste.currentRow()
        kayitlar = self.parent_app.animsaticilar.get(self.aktif_vakit, [])
        if 0 <= row < len(kayitlar):
            kayitlar.pop(row)
            self.parent_app.animsaticilari_kaydet()
            self._listeyi_yenile()
            self._formu_sifirla()
            self.animsaticiDegisti.emit()

    def mousePressEvent(self, event):
        # Kart dışına tıklanınca katmanı kapat
        if not self.kart.geometry().contains(event.pos()):
            self.hide()
        event.accept()


# --- 1 Aylık Etkileşimli (Kaydırılabilir & Yakınlaştırılabilir) Vakit Grafiği ---
class VakitGrafikCanvas(QWidget):
    RENKLER = {
        "ims": QtGui.QColor("#38bdf8"),
        "sab": QtGui.QColor("#facc15"),
        "ogl": QtGui.QColor("#22c55e"),
        "iki": QtGui.QColor("#fb923c"),
        "aks": QtGui.QColor("#f43f5e"),
        "yat": QtGui.QColor("#a78bfa"),
    }

    def __init__(self, vakitler_sozluk, secili_key="all", dark_mode=False, parent=None):
        super().__init__(parent)
        self.vakitler_sozluk = vakitler_sozluk
        self.secili_key = secili_key
        self.dark_mode = dark_mode
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)

        self.margin_left = 62
        self.margin_right = 24
        self.margin_top = 24
        self.margin_bottom = 38

        self._panning = False
        self._pan_start = QPoint()
        self._pan_bounds = (0.0, 31.0, 0.0, 1440.0)
        self._hover_pos = None

        self.gunler = []
        self.seriler = {k: [] for k in ["ims", "sab", "ogl", "iki", "aks", "yat"]}
        self._veriyi_hazirla()
        self.gorunumu_sifirla()

    def _veriyi_hazirla(self):
        self.gunler = sorted([int(g) for g in self.vakitler_sozluk.keys() if g.isdigit() and self.vakitler_sozluk[g]])
        for k in self.seriler:
            self.seriler[k] = []
        for g in self.gunler:
            gun_veri = self.vakitler_sozluk.get(str(g), {})
            for k in self.seriler:
                v = gun_veri.get(k)
                if v and len(v) >= 2:
                    try:
                        dk = int(v[0]) * 60 + int(v[1])
                        self.seriler[k].append((g, dk))
                    except ValueError:
                        pass

    def filtre_degistir(self, key):
        self.secili_key = key
        self.gorunumu_sifirla()
        self.update()

    def gorunumu_sifirla(self):
        if not self.gunler:
            self.x_min, self.x_max = 0.5, 31.5
            self.y_min, self.y_max = 0.0, 1440.0
            return

        self.x_min = min(self.gunler) - 0.6
        self.x_max = max(self.gunler) + 0.6

        if self.secili_key == "all":
            degerler = [dk for k in self.seriler for _, dk in self.seriler[k]]
            pad = 45.0
        else:
            degerler = [dk for _, dk in self.seriler.get(self.secili_key, [])]
            pad = 8.0

        if degerler:
            mn, mx = min(degerler), max(degerler)
            if mx - mn < 10:
                mn -= 10
                mx += 10
            self.y_min = max(0.0, mn - pad)
            self.y_max = min(1440.0, mx + pad)
        else:
            self.y_min, self.y_max = 0.0, 1440.0
        self.update()

    def _plot_rect(self):
        return QRectF(
            self.margin_left,
            self.margin_top,
            max(10, self.width() - self.margin_left - self.margin_right),
            max(10, self.height() - self.margin_top - self.margin_bottom)
        )

    def _to_screen(self, x_val, y_val, rect):
        sx = rect.left() + (x_val - self.x_min) / (self.x_max - self.x_min) * rect.width()
        sy = rect.bottom() - (y_val - self.y_min) / (self.y_max - self.y_min) * rect.height()
        return QPointF(sx, sy)

    def _uygun_adim(self, aralik, adaylar, hedef_sayisi=6):
        for adim in adaylar:
            if aralik / adim <= hedef_sayisi + 2:
                return adim
        return adaylar[-1]

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        bg = QtGui.QColor("#111318") if self.dark_mode else QtGui.QColor("#f8fafc")
        plot_bg = QtGui.QColor("#181c23") if self.dark_mode else QtGui.QColor("#ffffff")
        grid_c = QtGui.QColor("#2a303c") if self.dark_mode else QtGui.QColor("#e2e8f0")
        text_c = QtGui.QColor("#cbd5e1") if self.dark_mode else QtGui.QColor("#334155")
        border_c = QtGui.QColor("#374151") if self.dark_mode else QtGui.QColor("#cbd5e1")

        p.fillRect(self.rect(), bg)
        rect = self._plot_rect()
        p.fillRect(rect, plot_bg)

        # Y ekseni ızgara ve saat etiketleri
        y_span = max(1.0, self.y_max - self.y_min)
        y_step = self._uygun_adim(y_span, [1, 2, 5, 10, 15, 30, 60, 120, 180, 240], 6)
        ilk_y = int(self.y_min // y_step) * y_step

        p.setFont(QtGui.QFont("TRT Medium", 9))
        y_val = ilk_y
        while y_val <= self.y_max + y_step:
            if self.y_min <= y_val <= self.y_max and 0 <= y_val < 1440:
                pt = self._to_screen(self.x_min, y_val, rect)
                p.setPen(QtGui.QPen(grid_c, 1, Qt.DashLine))
                p.drawLine(QPointF(rect.left(), pt.y()), QPointF(rect.right(), pt.y()))
                p.setPen(text_c)
                saat_str = f"{int(y_val // 60):02d}:{int(y_val % 60):02d}"
                p.drawText(QRectF(4, pt.y() - 9, self.margin_left - 10, 18), Qt.AlignRight | Qt.AlignVCenter, saat_str)
            y_val += y_step

        # X ekseni ızgara ve gün etiketleri
        x_span = max(1.0, self.x_max - self.x_min)
        x_step = self._uygun_adim(x_span, [1, 2, 3, 5, 10], 10)
        ilk_x = max(1, int(self.x_min // x_step) * x_step)
        max_gun = max(self.gunler) if self.gunler else 31

        x_val = ilk_x
        while x_val <= min(max_gun, int(self.x_max) + x_step):
            if self.x_min <= x_val <= self.x_max and 1 <= x_val <= max_gun:
                pt = self._to_screen(x_val, self.y_min, rect)
                p.setPen(QtGui.QPen(grid_c, 1, Qt.DashLine))
                p.drawLine(QPointF(pt.x(), rect.top()), QPointF(pt.x(), rect.bottom()))
                p.setPen(text_c)
                p.drawText(QRectF(pt.x() - 16, rect.bottom() + 6, 32, 20), Qt.AlignCenter, str(int(x_val)))
            x_val += x_step

        # Çerçeve
        p.setPen(QtGui.QPen(border_c, 1))
        p.drawRect(rect)

        # Kırpma alanı içinde çizgiler
        p.setClipRect(rect)

        # Bugünün dikey vurgusu
        bugun = datetime.datetime.now().day
        if self.x_min <= bugun <= self.x_max:
            bx = self._to_screen(bugun, self.y_min, rect).x()
            p.setPen(QtGui.QPen(QtGui.QColor("#ef4444"), 1.5, Qt.DotLine))
            p.drawLine(QPointF(bx, rect.top()), QPointF(bx, rect.bottom()))

        keys_to_draw = list(self.seriler.keys()) if self.secili_key == "all" else [self.secili_key]
        for k in keys_to_draw:
            noktalar = self.seriler.get(k, [])
            if not noktalar:
                continue
            renk = self.RENKLER[k]
            pen = QtGui.QPen(renk, 2.2)
            p.setPen(pen)

            ekran_noktalari = [self._to_screen(g, dk, rect) for g, dk in noktalar]
            for i in range(len(ekran_noktalari) - 1):
                p.drawLine(ekran_noktalari[i], ekran_noktalari[i + 1])

            p.setBrush(renk)
            for (g, _), pt in zip(noktalar, ekran_noktalari):
                r = 4.2 if g == bugun else 2.6
                p.drawEllipse(pt, r, r)

        p.setClipping(False)

        # Fare ile üzerine gelince gün ve saat bilgisi
        if self._hover_pos and rect.contains(self._hover_pos) and self.gunler:
            mx = self._hover_pos.x()
            gun_tahmin = int(round(self.x_min + (mx - rect.left()) / rect.width() * (self.x_max - self.x_min)))
            if str(gun_tahmin) in self.vakitler_sozluk and self.vakitler_sozluk[str(gun_tahmin)]:
                gx = self._to_screen(gun_tahmin, self.y_min, rect).x()
                if rect.left() <= gx <= rect.right():
                    p.setPen(QtGui.QPen(QtGui.QColor(148, 163, 184, 160), 1))
                    p.drawLine(QPointF(gx, rect.top()), QPointF(gx, rect.bottom()))

                gun_veri = self.vakitler_sozluk[str(gun_tahmin)]
                ay_adi = datetime.datetime.now().strftime("%B")
                satirlar = [f"{gun_tahmin} {ay_adi}"]
                for k in keys_to_draw:
                    v = gun_veri.get(k)
                    if v:
                        satirlar.append(f"{VAKIT_KEY_TO_AD[k]}: {v[0]}:{v[1]}")

                p.setFont(QtGui.QFont("TRT Medium", 9))
                fm = p.fontMetrics()
                box_w = max(fm.horizontalAdvance(s) for s in satirlar) + 18
                box_h = len(satirlar) * 18 + 12
                bx = self._hover_pos.x() + 14
                by = self._hover_pos.y() - box_h // 2
                if bx + box_w > rect.right():
                    bx = self._hover_pos.x() - box_w - 14
                by = max(rect.top() + 4, min(by, rect.bottom() - box_h - 4))

                tip_rect = QRectF(bx, by, box_w, box_h)
                tip_bg = QtGui.QColor(20, 24, 32, 235) if self.dark_mode else QtGui.QColor(255, 255, 255, 240)
                tip_border = QtGui.QColor("#475569") if self.dark_mode else QtGui.QColor("#94a3b8")
                p.setBrush(tip_bg)
                p.setPen(QtGui.QPen(tip_border, 1))
                p.drawRoundedRect(tip_rect, 6, 6)

                y_txt = by + 17
                for idx, satir in enumerate(satirlar):
                    if idx == 0:
                        p.setPen(QtGui.QColor("#f8fafc") if self.dark_mode else QtGui.QColor("#0f172a"))
                    else:
                        k = keys_to_draw[idx - 1]
                        p.setPen(self.RENKLER[k] if self.dark_mode else self.RENKLER[k].darker(130))
                    p.drawText(QPointF(bx + 9, y_txt), satir)
                    y_txt += 18

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._panning = True
            self._pan_start = event.pos()
            self._pan_bounds = (self.x_min, self.x_max, self.y_min, self.y_max)
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        self._hover_pos = event.pos()
        if self._panning:
            rect = self._plot_rect()
            dx_px = event.pos().x() - self._pan_start.x()
            dy_px = event.pos().y() - self._pan_start.y()
            ox0, ox1, oy0, oy1 = self._pan_bounds
            dx = -dx_px / rect.width() * (ox1 - ox0)
            dy = dy_px / rect.height() * (oy1 - oy0)
            self.x_min, self.x_max = ox0 + dx, ox1 + dx
            self.y_min, self.y_max = oy0 + dy, oy1 + dy
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._panning = False
            self.setCursor(Qt.OpenHandCursor)

    def leaveEvent(self, event):
        self._hover_pos = None
        self.update()

    def wheelEvent(self, event):
        rect = self._plot_rect()
        if not rect.contains(event.pos()):
            return
        delta = event.angleDelta().y()
        factor = 0.85 if delta > 0 else 1.18

        rx = (event.pos().x() - rect.left()) / rect.width()
        ry = (rect.bottom() - event.pos().y()) / rect.height()
        cx = self.x_min + rx * (self.x_max - self.x_min)
        cy = self.y_min + ry * (self.y_max - self.y_min)

        new_x_span = max(2.0, min(90.0, (self.x_max - self.x_min) * factor))
        new_y_span = max(5.0, min(1800.0, (self.y_max - self.y_min) * factor))

        mods = event.modifiers()
        if mods != Qt.ControlModifier:
            self.x_min = cx - rx * new_x_span
            self.x_max = self.x_min + new_x_span
        if mods != Qt.ShiftModifier:
            self.y_min = cy - ry * new_y_span
            self.y_max = self.y_min + new_y_span
        self.update()


class VakitGrafikDialog(QDialog):
    def __init__(self, sehir_adi, vakitler_sozluk, baslangic_key="all", dark_mode=False, parent=None):
        super().__init__(parent)
        ay_adi = datetime.datetime.now().strftime("%B %Y")
        self.setWindowTitle(f"Aylık Vakit Grafiği — {sehir_adi} ({ay_adi})")
        self.resize(780, 440)
        self.dark_mode = dark_mode

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        ust_bar = QHBoxLayout()
        ust_bar.setSpacing(6)

        self.filtre_btnler = {}
        secenekler = [
            ("all", "Tümü"), ("ims", "İmsak"), ("sab", "Güneş"),
            ("ogl", "Öğle"), ("iki", "İkindi"), ("aks", "Akşam"), ("yat", "Yatsı")
        ]
        for key, etiket in secenekler:
            btn = QPushButton(etiket, self)
            btn.setCheckable(True)
            btn.setFont(QtGui.QFont("TRT Medium", 9))
            btn.clicked.connect(lambda _checked, k=key: self._filtre_sec(k))
            self.filtre_btnler[key] = btn
            ust_bar.addWidget(btn)

        ust_bar.addStretch()

        self.sifirla_btn = QPushButton("Sıfırla", self)
        self.sifirla_btn.setFont(QtGui.QFont("TRT Medium", 9))
        ust_bar.addWidget(self.sifirla_btn)

        layout.addLayout(ust_bar)

        self.canvas = VakitGrafikCanvas(vakitler_sozluk, secili_key=baslangic_key, dark_mode=dark_mode, parent=self)
        self.sifirla_btn.clicked.connect(self.canvas.gorunumu_sifirla)
        layout.addWidget(self.canvas, 1)

        alt_bilgi = QLabel("Sol tık sürükle: Kaydır  |  Fare tekerleği: Yakınlaştır / Uzaklaştır  |  Kırmızı kesikli çizgi: Bugün", self)
        alt_bilgi.setFont(QtGui.QFont("TRT Medium", 8))
        alt_bilgi.setAlignment(Qt.AlignCenter)
        layout.addWidget(alt_bilgi)

        if dark_mode:
            self.setStyleSheet("""
                QDialog { background-color: #111318; color: #e5e7eb; }
                QLabel { color: #94a3b8; }
                QPushButton {
                    background-color: #1f242d; color: #cbd5e1;
                    border: 1px solid #303642; border-radius: 5px; padding: 4px 10px;
                }
                QPushButton:hover { background-color: #2b313e; }
                QPushButton:checked { background-color: #2563eb; color: #ffffff; border-color: #3b82f6; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background-color: #f8fafc; color: #0f172a; }
                QLabel { color: #475569; }
                QPushButton {
                    background-color: #e2e8f0; color: #0f172a;
                    border: 1px solid #cbd5e1; border-radius: 5px; padding: 4px 10px;
                }
                QPushButton:hover { background-color: #cbd5e1; }
                QPushButton:checked { background-color: #0d9488; color: #ffffff; border-color: #0f766e; }
            """)

        self._filtre_sec(baslangic_key if baslangic_key in self.filtre_btnler else "all")

    def _filtre_sec(self, key):
        for k, btn in self.filtre_btnler.items():
            btn.setChecked(k == key)
        self.canvas.filtre_degistir(key)


# --- Konum Seçme Penceresi ---
class Ui_KonumSecimEkrani(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 156)
        Form.setWindowTitle("Namaz Vakitleri | Konum Seçimi")
        Form.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:0.840909, y2:1, "
            "stop:0.460227 rgba(134, 207, 139, 255), stop:0.602273 rgba(86, 183, 159, 255), "
            "stop:0.761364 rgba(48, 153, 207, 255))"
        )

        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout = QtWidgets.QGridLayout()

        self.ulke = QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("TRT")
        font.setPointSize(11)
        self.ulke.setFont(font)
        self.ulke.setStyleSheet("background:transparent;")
        self.gridLayout.addWidget(self.ulke, 0, 0, 1, 1)

        self.ulke_adi = QtWidgets.QComboBox(Form)
        self.ulke_adi.setStyleSheet(
            "background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, "
            "fx:0.5, fy:0.5, stop:0.142045 rgba(200, 200, 200, 255))"
        )
        self.ulke_adi.setEnabled(False)
        self.gridLayout.addWidget(self.ulke_adi, 0, 1, 1, 2)

        self.sehir = QLabel(Form)
        self.sehir.setFont(font)
        self.sehir.setStyleSheet("background:transparent;")
        self.gridLayout.addWidget(self.sehir, 1, 0, 1, 1)

        self.sehir_adi = QtWidgets.QComboBox(Form)
        self.sehir_adi.setStyleSheet(
            "background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, "
            "fx:0.5, fy:0.5, stop:0.142045 rgba(200, 200, 200, 255))"
        )
        self.gridLayout.addWidget(self.sehir_adi, 1, 1, 1, 2)

        self.konum_sec_button = QPushButton(Form)
        self.konum_sec_button.setFont(font)
        self.konum_sec_button.setStyleSheet(
            "background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, "
            "fx:0.5, fy:0.5, stop:0.142045 rgba(200, 200, 200, 255))"
        )
        self.gridLayout.addWidget(self.konum_sec_button, 4, 0, 1, 3)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.ulke.setText(_translate("Form", '<html><head/><body><p align="right">Ülke:</p></body></html>'))
        self.sehir.setText(_translate("Form", '<html><head/><body><p align="right">Şehir:</p></body></html>'))
        self.konum_sec_button.setText(_translate("Form", "Seç"))


class KonumSecimDialog(QDialog):
    konumSecildi = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_KonumSecimEkrani()
        self.ui.setupUi(self)
        self.sehir_data = {
            "Adana": "adana", "Adıyaman": "adiyaman", "Afyonkarahisar": "afyonkarahisar", "Ağrı": "agri",
            "Amasya": "amasya", "'Ankara": "ankara", "Antalya": "antalya", "Artvin": "artvin", "Aydın": "aydin",
            "Balıkesir": "balikesir", "Bilecik": "bilecik", "Bingöl": "bingol", "Bitlis": "bitlis", "Bolu": "bolu",
            "Burdur": "burdur", "Bursa": "bursa", "Çanakkale": "canakkale", "Çankırı": "cankiri", "'Çorum": "corum",
            "Denizli": "denizli", "Diyarbakır": "diyarbakir", "Edirne": "edirne", "Elazığ": "elazig",
            "Erzincan": "erzincan", "Erzurum": "erzurum", "Eskişehir": "eskisehir", "Gaziantep": "gaziantep",
            "Giresun": "giresun", "Gümüşhane": "gumushane", "Hakkari": "hakkari", "Hatay": "hatay",
            "Isparta": "isparta", "Mersin": "mersin", "İstanbul": "istanbul", "İzmir": "izmir", "Kars": "kars",
            "Kastamonu": "kastamonu", "Kayseri": "kayseri", "Kırklareli": "kirklareli", "Kırşehir": "kirsehir",
            "Kocaeli": "kocaeli", "Konya": "konya", "Kütahya": "kutahya", "Malatya": "malatya", "Leuven": "leuven",
            "Manisa": "manisa", "Kahramanmaraş": "kahramanmaras", "Mardin": "mardin", "Muğla": "mugla", "Muş": "mus",
            "Nevşehir": "nevsehir", "'Niğde": "nigde", "Ordu": "ordu", "Rize": "rize", "Sakarya": "sakarya",
            "Samsun": "samsun", "Siirt": "siirt", "Sinop": "sinop", "Sivas": "sivas", "Tekirdağ": "tekirdag",
            "Tokat": "tokat", "Trabzon": "trabzon", "Tunceli": "tunceli", "Şanlıurfa": "sanliurfa", "Uşak": "usak",
            "Van": "van", "Yozgat": "yozgat", "Zonguldak": "zonguldak", "Aksaray": "aksaray", "Bayburt": "bayburt",
            "Karaman": "karaman", "Kırıkkale": "kirikkale", "Batman": "batman", "Şırnak": "sirnak", "Bartın": "bartin",
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


# --- Ana Pencerenin Arayüzü ---
class Ui_AnaPencere(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 250)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        Form.setFont(font)
        try:
            Form.setWindowIcon(QtGui.QIcon('cami_ikonu.png'))
        except Exception:
            print("Uyarı: 'cami_ikonu.png' bulunamadı.")

        self.main_layout = QtWidgets.QVBoxLayout(Form)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.background_frame = QFrame(Form)
        self.background_frame.setObjectName("background_frame")
        self.background_frame.setStyleSheet("QFrame#background_frame { border-radius: 10px; }")
        self.main_layout.addWidget(self.background_frame)

        layout = QtWidgets.QVBoxLayout(self.background_frame)

        # Başlık Çubuğu ve Butonlar
        self.title_bar_layout = QtWidgets.QHBoxLayout()
        self.title_bar_layout.setContentsMargins(10, 5, 10, 0)
        self.title_bar_layout.setSpacing(5)

        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.title_bar_layout.addItem(spacer)

        # Hadis Göster/Gizle Butonu
        self.hadisButton = QPushButton("❝", self.background_frame)
        self.hadisButton.setFixedSize(20, 20)
        self.hadisButton.setStyleSheet(
            "QPushButton { background-color: #38bdf8; color: #0f172a; border-radius: 10px; border: 1px solid #0284c7; font-weight: bold; } "
            "QPushButton:hover { background-color: #7dd3fc; }"
        )
        self.hadisButton.setToolTip("Hadis Satırını Aç / Kapat")
        self.title_bar_layout.addWidget(self.hadisButton)

        # Tema Seçici Butonu
        self.temaButton = QPushButton("◈", self.background_frame)
        self.temaButton.setFixedSize(20, 20)
        self.temaButton.setStyleSheet(
            "QPushButton { background-color: #a78bfa; color: #0f172a; border-radius: 10px; border: 1px solid #7c3aed; font-weight: bold; } "
            "QPushButton:hover { background-color: #c4b5fd; }"
        )
        self.temaButton.setToolTip("Arka Plan Teması Seç")
        self.title_bar_layout.addWidget(self.temaButton)

        # Karanlık Tema Butonu
        self.darkModeButton = QPushButton("☾", self.background_frame)
        self.darkModeButton.setFixedSize(20, 20)
        self.darkModeButton.setStyleSheet(
            "QPushButton { background-color: #334155; color: #f8fafc; border-radius: 10px; border: 1px solid #1e293b; font-weight: bold; } "
            "QPushButton:hover { background-color: #475569; }"
        )
        self.darkModeButton.setToolTip("Karanlık Tema Aç / Kapat")
        self.title_bar_layout.addWidget(self.darkModeButton)

        self.pinButton = QPushButton("📌", self.background_frame)
        self.pinButton.setFixedSize(20, 20)
        self.pinButton.setStyleSheet(
            "QPushButton { background-color: #34d399; border-radius: 10px; border: 1px solid #2b9e76; } "
            "QPushButton:hover { background-color: #6ee7b7; }"
        )
        self.pinButton.setToolTip("Kompakt Görünüme Geç / Sabitle")
        self.title_bar_layout.addWidget(self.pinButton)

        self.minimizeButton = QPushButton("−", self.background_frame)
        self.minimizeButton.setFixedSize(20, 20)
        self.minimizeButton.setStyleSheet(
            "QPushButton { background-color: #fbbd23; border-radius: 10px; border: 1px solid #f4a12e; font-weight: bold; } "
            "QPushButton:hover { background-color: #fccf4b; }"
        )
        self.minimizeButton.setToolTip("Simge Durumuna Küçült")
        self.title_bar_layout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton("×", self.background_frame)
        self.closeButton.setFixedSize(20, 20)
        self.closeButton.setStyleSheet(
            "QPushButton { background-color: #f87171; border-radius: 10px; border: 1px solid #dc2626; font-weight: bold; } "
            "QPushButton:hover { background-color: #fca5a5; }"
        )
        self.closeButton.setToolTip("Kapat")
        self.title_bar_layout.addWidget(self.closeButton)

        layout.addLayout(self.title_bar_layout)

        # İçerik Alanı
        content_layout = QtWidgets.QVBoxLayout()
        header_layout = QtWidgets.QHBoxLayout()

        self.lab_namaz_vakitleri = QLabel()
        self.lab_namaz_vakitleri.setStyleSheet('background: transparent; font: 24pt "TRT Medium Italic";')
        self.lab_namaz_vakitleri.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.lab_namaz_vakitleri)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Plain)
        header_layout.addWidget(self.line_2)

        self.lab_tarih = QLabel()
        self.lab_tarih.setStyleSheet('background: transparent; font: 20pt "TRT Medium";')
        self.lab_tarih.setCursor(Qt.PointingHandCursor)
        self.lab_tarih.setToolTip("Hicri / Miladi tarih geçişi için tıklayın")
        header_layout.addWidget(self.lab_tarih)
        content_layout.addLayout(header_layout)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Plain)
        content_layout.addWidget(self.line)

        vakit_row_layout = QtWidgets.QHBoxLayout()
        self.v_lines = []

        def create_vakit_layout(name, parent):
            v_layout = QtWidgets.QVBoxLayout()
            baslik = QLabel(f"{name.capitalize()}", parent, font=QtGui.QFont("TRT Bold", 16))
            baslik.setAlignment(Qt.AlignCenter)
            baslik.setToolTip("Anımsatıcı eklemek için sağ tıklayın")
            vakit = QLabel("--:--", parent, font=QtGui.QFont("Open Sans Light", 16))
            vakit.setAlignment(Qt.AlignCenter)
            vakit.setToolTip("Aylık grafik için sağ tıklayın")
            v_layout.addWidget(baslik)
            v_layout.addWidget(vakit)
            return v_layout, baslik, vakit

        layouts = {}
        for name in ["imsak", "sabah", "ogle", "ikindi", "aksam", "yatsi"]:
            layouts[name] = create_vakit_layout(name, self.background_frame)
            vakit_row_layout.addLayout(layouts[name][0])
            if name != "yatsi":
                line_v = QFrame()
                line_v.setFrameShape(QFrame.VLine)
                line_v.setFrameShadow(QFrame.Plain)
                self.v_lines.append(line_v)
                vakit_row_layout.addWidget(line_v)

        self.imsak, self.imsak_vakti = layouts["imsak"][1], layouts["imsak"][2]
        self.sabah, self.sabah_vakti = layouts["sabah"][1], layouts["sabah"][2]
        self.ogle, self.ogle_vakti = layouts["ogle"][1], layouts["ogle"][2]
        self.ikindi, self.ikindi_vakti = layouts["ikindi"][1], layouts["ikindi"][2]
        self.aksam, self.aksam_vakti = layouts["aksam"][1], layouts["aksam"][2]
        self.yatsi, self.yatsi_vakti = layouts["yatsi"][1], layouts["yatsi"][2]

        self.imsak.setText("İmsak")
        self.sabah.setText("Sabah")
        self.ogle.setText("Öğle")
        self.ikindi.setText("İkindi")
        self.aksam.setText("Akşam")
        self.yatsi.setText("Yatsı")

        content_layout.addLayout(vakit_row_layout)
        timer_layout = QtWidgets.QHBoxLayout()

        self.lab_vaktin_cikmasina = QLabel()
        self.lab_vaktin_cikmasina.setStyleSheet('font: 20pt "TRT Bold"; background: transparent;')
        timer_layout.addWidget(self.lab_vaktin_cikmasina)

        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setEnabled(False)
        self.time_edit.setStyleSheet('font: 35pt "TRT Bold"; background: transparent;')
        self.time_edit.setFrame(False)
        self.time_edit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        timer_layout.addWidget(self.time_edit)

        layout.addLayout(content_layout)
        layout.addLayout(timer_layout)

        # En altta tam genişlikte Hadis satırı (sütunları birleşik alt satır)
        self.hadis_container = QWidget(self.background_frame)
        self.hadis_container.setStyleSheet("background: transparent;")
        hadis_layout = QVBoxLayout(self.hadis_container)
        hadis_layout.setContentsMargins(6, 2, 6, 4)
        hadis_layout.setSpacing(4)

        self.hadis_line = QFrame(self.hadis_container)
        self.hadis_line.setFrameShape(QFrame.HLine)
        self.hadis_line.setFrameShadow(QFrame.Plain)
        hadis_layout.addWidget(self.hadis_line)

        self.lab_hadis = QLabel(self.hadis_container)
        self.lab_hadis.setWordWrap(True)
        self.lab_hadis.setAlignment(Qt.AlignCenter)
        self.lab_hadis.setCursor(Qt.PointingHandCursor)
        self.lab_hadis.setToolTip("Yeni bir hadis görmek için tıklayın")
        self.lab_hadis.setStyleSheet('background: transparent; font: italic 10pt "TRT Medium"; padding: 2px 6px;')
        hadis_layout.addWidget(self.lab_hadis)

        self.hadis_container.setVisible(False)
        layout.addWidget(self.hadis_container)

    def retranslateUi(self, Form, parent_app):
        an = datetime.datetime.now()
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Namaz Vakitleri"))
        self.time_edit.setDisplayFormat(_translate("Form", "HH:mm:ss"))
        self.lab_vaktin_cikmasina.setText(_translate("Form", "Vaktin Çıkmasına:"))

        display_name = parent_app.konum_penceresi.get_sehir_display_name(parent_app.sehir_id)
        self.lab_namaz_vakitleri.setText(_translate("Form", f"<html><head/><body><p>{display_name}</p></body></html>"))

        if parent_app.hicri_goster:
            tarih_str = hicri_tarih_metni(an)
        else:
            tarih_str = parent_app.tarih_ne('%d %B %A')
        self.lab_tarih.setText(_translate("Form", f'<html><head/><body><p align="center">{tarih_str}</p></body></html>'))

        # Tüm başlıkları sıfırla (yatsı kaydırması sonrası gece yarısı düzeltmesi)
        self.imsak.setText("İmsak")
        self.sabah.setText("Güneş")
        self.ogle.setText("Öğle")
        self.ikindi.setText("İkindi")
        self.aksam.setText("Akşam")
        self.yatsi.setText("Yatsı")

        sozluk = parent_app.vakitler_sozluk
        gun_str = str(an.day)
        if sozluk and gun_str in sozluk and "ims" in sozluk[gun_str]:
            gunlu = sozluk[gun_str]
            self.imsak_vakti.setText(f'{gunlu["ims"][0]}:{gunlu["ims"][1]}')
            self.sabah_vakti.setText(f'{gunlu["sab"][0]}:{gunlu["sab"][1]}')
            self.ogle_vakti.setText(f'{gunlu["ogl"][0]}:{gunlu["ogl"][1]}')
            self.ikindi_vakti.setText(f'{gunlu["iki"][0]}:{gunlu["iki"][1]}')
            self.aksam_vakti.setText(f'{gunlu["aks"][0]}:{gunlu["aks"][1]}')
            self.yatsi_vakti.setText(f'{gunlu["yat"][0]}:{gunlu["yat"][1]}')
        else:
            for vakit_label in [
                self.imsak_vakti, self.sabah_vakti, self.ogle_vakti,
                self.ikindi_vakti, self.aksam_vakti, self.yatsi_vakti
            ]:
                vakit_label.setText("--:--")


# --- Ana Pencerenin İşleyişi ---
class AnaPencere(QWidget):
    CONFIG_FILE = "last_location.cfg"
    SETTINGS_FILE = "ayarlar.json"
    REMINDERS_FILE = "animsaticilar.json"
    HADIS_FILE = "hadisler.json"

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragPos = QPoint()

        self.ui = Ui_AnaPencere()
        self.ui.setupUi(self)

        # Ayarlar, anımsatıcılar ve hadis veri tabanını yükle
        self.dark_mode = False
        self.tema = "varsayilan"
        self.ozel_gun_tema = True
        self.hadis_goster = False
        self.hicri_goster = False
        self.ayarlari_yukle()

        self.animsaticilar = {}
        self.animsaticilari_yukle()
        self.gonderilen_tek_bildirimler = set()

        self.hadisler = []
        self.hadisleri_yukle()
        self.rastgele_hadis_goster()

        # Kompakt pencereyi oluştur ve sinyallerini bağla
        self.kompakt_pencere = KompaktPencere()
        self.kompakt_pencere.tamGorunumeGecSignal.connect(self.goster_ana_pencere)
        self.kompakt_pencere.uygulamayiKapatSignal.connect(self.close)

        # Second layer anımsatıcı katmanı
        self.animsatici_katmani = AnimsaticiKatmani(self, self.ui.background_frame)

        # Değişkenlerin başlangıç değerleri
        self.konum_basariyla_yuklendi = True
        self.simdiki_vakit_adi = "shezmI"
        self.vakitler_sozluk = {}
        self.window_minimized = False
        self.hedef_zaman = None
        self.hesaplanan_gun = None
        self.hesaplanan_ay = None

        # Sınıfların örnekleri
        self.konum_penceresi = KonumSecimDialog(self)
        self.toaster = ToastNotifier() if ToastNotifier else None

        # Buton bağlantıları
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.minimizeButton.clicked.connect(self.showMinimized)
        self.ui.pinButton.clicked.connect(self.goster_kompakt_pencere)
        self.ui.darkModeButton.clicked.connect(self.karanlik_tema_degistir)
        self.ui.temaButton.clicked.connect(self.tema_menusu_ac)
        self.ui.hadisButton.clicked.connect(self.hadis_satiri_degistir)

        # Başlangıç fonksiyonları
        self.load_last_location()
        if not self.konum_basariyla_yuklendi:
            return

        # Event filter bağlantıları
        self.ui.lab_namaz_vakitleri.installEventFilter(self)
        self.ui.lab_tarih.installEventFilter(self)
        self.ui.lab_hadis.installEventFilter(self)

        self.vakit_baslik_list = [
            self.ui.imsak, self.ui.sabah, self.ui.ogle,
            self.ui.ikindi, self.ui.aksam, self.ui.yatsi
        ]
        self.vakit_saat_list = [
            self.ui.imsak_vakti, self.ui.sabah_vakti, self.ui.ogle_vakti,
            self.ui.ikindi_vakti, self.ui.aksam_vakti, self.ui.yatsi_vakti
        ]
        for lbl in self.vakit_baslik_list + self.vakit_saat_list:
            lbl.installEventFilter(self)

        self.konum_penceresi.konumSecildi.connect(self.konumuGuncelle)

        # Hadis görünürlüğünü başlangıç ayarına göre uygula
        self._hadis_gorunurlugunu_uygula()

        self.en_son_ne_zaman_calisti()
        self.ui.retranslateUi(self, self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

        self.kac_dakka_var_hesapla()

    # --- Ayarlar, Anımsatıcılar ve Hadis Dosya Yönetimi ---
    def ayarlari_yukle(self):
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.dark_mode = bool(data.get("dark_mode", False))
                self.tema = data.get("tema", "varsayilan")
                self.ozel_gun_tema = bool(data.get("ozel_gun_tema", True))
                self.hadis_goster = bool(data.get("hadis_goster", False))
                self.hicri_goster = bool(data.get("hicri_goster", False))
            except Exception as e:
                print(f"Ayarlar yüklenirken hata: {e}")

    def ayarlari_kaydet(self):
        data = {
            "dark_mode": self.dark_mode,
            "tema": self.tema,
            "ozel_gun_tema": self.ozel_gun_tema,
            "hadis_goster": self.hadis_goster,
            "hicri_goster": self.hicri_goster
        }
        try:
            with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ayarlar kaydedilirken hata: {e}")

    def animsaticilari_yukle(self):
        if os.path.exists(self.REMINDERS_FILE):
            try:
                with open(self.REMINDERS_FILE, "r", encoding="utf-8") as f:
                    self.animsaticilar = json.load(f)
                return
            except Exception as e:
                print(f"Anımsatıcılar yüklenirken hata: {e}")
        self.animsaticilar = json.loads(json.dumps(VARSAYILAN_ANIMSATICILAR))
        self.animsaticilari_kaydet()

    def animsaticilari_kaydet(self):
        try:
            with open(self.REMINDERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.animsaticilar, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Anımsatıcılar kaydedilirken hata: {e}")

    def hadisleri_yukle(self):
        if not os.path.exists(self.HADIS_FILE):
            try:
                with open(self.HADIS_FILE, "w", encoding="utf-8") as f:
                    json.dump(VARSAYILAN_HADISLER, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Hadis dosyası oluşturulamadı: {e}")
        try:
            with open(self.HADIS_FILE, "r", encoding="utf-8") as f:
                yuklenen = json.load(f)
            if isinstance(yuklenen, list) and yuklenen:
                self.hadisler = yuklenen
                return
        except Exception as e:
            print(f"Hadisler yüklenirken hata: {e}")
        self.hadisler = list(VARSAYILAN_HADISLER)

    def rastgele_hadis_goster(self):
        if not self.hadisler:
            return
        secilen = random.choice(self.hadisler)
        if isinstance(secilen, dict):
            metin = secilen.get("metin", "")
            kaynak = secilen.get("kaynak", "")
            yazi = f'"{metin}"  — {kaynak}' if kaynak else f'"{metin}"'
        else:
            yazi = f'"{secilen}"'
        self.ui.lab_hadis.setText(yazi)

    # --- Tema, Karanlık Mod ve Hadis Kontrolleri ---
    def karanlik_tema_degistir(self):
        self.dark_mode = not self.dark_mode
        self.ayarlari_kaydet()
        self.kac_dakka_var_hesapla()
        if self.animsatici_katmani.isVisible():
            self.animsatici_katmani.tema_uygula(self.dark_mode)

    def tema_menusu_ac(self):
        menu = QMenu(self)
        if self.dark_mode:
            menu.setStyleSheet(
                "QMenu { background-color: #181b20; color: #e5e7eb; border: 1px solid #303642; padding: 4px; } "
                "QMenu::item:selected { background-color: #2563eb; }"
            )

        temalar = [
            ("varsayilan", "Varsayılan (Gündüz / Gece)"),
            ("gunese_bagli", "Güneşe Bağlı (Vakitlere Göre)"),
            ("zumrut", "Zümrüt"),
            ("gece_mavisi", "Gece Mavisi"),
            ("gun_batimi", "Gün Batımı"),
        ]
        for tema_id, etiket in temalar:
            act = QAction(etiket, menu)
            act.setCheckable(True)
            act.setChecked(self.tema == tema_id)
            act.triggered.connect(lambda _c, t=tema_id: self.tema_sec(t))
            menu.addAction(act)

        menu.addSeparator()
        ozel_act = QAction("Özel Gün Teması (Otomatik)", menu)
        ozel_act.setCheckable(True)
        ozel_act.setChecked(self.ozel_gun_tema)
        ozel_act.triggered.connect(self.ozel_gun_tema_degistir)
        menu.addAction(ozel_act)

        pos = self.ui.temaButton.mapToGlobal(QPoint(0, self.ui.temaButton.height() + 4))
        menu.exec_(pos)

    def tema_sec(self, yeni_tema):
        self.tema = yeni_tema
        self.ayarlari_kaydet()
        self.kac_dakka_var_hesapla()

    def ozel_gun_tema_degistir(self):
        self.ozel_gun_tema = not self.ozel_gun_tema
        self.ayarlari_kaydet()
        self.kac_dakka_var_hesapla()

    def hadis_satiri_degistir(self):
        self.hadis_goster = not self.hadis_goster
        self.ayarlari_kaydet()
        self._hadis_gorunurlugunu_uygula()

    def _hadis_gorunurlugunu_uygula(self):
        self.ui.hadis_container.setVisible(self.hadis_goster)
        self.resize(self.width(), 305 if self.hadis_goster else 250)

    def _arkaplan_ve_stilleri_al(self, ozel_gun):
        border_radius_padding = "border-radius: 5px; padding: 3px;"

        # Karanlık tema aktifse
        if self.dark_mode:
            if ozel_gun and self.ozel_gun_tema:
                arkaplan = (
                    "QFrame#background_frame { "
                    "background: qradialgradient(spread:pad, cx:0.5, cy:0.4, radius:1.05, fx:0.1, fy:0.1, "
                    "stop:0 rgba(58, 43, 12, 252), stop:0.45 rgba(26, 22, 14, 254), stop:1 rgba(12, 13, 16, 255)); "
                    "border: 1px solid rgba(217, 164, 46, 130); border-radius: 10px; }"
                )
                aktif_b = f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a16207, stop:1 #713f12); color: #fefce8; {border_radius_padding}"
                aktif_v = f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #854d0e, stop:1 #422006); color: #fefce8; {border_radius_padding}"
            else:
                arkaplan = (
                    "QFrame#background_frame { "
                    "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
                    "stop:0 rgba(22, 25, 31, 252), stop:1 rgba(11, 13, 17, 255)); "
                    "border: 1px solid rgba(55, 65, 81, 160); border-radius: 10px; }"
                )
                aktif_b = f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #991b1b, stop:1 #450a0a); color: #f8fafc; {border_radius_padding}"
                aktif_v = f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7f1d1d, stop:1 #3b0712); color: #f8fafc; {border_radius_padding}"

            gecmis_b = f"background-color: #1a1e26; color: #64748b; {border_radius_padding}"
            gecmis_v = f"background-color: #161920; color: #64748b; {border_radius_padding}"
            normal_b = f"background-color: #212631; color: #e2e8f0; {border_radius_padding}"
            normal_v = f"background-color: #1c2029; color: #cbd5e1; {border_radius_padding}"
            return arkaplan, gecmis_b, gecmis_v, aktif_b, aktif_v, normal_b, normal_v

        # Açık (orijinal) kutu stilleri
        gecmis_b = f"background:qlineargradient(spread:pad, x1:0.858, y1:0.1535, x2:0.045, y2:1, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255)); {border_radius_padding}"
        gecmis_v = f"background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0.397727 rgba(22, 90, 173, 255), stop:0.721591 rgba(124, 131, 116, 255)); {border_radius_padding}"
        aktif_b = f"background:qradialgradient(spread:pad, cx:1, cy:0, radius:2, fx:1, fy:0, stop:0 rgba(118, 15, 15, 255), stop:0.193182 rgba(255, 31, 31, 255), stop:0.710227 rgba(24, 0, 165, 250)); color:rgb(227, 227, 227); {border_radius_padding}"
        aktif_v = f"background:qradialgradient(spread:pad, cx:1, cy:1, radius:2, fx:1, fy:1, stop:0 rgba(118, 15, 15, 255), stop:0.267045 rgba(255, 31, 31, 255), stop:0.704545 rgba(20, 1, 132, 250)); color:rgb(227, 227, 227); {border_radius_padding}"
        normal_b = f"background:qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0.318182 rgba(9, 127, 70, 248), stop:1 rgba(44, 171, 255, 255)); {border_radius_padding}"
        normal_v = f"background:qlineargradient(spread:pad, x1:0, y1:0, x2:0.949, y2:0.960591, stop:0.0397727 rgba(39, 210, 255, 255), stop:0.431818 rgba(0, 108, 108, 255)); {border_radius_padding}"

        # Özel gün teması (Altın sarısına yakın geçişli arka plan)
        if ozel_gun and self.ozel_gun_tema:
            if self.simdiki_vakit_adi in ["Akşam", "Yatsı"]:
                arkaplan = (
                    "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.583, cy:0.602881, "
                    "radius:0.971914, fx:0.006, fy:0.0181152, stop:0.0431548 rgba(120, 84, 8, 253), "
                    "stop:0.22 rgba(168, 124, 18, 248), stop:0.48 rgba(204, 158, 36, 245), "
                    "stop:0.85 rgba(38, 26, 6, 255)); border-radius: 10px; }"
                )
            else:
                arkaplan = (
                    "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.55, cy:0.55, "
                    "radius:1.0, fx:0.05, fy:0.05, stop:0.08 rgba(185, 138, 18, 252), "
                    "stop:0.35 rgba(224, 178, 44, 248), stop:0.65 rgba(154, 112, 16, 248), "
                    "stop:1 rgba(48, 34, 8, 255)); border-radius: 10px; }"
                )
            return arkaplan, gecmis_b, gecmis_v, aktif_b, aktif_v, normal_b, normal_v

        # Seçilebilir arka plan temaları
        if self.tema == "gunese_bagli":
            vakit_arkaplanlari = {
                "İmsak": (
                    "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.5, cy:0.6, radius:1.0, "
                    "fx:0.1, fy:0.1, stop:0.1 rgba(30, 27, 75, 252), stop:0.45 rgba(55, 48, 138, 248), "
                    "stop:1 rgba(10, 12, 28, 255)); border-radius: 10px; }"
                ),
                "Güneş": (
                    "QFrame#background_frame { background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, "
                    "stop:0 rgba(217, 119, 6, 248), stop:0.45 rgba(245, 158, 11, 242), "
                    "stop:0.8 rgba(56, 130, 180, 245), stop:1 rgba(23, 55, 94, 255)); border-radius: 10px; }"
                ),
                "Öğle": (
                    "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.5, cy:0.3, radius:1.05, "
                    "fx:0.5, fy:0.05, stop:0.1 rgba(56, 189, 248, 248), stop:0.5 rgba(14, 116, 144, 248), "
                    "stop:1 rgba(12, 42, 68, 255)); border-radius: 10px; }"
                ),
                "İkindi": (
                    "QFrame#background_frame { background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
                    "stop:0 rgba(202, 138, 4, 248), stop:0.5 rgba(180, 83, 9, 248), "
                    "stop:1 rgba(45, 24, 16, 255)); border-radius: 10px; }"
                ),
                "Akşam": (
                    "QFrame#background_frame { background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
                    "stop:0 rgba(159, 18, 57, 250), stop:0.45 rgba(107, 33, 168, 248), "
                    "stop:1 rgba(17, 12, 34, 255)); border-radius: 10px; }"
                ),
                "Yatsı": (
                    "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.55, cy:0.6, radius:0.98, "
                    "fx:0.05, fy:0.05, stop:0.08 rgba(15, 23, 66, 253), stop:0.4 rgba(30, 41, 115, 248), "
                    "stop:0.85 rgba(3, 7, 18, 255)); border-radius: 10px; }"
                ),
            }
            arkaplan = vakit_arkaplanlari.get(self.simdiki_vakit_adi, vakit_arkaplanlari["Öğle"])
        elif self.tema == "zumrut":
            arkaplan = (
                "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.0, "
                "fx:0.1, fy:0.1, stop:0.1 rgba(6, 95, 70, 250), stop:0.45 rgba(16, 148, 108, 248), "
                "stop:1 rgba(4, 28, 24, 255)); border-radius: 10px; }"
            )
        elif self.tema == "gece_mavisi":
            arkaplan = (
                "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.0, "
                "fx:0.1, fy:0.1, stop:0.1 rgba(15, 42, 96, 252), stop:0.45 rgba(29, 78, 168, 248), "
                "stop:1 rgba(6, 14, 32, 255)); border-radius: 10px; }"
            )
        elif self.tema == "gun_batimi":
            arkaplan = (
                "QFrame#background_frame { background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
                "stop:0 rgba(190, 75, 55, 248), stop:0.5 rgba(126, 34, 92, 248), "
                "stop:1 rgba(24, 14, 34, 255)); border-radius: 10px; }"
            )
        else:
            # Orijinal varsayılan gündüz / gece arka planı
            arkaplan_gunduz = (
                "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1.018, "
                "fx:0, fy:0.014, stop:0.15894 rgba(5, 82, 45, 248), stop:0.318182 rgba(9, 127, 70, 248), "
                "stop:1 rgba(3, 12, 18, 255)); border-radius: 10px; }"
            )
            arkaplan_gece = (
                "QFrame#background_frame { background:qradialgradient(spread:pad, cx:0.583, cy:0.602881, "
                "radius:0.971914, fx:0.006, fy:0.0181152, stop:0.0431548 rgba(18, 25, 85, 253), "
                "stop:0.169643 rgba(29, 38, 198, 248), stop:0.375 rgba(57, 60, 255, 248), "
                "stop:0.770833 rgba(3, 12, 18, 255)); border-radius: 10px; }"
            )
            arkaplan = arkaplan_gece if self.simdiki_vakit_adi in ["Akşam", "Yatsı"] else arkaplan_gunduz

        return arkaplan, gecmis_b, gecmis_v, aktif_b, aktif_v, normal_b, normal_v

    def _yazi_ve_cizgi_stillerini_uygula(self, ozel_gun):
        if self.dark_mode:
            text_color = "#f3f4f6"
            sub_color = "#cbd5e1"
            line_style = "color: #2d3340;"
            self.ui.darkModeButton.setText("☀")
            self.ui.darkModeButton.setStyleSheet(
                "QPushButton { background-color: #f59e0b; color: #0f172a; border-radius: 10px; border: 1px solid #d97706; font-weight: bold; } "
                "QPushButton:hover { background-color: #fbbf24; }"
            )
        else:
            text_color = ""
            sub_color = "#0f172a" if (ozel_gun and self.ozel_gun_tema) else "#e5e7eb"
            line_style = ""
            self.ui.darkModeButton.setText("☾")
            self.ui.darkModeButton.setStyleSheet(
                "QPushButton { background-color: #334155; color: #f8fafc; border-radius: 10px; border: 1px solid #1e293b; font-weight: bold; } "
                "QPushButton:hover { background-color: #475569; }"
            )

        color_css = f" color: {text_color};" if text_color else ""
        self.ui.lab_namaz_vakitleri.setStyleSheet(f'background: transparent; font: 24pt "TRT Medium Italic";{color_css}')
        self.ui.lab_tarih.setStyleSheet(f'background: transparent; font: 20pt "TRT Medium";{color_css}')
        self.ui.lab_vaktin_cikmasina.setStyleSheet(f'font: 20pt "TRT Bold"; background: transparent;{color_css}')
        self.ui.time_edit.setStyleSheet(f'font: 35pt "TRT Bold"; background: transparent;{color_css}')
        self.ui.lab_hadis.setStyleSheet(f'background: transparent; font: italic 10pt "TRT Medium"; padding: 2px 6px; color: {sub_color};')

        for ln in [self.ui.line, self.ui.line_2, self.ui.hadis_line] + self.ui.v_lines:
            ln.setStyleSheet(line_style)

    # --- Pencere Değiştirme Mantığı ---
    def goster_kompakt_pencere(self):
        self.kompakt_pencere.move(self.pos())
        self.kompakt_pencere.show()
        self.hide()

    def goster_ana_pencere(self):
        self.move(self.kompakt_pencere.pos())
        self.show()
        self.kompakt_pencere.hide()

    def closeEvent(self, event):
        self.kompakt_pencere.close()
        super().closeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "animsatici_katmani") and self.animsatici_katmani.isVisible():
            self.animsatici_katmani.setGeometry(self.ui.background_frame.rect())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.animsatici_katmani.isVisible():
            self.animsatici_katmani.hide()
            return
        super().keyPressEvent(event)

    # --- Ana Hesaplama Fonksiyonu ---
    def kac_dakka_var_hesapla(self):
        an = datetime.datetime.now()
        self.hesaplanan_gun = an.date()
        self.hesaplanan_ay = (an.year, an.month)
        self.gonderilen_tek_bildirimler.clear()

        self.ui.retranslateUi(self, self)

        all_widgets = self.vakit_baslik_list
        all_vakit_widgets = self.vakit_saat_list

        gun_str = str(an.day)
        if not self.vakitler_sozluk or gun_str not in self.vakitler_sozluk or not self.vakitler_sozluk[gun_str]:
            self.ui.lab_vaktin_cikmasina.setText("Veri bekleniyor...")
            self.hedef_zaman = None
            return

        gunun_verileri = self.vakitler_sozluk[gun_str]
        toplam_saniye = an.hour * 3600 + an.minute * 60 + an.second

        try:
            vakit_saniyeleri = {k: int(v[0]) * 3600 + int(v[1]) * 60 for k, v in gunun_verileri.items()}
        except (ValueError, TypeError, KeyError):
            self.ui.lab_vaktin_cikmasina.setText("Hatalı veri...")
            self.hedef_zaman = None
            return

        # Şimdiki vakti belirle (özel gün ve tema hesabı için önce belirlenir)
        if toplam_saniye < vakit_saniyeleri["ims"]:
            self.simdiki_vakit_adi = "Yatsı"
        elif toplam_saniye < vakit_saniyeleri["sab"]:
            self.simdiki_vakit_adi = "İmsak"
        elif toplam_saniye < vakit_saniyeleri["ogl"]:
            self.simdiki_vakit_adi = "Güneş"
        elif toplam_saniye < vakit_saniyeleri["iki"]:
            self.simdiki_vakit_adi = "Öğle"
        elif toplam_saniye < vakit_saniyeleri["aks"]:
            self.simdiki_vakit_adi = "İkindi"
        elif toplam_saniye < vakit_saniyeleri["yat"]:
            self.simdiki_vakit_adi = "Akşam"
        else:
            self.simdiki_vakit_adi = "Yatsı"

        aksam_sonrasi = toplam_saniye >= vakit_saniyeleri["aks"]
        ozel_gun = ozel_gun_bul(an, aksam_sonrasi=aksam_sonrasi)
        if ozel_gun:
            self.ui.lab_tarih.setToolTip(f"{ozel_gun} — Hicri / Miladi tarih geçişi için tıklayın")
        else:
            self.ui.lab_tarih.setToolTip("Hicri / Miladi tarih geçişi için tıklayın")

        (
            arkaplan_stili,
            stil_gecmis_baslik, stil_gecmis_vakit,
            stil_aktif_baslik, stil_aktif_vakit,
            stil_normal_baslik, stil_normal_vakit
        ) = self._arkaplan_ve_stilleri_al(ozel_gun)

        self.ui.background_frame.setStyleSheet(arkaplan_stili)
        self._yazi_ve_cizgi_stillerini_uygula(ozel_gun)

        for w in all_widgets:
            w.setStyleSheet(stil_normal_baslik)
        for w in all_vakit_widgets:
            w.setStyleSheet(stil_normal_vakit)

        self.aktif_stil_baslik, self.aktif_stil_vakit = stil_aktif_baslik, stil_aktif_vakit
        self.aktif_vakit_adi, self.aktif_vakit_saati = "", ""
        self.aktif_font_baslik, self.aktif_font_vakit = all_widgets[0].font(), all_vakit_widgets[0].font()

        def set_styles(aktif_index, aktif_vakit_adi_str, aktif_vakit_saati_str):
            self.aktif_vakit_adi = aktif_vakit_adi_str
            self.aktif_vakit_saati = aktif_vakit_saati_str
            for i in range(len(all_widgets)):
                if i < aktif_index:
                    all_widgets[i].setStyleSheet(stil_gecmis_baslik)
                    all_vakit_widgets[i].setStyleSheet(stil_gecmis_vakit)
                elif i == aktif_index:
                    all_widgets[i].setStyleSheet(stil_aktif_baslik)
                    all_vakit_widgets[i].setStyleSheet(stil_aktif_vakit)
                    self.aktif_stil_baslik = stil_aktif_baslik
                    self.aktif_stil_vakit = stil_aktif_vakit
                    self.aktif_font_baslik = all_widgets[i].font()
                    self.aktif_font_vakit = all_vakit_widgets[i].font()
                else:
                    all_widgets[i].setStyleSheet(stil_normal_baslik)
                    all_vakit_widgets[i].setStyleSheet(stil_normal_vakit)

        def hedef_dt_olustur(tarih_obj, vakit_pair):
            return datetime.datetime(
                tarih_obj.year, tarih_obj.month, tarih_obj.day,
                int(vakit_pair[0]), int(vakit_pair[1]), 0
            )

        ims_v = f'{gunun_verileri["ims"][0]}:{gunun_verileri["ims"][1]}'
        sab_v = f'{gunun_verileri["sab"][0]}:{gunun_verileri["sab"][1]}'
        ogl_v = f'{gunun_verileri["ogl"][0]}:{gunun_verileri["ogl"][1]}'
        iki_v = f'{gunun_verileri["iki"][0]}:{gunun_verileri["iki"][1]}'
        aks_v = f'{gunun_verileri["aks"][0]}:{gunun_verileri["aks"][1]}'
        yat_v = f'{gunun_verileri["yat"][0]}:{gunun_verileri["yat"][1]}'

        if toplam_saniye < vakit_saniyeleri["ims"]:
            sonraki_vakit_adi = "İmsak"
            self.hedef_zaman = hedef_dt_olustur(an, gunun_verileri["ims"])
            set_styles(-1, "Yatsı", "...")
        elif toplam_saniye < vakit_saniyeleri["sab"]:
            sonraki_vakit_adi = "Güneş"
            self.hedef_zaman = hedef_dt_olustur(an, gunun_verileri["sab"])
            set_styles(0, "İmsak", ims_v)
        elif toplam_saniye < vakit_saniyeleri["ogl"]:
            sonraki_vakit_adi = "Öğle"
            self.hedef_zaman = hedef_dt_olustur(an, gunun_verileri["ogl"])
            set_styles(1, "Güneş", sab_v)
        elif toplam_saniye < vakit_saniyeleri["iki"]:
            sonraki_vakit_adi = "İkindi"
            self.hedef_zaman = hedef_dt_olustur(an, gunun_verileri["iki"])
            set_styles(2, "Öğle", ogl_v)
        elif toplam_saniye < vakit_saniyeleri["aks"]:
            sonraki_vakit_adi = "Akşam"
            self.hedef_zaman = hedef_dt_olustur(an, gunun_verileri["aks"])
            set_styles(3, "İkindi", iki_v)
        elif toplam_saniye < vakit_saniyeleri["yat"]:
            sonraki_vakit_adi = "Yatsı"
            self.hedef_zaman = hedef_dt_olustur(an, gunun_verileri["yat"])
            set_styles(4, "Akşam", aks_v)
        else:
            sonraki_vakit_adi = "İmsak"
            sonraki_gun = an + datetime.timedelta(days=1)
            sonraki_gun_str = str(sonraki_gun.day)
            # Ay sonu kontrolü: sadece aynı ay içindeyse sonraki günün verisini kullan
            if (
                sonraki_gun.month == an.month
                and sonraki_gun_str in self.vakitler_sozluk
                and self.vakitler_sozluk[sonraki_gun_str].get("ims")
            ):
                sonraki_gun_verileri = self.vakitler_sozluk[sonraki_gun_str]
                self.yatsi_vakti_gosterimini_guncelle(gunun_verileri, sonraki_gun_verileri)
                self.hedef_zaman = hedef_dt_olustur(sonraki_gun, sonraki_gun_verileri["ims"])
                for i in range(len(all_widgets)):
                    all_widgets[i].setStyleSheet(stil_normal_baslik)
                    all_vakit_widgets[i].setStyleSheet(stil_normal_vakit)
                self.ui.imsak.setStyleSheet(stil_aktif_baslik)
                self.ui.imsak_vakti.setStyleSheet(stil_aktif_vakit)
                self.aktif_vakit_adi = "Yatsı"
                self.aktif_vakit_saati = yat_v
                self.aktif_stil_baslik = stil_aktif_baslik
                self.aktif_stil_vakit = stil_aktif_vakit
                self.aktif_font_baslik = self.ui.imsak.font()
                self.aktif_font_vakit = self.ui.imsak_vakti.font()
            else:
                self.hedef_zaman = datetime.datetime(sonraki_gun.year, sonraki_gun.month, sonraki_gun.day, 0, 0, 0)
                sonraki_vakit_adi = "Yeni Ay"
                set_styles(5, "Yatsı", yat_v)

        self.ui.lab_vaktin_cikmasina.setText(
            f'<html><head/><body><p align="right">{sonraki_vakit_adi} Vaktine:</p></body></html>'
        )

        kalan = max(0, min(86399, int((self.hedef_zaman - an).total_seconds())))
        kalan_saat, kalan_saniye_rem = divmod(kalan, 3600)
        kalan_dakika, kalan_saniye = divmod(kalan_saniye_rem, 60)
        time_obj = QTime(kalan_saat, kalan_dakika, kalan_saniye)

        self.ui.time_edit.setTime(time_obj)
        self.kompakt_pencere.guncelle(
            self.aktif_vakit_adi, self.aktif_vakit_saati,
            self.aktif_stil_baslik, self.aktif_stil_vakit,
            self.aktif_font_baslik, self.aktif_font_vakit,
            time_obj, dark_mode=self.dark_mode
        )

    def timerEvent(self):
        if self.hedef_zaman is None:
            return

        now = datetime.datetime.now()

        # Ay veya gün değiştiyse (ör. uyku modundan çıkışta) verileri senkronize et
        if (now.year, now.month) != self.hesaplanan_ay:
            self.en_son_ne_zaman_calisti()
            self.kac_dakka_var_hesapla()
            return

        kalan = int((self.hedef_zaman - now).total_seconds())
        if kalan <= 0 or now.date() != self.hesaplanan_gun:
            self.kac_dakka_var_hesapla()
            return

        kalan = min(86399, kalan)
        kalan_saat, rem = divmod(kalan, 3600)
        kalan_dakika, kalan_saniye = divmod(rem, 60)
        time_obj = QTime(kalan_saat, kalan_dakika, kalan_saniye)

        self.ui.time_edit.setTime(time_obj)
        self.kompakt_pencere.time_edit.setTime(time_obj)

        if self.window_minimized:
            self.setWindowTitle(f"{self.simdiki_vakit_adi} {time_obj.toString()}")

        # Vakte özel anımsatıcı kontrolü
        kalan_toplam_dk = kalan // 60
        vakit_animsaticilari = self.animsaticilar.get(self.simdiki_vakit_adi, [])
        for anm in vakit_animsaticilari:
            hedef_dk = int(anm.get("dakika", 0))
            tip = anm.get("tip", "tek")
            if tip == "tek":
                anahtar = (self.hedef_zaman, hedef_dk)
                if kalan_toplam_dk == hedef_dk and kalan_saniye == 0 and anahtar not in self.gonderilen_tek_bildirimler:
                    self.gonderilen_tek_bildirimler.add(anahtar)
                    self.bildirim_gonder(f"{self.simdiki_vakit_adi} Vaktinin Çıkmasına", f"Son {hedef_dk} Dakika", 5)
            elif tip == "bir_dakika":
                if kalan_toplam_dk == hedef_dk:
                    self.bildirim_gonder(f"{self.simdiki_vakit_adi} Vaktinin Çıkmasına", f"Son {hedef_dk} Dakika", 5)

    # --- Diğer Fonksiyonlar ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def load_last_location(self):
        last_sehir = ""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    last_sehir = f.read().strip()
            except Exception as e:
                print(f"Son konum yüklenirken hata oluştu: {e}")

        if last_sehir:
            self.sehir_id = last_sehir
            return

        if self.konum_penceresi.exec_() == QDialog.Accepted:
            secili_sehir_gosterim = self.konum_penceresi.ui.sehir_adi.currentText()
            self.sehir_id = self.konum_penceresi.sehir_data[secili_sehir_gosterim]
            self.save_last_location()
        else:
            self.konum_basariyla_yuklendi = False

    def save_last_location(self):
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
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
            if not imsakiye_table:
                raise ValueError("İmsakiye tablosu bulunamadı.")
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
            with open(f"en_son_ne_zaman_calisti_{sehir_id_to_fetch}.txt", "w", encoding="utf-8") as file:
                file.write(now.strftime("%Y\n%m"))
            self.vakitler_sozluk = days_dict
        except (URLError, ValueError) as e:
            print(f"Hata: {e}")
            self.ui.lab_namaz_vakitleri.setText("İnternet Hatası veya\nGeçersiz Şehir!")
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
                with open(check_file, "r", encoding="utf-8") as file:
                    yıl, ay = file.read().strip().split("\n")
                if int(yıl) == now.year and int(ay) == now.month:
                    needs_update = False
            except Exception:
                needs_update = True
        if needs_update:
            self.vakits(self.sehir_id)
        else:
            self.vakitleri_getir()

    def vakitleri_getir(self):
        try:
            with open(f"{self.sehir_id}.txt", "r", encoding="utf-8") as file:
                self.vakitler_sozluk = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.vakits(self.sehir_id)

    def tarih_ne(self, istek):
        return datetime.datetime.strftime(datetime.datetime.now(), istek)

    def yatsi_vakti_gosterimini_guncelle(self, bugunun_verileri, yarin_verileri):
        _translate = QtCore.QCoreApplication.translate
        etiket_widgetleri = self.vakit_baslik_list
        vakit_widgetleri = self.vakit_saat_list
        yeni_etiketler = ["Yatsı", "İmsak", "Güneş", "Öğle", "İkindi", "Akşam"]
        yarin_vakit_anahtarlari = ["ims", "sab", "ogl", "iki", "aks"]
        etiket_widgetleri[0].setText(_translate("Form", yeni_etiketler[0]))
        vakit_widgetleri[0].setText(f'{bugunun_verileri["yat"][0]}:{bugunun_verileri["yat"][1]}')
        for i in range(1, 6):
            etiket_widgetleri[i].setText(_translate("Form", yeni_etiketler[i]))
            vakit_anahtari = yarin_vakit_anahtarlari[i - 1]
            vakit_degeri = yarin_verileri.get(vakit_anahtari)
            if vakit_degeri:
                vakit_widgetleri[i].setText(f'{vakit_degeri[0]}:{vakit_degeri[1]}')
            else:
                vakit_widgetleri[i].setText("--:--")

    @pyqtSlot(str)
    def konumuGuncelle(self, yeni_sehir_id):
        if self.sehir_id != yeni_sehir_id:
            self.sehir_id = yeni_sehir_id
            self.en_son_ne_zaman_calisti()
            self.ui.retranslateUi(self, self)
            self.kac_dakka_var_hesapla()
            self.save_last_location()

    def bildirim_gonder(self, baslik, mesaj, sure):
        if not self.toaster:
            return
        try:
            self.toaster.show_toast(baslik, mesaj, duration=sure, threaded=True)
        except Exception as e:
            print(f"Bildirim hatası: {e}")

    def eventFilter(self, source, event):
        # Şehir adına çift tık: Konum seçimi
        if source is self.ui.lab_namaz_vakitleri and event.type() == QEvent.MouseButtonDblClick:
            self.konum_penceresi.exec_()
            return True

        # Tarihe tek tık: Hicri / Miladi geçişi
        if source is self.ui.lab_tarih and event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.hicri_goster = not self.hicri_goster
            self.ayarlari_kaydet()
            an = datetime.datetime.now()
            tarih_str = hicri_tarih_metni(an) if self.hicri_goster else self.tarih_ne('%d %B %A')
            self.ui.lab_tarih.setText(f'<html><head/><body><p align="center">{tarih_str}</p></body></html>')
            return True

        # Hadis satırına tık: Yeni rastgele hadis
        if source is self.ui.lab_hadis and event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.rastgele_hadis_goster()
            return True

        # Vakit başlığına sağ tık: Second layer anımsatıcı katmanı
        if source in self.vakit_baslik_list and event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:
            vakit_adi = source.text().strip()
            if vakit_adi == "Sabah":
                vakit_adi = "Güneş"
            self.animsatici_katmani.ac(vakit_adi)
            return True

        # Vakit saatine sağ tık: 1 aylık etkileşimli grafik
        if source in self.vakit_saat_list and event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:
            idx = self.vakit_saat_list.index(source)
            vakit_adi = self.vakit_baslik_list[idx].text().strip()
            vakit_key = VAKIT_AD_TO_KEY.get(vakit_adi, "all")
            sehir_adi = self.konum_penceresi.get_sehir_display_name(self.sehir_id).lstrip("'")
            dlg = VakitGrafikDialog(sehir_adi, self.vakitler_sozluk, baslangic_key=vakit_key, dark_mode=self.dark_mode, parent=self)
            dlg.exec_()
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


# --- Uygulamayı Başlat ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QToolTip {
            font-family: "TRT Medium";
            font-size: 8pt;
            color: #f3f4f6;
            background-color: #181b20;
            border: 1px solid #374151;
            border-radius: 4px;
            padding: 2px 5px;
        }
    """)
    ana_pencere = AnaPencere()
    if ana_pencere.konum_basariyla_yuklendi:
        ana_pencere.show()
        sys.exit(app.exec_())
