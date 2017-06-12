from PyQt5.QtWidgets import *#QMainWindow, QApplication, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import *
import numpy as np
import csv
from tkinter import *
from time import gmtime, strftime
import sys

import canvas
import trameckomat_spectra as TS
import input_output as IO

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

qtCreatorFile = "app_layout.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow):

    meze_sirka = [0,0]
    meze_delka = [0,0]
    meze_uhel = [0,0]
    meze_suma_uhlu = [0,0]

    field_state = np.zeros ([51,8],dtype=np.int)  #tramecky cislujem od 1 !!!

    wlist_numbers = []
    wlist_sirka = []
    wlist_delka = []
    wlist_U_PD = []
    wlist_U_PH = []
    wlist_U_LH = []
    wlist_U_LD = []

    wlist_meze_delka = []
    wlist_meze_sirka = []
    wlist_meze_uhel = []
    wlist_meze_suma_uhlu = []
    wlist_column_labels = []

    matrix = []
    counts = []
    labels = []
    others = []
    wavelength = []

    def __init__(self):

        # v programu se pouziva jen nazev sirka (podle vstupu se do pole s nazvem sirka zada bud sirka, nebo vyska)

        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_menu = QMenu('&File', self)
        self.help_menu = QMenu('&Help', self)
        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.help_menu)

    #################################################################################################################### TAB 1 - widgets
        self.wlist_meze_sirka = (self.ui.lineEdit_LSL_sirka,self.ui.lineEdit_USL_sirka)
        self.wlist_meze_delka = (self.ui.lineEdit_LSL_delka,self.ui.lineEdit_USL_delka)
        self.wlist_meze_uhel = (self.ui.lineEdit_LSL_uhel,self.ui.lineEdit_USL_uhel)
        self.wlist_meze_suma_uhlu = (self.ui.lineEdit_LSL_suma_uhlu,self.ui.lineEdit_USL_suma_uhlu)

        self.wlist_column_labels = (self.ui.poradi_label_01, self.ui.poradi_label_02, self.ui.poradi_label_03, self.ui.poradi_label_04, self.ui.poradi_label_05,
                               self.ui.poradi_label_06, self.ui.poradi_label_07, self.ui.poradi_label_08, self.ui.poradi_label_09,
                               self.ui.poradi_label_11, self.ui.poradi_label_12, self.ui.poradi_label_13, self.ui.poradi_label_14, self.ui.poradi_label_15,
                               self.ui.poradi_label_16, self.ui.poradi_label_17, self.ui.poradi_label_18, self.ui.poradi_label_19,
                               self.ui.poradi_label_21, self.ui.poradi_label_22, self.ui.poradi_label_23, self.ui.poradi_label_24, self.ui.poradi_label_25,
                               self.ui.poradi_label_26, self.ui.poradi_label_27, self.ui.poradi_label_28, self.ui.poradi_label_29
                               )

        self.wlist_numbers = (self.ui.label_01, self.ui.label_02, self.ui.label_03, self.ui.label_04, self.ui.label_05,
                              self.ui.label_06, self.ui.label_07, self.ui.label_08, self.ui.label_09, self.ui.label_10,
                              self.ui.label_11, self.ui.label_12, self.ui.label_13, self.ui.label_14, self.ui.label_15,
                              self.ui.label_16, self.ui.label_17, self.ui.label_18, self.ui.label_19, self.ui.label_20,
                              self.ui.label_21, self.ui.label_22, self.ui.label_23, self.ui.label_24, self.ui.label_25,
                              self.ui.label_26, self.ui.label_27, self.ui.label_28, self.ui.label_29, self.ui.label_30,
                              self.ui.label_31, self.ui.label_32, self.ui.label_33, self.ui.label_34, self.ui.label_35,
                              self.ui.label_36, self.ui.label_37, self.ui.label_38, self.ui.label_39, self.ui.label_40,
                              self.ui.label_41, self.ui.label_42, self.ui.label_43, self.ui.label_44, self.ui.label_45,
                              self.ui.label_46, self.ui.label_47, self.ui.label_48, self.ui.label_49, self.ui.label_50
                              )
        self.wlist_sirka = (self.ui.lineEdit_001, self.ui.lineEdit_002, self.ui.lineEdit_003, self.ui.lineEdit_004, self.ui.lineEdit_005,
                            self.ui.lineEdit_006, self.ui.lineEdit_007, self.ui.lineEdit_008, self.ui.lineEdit_009, self.ui.lineEdit_010,
                            self.ui.lineEdit_011, self.ui.lineEdit_012, self.ui.lineEdit_013, self.ui.lineEdit_014, self.ui.lineEdit_015,
                            self.ui.lineEdit_016, self.ui.lineEdit_017, self.ui.lineEdit_018, self.ui.lineEdit_019, self.ui.lineEdit_020,
                            self.ui.lineEdit_021, self.ui.lineEdit_022, self.ui.lineEdit_023, self.ui.lineEdit_024, self.ui.lineEdit_025,
                            self.ui.lineEdit_026, self.ui.lineEdit_027, self.ui.lineEdit_028, self.ui.lineEdit_029, self.ui.lineEdit_030,
                            self.ui.lineEdit_031, self.ui.lineEdit_032, self.ui.lineEdit_033, self.ui.lineEdit_034, self.ui.lineEdit_035,
                            self.ui.lineEdit_036, self.ui.lineEdit_037, self.ui.lineEdit_038, self.ui.lineEdit_039, self.ui.lineEdit_040,
                            self.ui.lineEdit_041, self.ui.lineEdit_042, self.ui.lineEdit_043, self.ui.lineEdit_044, self.ui.lineEdit_045,
                            self.ui.lineEdit_046, self.ui.lineEdit_047, self.ui.lineEdit_048, self.ui.lineEdit_049, self.ui.lineEdit_050,
                            self.ui.lineEdit_101, self.ui.lineEdit_102, self.ui.lineEdit_103, self.ui.lineEdit_104, self.ui.lineEdit_105,
                            self.ui.lineEdit_106, self.ui.lineEdit_107, self.ui.lineEdit_108, self.ui.lineEdit_109, self.ui.lineEdit_110,
                            self.ui.lineEdit_111, self.ui.lineEdit_112, self.ui.lineEdit_113, self.ui.lineEdit_114, self.ui.lineEdit_115,
                            self.ui.lineEdit_116, self.ui.lineEdit_117, self.ui.lineEdit_118, self.ui.lineEdit_119, self.ui.lineEdit_120,
                            self.ui.lineEdit_121, self.ui.lineEdit_122, self.ui.lineEdit_123, self.ui.lineEdit_124, self.ui.lineEdit_125,
                            self.ui.lineEdit_126, self.ui.lineEdit_127, self.ui.lineEdit_128, self.ui.lineEdit_129, self.ui.lineEdit_130,
                            self.ui.lineEdit_131, self.ui.lineEdit_132, self.ui.lineEdit_133, self.ui.lineEdit_134, self.ui.lineEdit_135,
                            self.ui.lineEdit_136, self.ui.lineEdit_137, self.ui.lineEdit_138, self.ui.lineEdit_139, self.ui.lineEdit_140,
                            self.ui.lineEdit_141, self.ui.lineEdit_142, self.ui.lineEdit_143, self.ui.lineEdit_144, self.ui.lineEdit_145,
                            self.ui.lineEdit_146, self.ui.lineEdit_147, self.ui.lineEdit_148, self.ui.lineEdit_149, self.ui.lineEdit_150
                            )
        self.wlist_delka = (self.ui.lineEdit_201, self.ui.lineEdit_202, self.ui.lineEdit_203, self.ui.lineEdit_204, self.ui.lineEdit_205,
                            self.ui.lineEdit_206, self.ui.lineEdit_207, self.ui.lineEdit_208, self.ui.lineEdit_209, self.ui.lineEdit_210,
                            self.ui.lineEdit_211, self.ui.lineEdit_212, self.ui.lineEdit_213, self.ui.lineEdit_214, self.ui.lineEdit_215,
                            self.ui.lineEdit_216, self.ui.lineEdit_217, self.ui.lineEdit_218, self.ui.lineEdit_219, self.ui.lineEdit_220,
                            self.ui.lineEdit_221, self.ui.lineEdit_222, self.ui.lineEdit_223, self.ui.lineEdit_224, self.ui.lineEdit_225,
                            self.ui.lineEdit_226, self.ui.lineEdit_227, self.ui.lineEdit_228, self.ui.lineEdit_229, self.ui.lineEdit_230,
                            self.ui.lineEdit_231, self.ui.lineEdit_232, self.ui.lineEdit_233, self.ui.lineEdit_234, self.ui.lineEdit_235,
                            self.ui.lineEdit_236, self.ui.lineEdit_237, self.ui.lineEdit_238, self.ui.lineEdit_239, self.ui.lineEdit_240,
                            self.ui.lineEdit_241, self.ui.lineEdit_242, self.ui.lineEdit_243, self.ui.lineEdit_244, self.ui.lineEdit_245,
                            self.ui.lineEdit_246, self.ui.lineEdit_247, self.ui.lineEdit_248, self.ui.lineEdit_249, self.ui.lineEdit_250
                            )
        self.wlist_U_PD = (self.ui.lineEdit_301, self.ui.lineEdit_302, self.ui.lineEdit_303, self.ui.lineEdit_304, self.ui.lineEdit_305,
                           self.ui.lineEdit_306, self.ui.lineEdit_307, self.ui.lineEdit_308, self.ui.lineEdit_309, self.ui.lineEdit_310,
                           self.ui.lineEdit_311, self.ui.lineEdit_312, self.ui.lineEdit_313, self.ui.lineEdit_314, self.ui.lineEdit_315,
                           self.ui.lineEdit_316, self.ui.lineEdit_317, self.ui.lineEdit_318, self.ui.lineEdit_319, self.ui.lineEdit_320,
                           self.ui.lineEdit_321, self.ui.lineEdit_322, self.ui.lineEdit_323, self.ui.lineEdit_324, self.ui.lineEdit_325,
                           self.ui.lineEdit_326, self.ui.lineEdit_327, self.ui.lineEdit_328, self.ui.lineEdit_329, self.ui.lineEdit_330,
                           self.ui.lineEdit_331, self.ui.lineEdit_332, self.ui.lineEdit_333, self.ui.lineEdit_334, self.ui.lineEdit_335,
                           self.ui.lineEdit_336, self.ui.lineEdit_337, self.ui.lineEdit_338, self.ui.lineEdit_339, self.ui.lineEdit_340,
                           self.ui.lineEdit_341, self.ui.lineEdit_342, self.ui.lineEdit_343, self.ui.lineEdit_344, self.ui.lineEdit_345,
                           self.ui.lineEdit_346, self.ui.lineEdit_347, self.ui.lineEdit_348, self.ui.lineEdit_349, self.ui.lineEdit_350
                           )
        self.wlist_U_PH = (self.ui.lineEdit_401, self.ui.lineEdit_402, self.ui.lineEdit_403, self.ui.lineEdit_404, self.ui.lineEdit_405,
                           self.ui.lineEdit_406, self.ui.lineEdit_407, self.ui.lineEdit_408, self.ui.lineEdit_409, self.ui.lineEdit_410,
                           self.ui.lineEdit_411, self.ui.lineEdit_412, self.ui.lineEdit_413, self.ui.lineEdit_414, self.ui.lineEdit_415,
                           self.ui.lineEdit_416, self.ui.lineEdit_417, self.ui.lineEdit_418, self.ui.lineEdit_419, self.ui.lineEdit_420,
                           self.ui.lineEdit_421, self.ui.lineEdit_422, self.ui.lineEdit_423, self.ui.lineEdit_424, self.ui.lineEdit_425,
                           self.ui.lineEdit_426, self.ui.lineEdit_427, self.ui.lineEdit_428, self.ui.lineEdit_429, self.ui.lineEdit_430,
                           self.ui.lineEdit_431, self.ui.lineEdit_432, self.ui.lineEdit_433, self.ui.lineEdit_434, self.ui.lineEdit_435,
                           self.ui.lineEdit_436, self.ui.lineEdit_437, self.ui.lineEdit_438, self.ui.lineEdit_439, self.ui.lineEdit_440,
                           self.ui.lineEdit_441, self.ui.lineEdit_442, self.ui.lineEdit_443, self.ui.lineEdit_444, self.ui.lineEdit_445,
                           self.ui.lineEdit_446, self.ui.lineEdit_447, self.ui.lineEdit_448, self.ui.lineEdit_449, self.ui.lineEdit_450
                           )
        self.wlist_U_LH = (self.ui.lineEdit_501, self.ui.lineEdit_502, self.ui.lineEdit_503, self.ui.lineEdit_504, self.ui.lineEdit_505,
                           self.ui.lineEdit_506, self.ui.lineEdit_507, self.ui.lineEdit_508, self.ui.lineEdit_509, self.ui.lineEdit_510,
                           self.ui.lineEdit_511, self.ui.lineEdit_512, self.ui.lineEdit_513, self.ui.lineEdit_514, self.ui.lineEdit_515,
                           self.ui.lineEdit_516, self.ui.lineEdit_517, self.ui.lineEdit_518, self.ui.lineEdit_519, self.ui.lineEdit_520,
                           self.ui.lineEdit_521, self.ui.lineEdit_522, self.ui.lineEdit_523, self.ui.lineEdit_524, self.ui.lineEdit_525,
                           self.ui.lineEdit_526, self.ui.lineEdit_527, self.ui.lineEdit_528, self.ui.lineEdit_529, self.ui.lineEdit_530,
                           self.ui.lineEdit_531, self.ui.lineEdit_532, self.ui.lineEdit_533, self.ui.lineEdit_534, self.ui.lineEdit_535,
                           self.ui.lineEdit_536, self.ui.lineEdit_537, self.ui.lineEdit_538, self.ui.lineEdit_539, self.ui.lineEdit_540,
                           self.ui.lineEdit_541, self.ui.lineEdit_542, self.ui.lineEdit_543, self.ui.lineEdit_544, self.ui.lineEdit_545,
                           self.ui.lineEdit_546, self.ui.lineEdit_547, self.ui.lineEdit_548, self.ui.lineEdit_549, self.ui.lineEdit_550
                           )
        self.wlist_U_LD = (self.ui.lineEdit_601, self.ui.lineEdit_602, self.ui.lineEdit_603, self.ui.lineEdit_604, self.ui.lineEdit_605,
                           self.ui.lineEdit_606, self.ui.lineEdit_607, self.ui.lineEdit_608, self.ui.lineEdit_609, self.ui.lineEdit_610,
                           self.ui.lineEdit_611, self.ui.lineEdit_612, self.ui.lineEdit_613, self.ui.lineEdit_614, self.ui.lineEdit_615,
                           self.ui.lineEdit_616, self.ui.lineEdit_617, self.ui.lineEdit_618, self.ui.lineEdit_619, self.ui.lineEdit_620,
                           self.ui.lineEdit_621, self.ui.lineEdit_622, self.ui.lineEdit_623, self.ui.lineEdit_624, self.ui.lineEdit_625,
                           self.ui.lineEdit_626, self.ui.lineEdit_627, self.ui.lineEdit_628, self.ui.lineEdit_629, self.ui.lineEdit_630,
                           self.ui.lineEdit_631, self.ui.lineEdit_632, self.ui.lineEdit_633, self.ui.lineEdit_634, self.ui.lineEdit_635,
                           self.ui.lineEdit_636, self.ui.lineEdit_637, self.ui.lineEdit_638, self.ui.lineEdit_639, self.ui.lineEdit_640,
                           self.ui.lineEdit_641, self.ui.lineEdit_642, self.ui.lineEdit_643, self.ui.lineEdit_644, self.ui.lineEdit_645,
                           self.ui.lineEdit_646, self.ui.lineEdit_647, self.ui.lineEdit_648, self.ui.lineEdit_649, self.ui.lineEdit_650
                           )
        self.wlist_suma_uhlu = (self.ui.label_suma_01, self.ui.label_suma_02, self.ui.label_suma_03, self.ui.label_suma_04, self.ui.label_suma_05,
                                self.ui.label_suma_06, self.ui.label_suma_07, self.ui.label_suma_08, self.ui.label_suma_09, self.ui.label_suma_10,
                                self.ui.label_suma_11, self.ui.label_suma_12, self.ui.label_suma_13, self.ui.label_suma_14, self.ui.label_suma_15,
                                self.ui.label_suma_16, self.ui.label_suma_17, self.ui.label_suma_18, self.ui.label_suma_19, self.ui.label_suma_20,
                                self.ui.label_suma_21, self.ui.label_suma_22, self.ui.label_suma_23, self.ui.label_suma_24, self.ui.label_suma_25,
                                self.ui.label_suma_26, self.ui.label_suma_27, self.ui.label_suma_28, self.ui.label_suma_29, self.ui.label_suma_30,
                                self.ui.label_suma_31, self.ui.label_suma_32, self.ui.label_suma_33, self.ui.label_suma_34, self.ui.label_suma_35,
                                self.ui.label_suma_36, self.ui.label_suma_37, self.ui.label_suma_38, self.ui.label_suma_39, self.ui.label_suma_40,
                                self.ui.label_suma_41, self.ui.label_suma_42, self.ui.label_suma_43, self.ui.label_suma_44, self.ui.label_suma_45,
                                self.ui.label_suma_46, self.ui.label_suma_47, self.ui.label_suma_48, self.ui.label_suma_49, self.ui.label_suma_50
                                )

        self.wlist_all_input_datafields = (self.wlist_sirka,self.wlist_delka,self.wlist_U_PH,self.wlist_U_PD,self.wlist_U_LD,self.wlist_U_LH,self.wlist_suma_uhlu)
        self.wlist_all_other_inputs = (self.ui.lineEdit_datum,self.ui.lineEdit_cas,
                                       self.ui.lineEdit_LSL_sirka,self.ui.lineEdit_USL_sirka,
                                       self.ui.lineEdit_LSL_delka,self.ui.lineEdit_USL_delka,
                                       self.ui.lineEdit_LSL_uhel,self.ui.lineEdit_USL_uhel,
                                       self.ui.lineEdit_LSL_suma_uhlu,self.ui.lineEdit_USL_suma_uhlu,
                                       self.ui.lineEdit_path_out,self.ui.lineEdit_production_number,self.ui.lineEdit_order_num
                                      )

        ########### set style
        for it in self.wlist_all_input_datafields:
                for ittt in it:
                    ittt.setStyleSheet("QWidget {background-color: rgb(250,250,250) }")

        for it in self.wlist_all_other_inputs:
            it.setStyleSheet("QWidget {background-color: rgb(250,250,250) }")

        for it in self.wlist_column_labels:
            it.setStyleSheet("QWidget {background-color: rgb(200,175,175) }")

        for it in self.wlist_numbers:
            it.setStyleSheet("QWidget {background-color: rgb(150,150,170) }")

        for it in self.wlist_suma_uhlu:
            it.setStyleSheet("QWidget {background-color: rgb(255,255,255) }")

        self.ui.tabWidget.setStyleSheet("QWidget {background-color: rgb(240,240,240) }")

        ###########

        ######## meze
        for i in range(2):
            self.wlist_meze_sirka[i].textChanged.connect(self.meze_sirka_change)
            self.wlist_meze_delka[i].textChanged.connect(self.meze_delka_change)
            self.wlist_meze_uhel[i].textChanged.connect(self.meze_uhel_change)
            self.wlist_meze_suma_uhlu[i].textChanged.connect(self.meze_suma_uhlu_change)

        for i in range(2):
            self.wlist_meze_sirka[i].setValidator(QDoubleValidator(0.99,99.99,4))
            self.wlist_meze_delka[i].setValidator(QDoubleValidator(0.99,99.99,4))
            self.wlist_meze_uhel[i].setValidator(QDoubleValidator(0.99,99.99,4))
            self.wlist_meze_suma_uhlu[i].setValidator(QDoubleValidator(0.99,99.99,4))
        ########

        ######## values
        for i in range(100):
            self.wlist_sirka[i].textChanged.connect(self.sirka_change)
            self.wlist_sirka[i].setValidator(QDoubleValidator(0.99,99.99,4))    # umoznuje float input se tremi desetinnymi misty

        for i in range(50):
            self.wlist_delka[i].textChanged.connect(self.delka_change)
            self.wlist_U_PD[i].textChanged.connect(self.uhel_change)
            self.wlist_U_PH[i].textChanged.connect(self.uhel_change)
            self.wlist_U_LD[i].textChanged.connect(self.uhel_change)
            self.wlist_U_LH[i].textChanged.connect(self.uhel_change)

            self.wlist_delka[i].setValidator(QDoubleValidator(0.99,99.99,4))
            self.wlist_U_PD[i].setValidator(QDoubleValidator(0.99,99.99,4))
            self.wlist_U_PH[i].setValidator(QDoubleValidator(0.99,99.99,4))
            self.wlist_U_LD[i].setValidator(QDoubleValidator(0.99,99.99,4))
            self.wlist_U_LH[i].setValidator(QDoubleValidator(0.99,99.99,4))

        for i in range(50):
            self.wlist_U_PD[i].setText(str(0))
            self.wlist_U_PH[i].setText(str(0))
            self.wlist_U_LH[i].setText(str(0))
            self.wlist_U_LD[i].setText(str(0))
            self.wlist_U_PD[i].textChanged.connect(self.suma_update)
            self.wlist_U_PH[i].textChanged.connect(self.suma_update)
            self.wlist_U_LD[i].textChanged.connect(self.suma_update)
            self.wlist_U_LH[i].textChanged.connect(self.suma_update)

        ######### buttons connections
        self.ui.pushButton_konec.clicked.connect(self.konec)
        self.ui.pushButton_konec_3.clicked.connect(self.konec)
        self.ui.pushButton_import_OUT.clicked.connect(self.import_OUT)
        self.ui.pushButton_export_CSV_all.clicked.connect(self.export_all_CSV)

        self.ui.pushButton_export_CSV_ok.clicked.connect(self.export_good_CSV)
        self.ui.pushButton_export_CSV_bad.clicked.connect(self.export_bad_CSV)
        self.ui.pushButton_import_CSV.clicked.connect(self.tb1_import_CSV)
        #########
    #################################################################################################################### TAB 1 - widgets - END

    #################################################################################################################### TAB T - widgets
        self.ui.pushButton_tabT_show_char.setEnabled(False)
        self.ui.pushButton_tabT_show_spec.setEnabled(False)
        self.ui.pushButton_tabT_saveT.setEnabled(False)

        self.tabT_verticalLayout = self.ui.verticalLayout_17
        self.tabT_sc = canvas.MyCanvas_trameckomat([0],[0],0,self.ui.tabWidget, width=2, height=2, dpi=100)

        self.tabT_toolbar = NavigationToolbar(self.tabT_sc, self)
        self.tabT_toolbar.hide()

        self.tabT_button1 = QPushButton('Zoom')
        self.tabT_button2 = QPushButton('Pan')
        self.tabT_button3 = QPushButton('Home')
        self.tabT_button3.clicked.connect(self.tabT_home)
        self.tabT_button2.clicked.connect(self.tabT_pan)
        self.tabT_button1.clicked.connect(self.tabT_zoom)

        self.tabT_horizLay = QHBoxLayout()
        self.tabT_verticalLayout.addWidget(self.tabT_sc)
        self.tabT_verticalLayout.addLayout(self.tabT_horizLay)

        self.tabT_horizLay.addWidget(self.tabT_button1)
        self.tabT_horizLay.addWidget(self.tabT_button2)
        self.tabT_horizLay.addWidget(self.tabT_button3)
        self.tabT_horizLay.addWidget(self.tabT_toolbar)

        #####
        self.ui.pushButton_tabT_procT_showT.clicked.connect(self.process_and_show_trameckomat_data)
        self.ui.pushButton_konec_2.clicked.connect(self.konec)
        self.ui.pushButton_tabT_show_char.clicked.connect(self.show_characteristic)
        self.ui.pushButton_tabT_show_spec.clicked.connect(self.show_spectrum)
        self.ui.pushButton_tabT_saveT.clicked.connect(self.save_trameckomat_results)
        self.ui.pushButton_tabT_procT_showT_saveT.clicked.connect(self.proc_show_save_trameckomat_data)
        self.ui.pushButton_tabT_procT_saveT.clicked.connect(self.proc_and_save_trameckomat_data)
        self.ui.checkBox_tabT_show_all.stateChanged.connect(self.check_other_checkboxes)
        self.ui.comboBox_tabT_choose_spectrum.currentTextChanged.connect(self.show_spectrum_automatic)
        self.ui.comboBox_tabT_choose_char.currentTextChanged.connect(self.show_characteristic_automatic)
        self.ui.pushButton_tabT_save_plot_char.clicked.connect(self.save_plot_char)
        self.ui.pushButton_tabT_save_plot_spec.clicked.connect(self.save_plot_spec)
        #####

    #################################################################################################################### TAB T - widgets - END

    #################################################################################################################### TAB D - widgets

        self.tabD_verticalLayout = self.ui.verticalLayout
        self.tabD_sc = canvas.MyCanvas_simple([0],[0])

        self.tabD_toolbar = NavigationToolbar(self.tabD_sc, self)
        self.tabD_toolbar.hide()

        self.tabD_button1 = QPushButton('Zoom')
        self.tabD_button2 = QPushButton('Pan')
        self.tabD_button3 = QPushButton('Home')
        self.tabD_button3.clicked.connect(self.tabD_home)
        self.tabD_button2.clicked.connect(self.tabD_pan)
        self.tabD_button1.clicked.connect(self.tabD_zoom)

        self.tabD_horizLay = QHBoxLayout()

        self.tabD_verticalLayout.addWidget(self.tabD_sc)
        self.tabD_verticalLayout.addLayout(self.tabD_horizLay)

        self.tabD_horizLay.addWidget(self.tabD_button1)
        self.tabD_horizLay.addWidget(self.tabD_button2)
        self.tabD_horizLay.addWidget(self.tabD_button3)
        self.tabD_horizLay.addWidget(self.tabD_toolbar)

        ###
        self.ui.pushButton_tabD_import_CSV.clicked.connect(self.tbD_import_data)

    #################################################################################################################### TAB D - widgets - END

    #################################################################################################################### TAB 1 - functions

    def import_OUT(self):
        try:
            strings,sirka_bliz_inp,sirka_dal_inp,delka_inp,U_PD_inp,U_PH_inp,U_LH_inp,U_LD_inp = IO.read_input_file_Mitutoyo()
            meze_delka, meze_sirka, meze_vyska , meze_uhel , meze_suma_uhlu = IO.read_meze()
            self.reset_all_fields()

            for i in range(50):
                if delka_inp[i] > 0:
                    self.wlist_sirka[i].setText(str(sirka_bliz_inp[i]))
                    self.wlist_sirka[i+50].setText(str(sirka_dal_inp[i]))
                    self.wlist_delka[i].setText(str(delka_inp[i]))
                    self.wlist_U_LD[i].setText(str(U_LD_inp[i]))
                    self.wlist_U_PD[i].setText(str(U_PD_inp[i]))
                    self.wlist_U_PH[i].setText(str(U_PH_inp[i]))
                    self.wlist_U_LH[i].setText(str(U_LH_inp[i]))

            for i in range(2):
                self.wlist_meze_delka[i].setText(str(meze_delka[i]))
                self.wlist_meze_uhel[i].setText(str(meze_uhel[i]))
                self.wlist_meze_suma_uhlu[i].setText(str(meze_suma_uhlu[i]))

            ############
            self.ui.label_path_in_2.setText(strings[0])
            self.ui.lineEdit_path_out.setText(strings[1])
            self.ui.lineEdit_datum.setText(strings[2])
            self.ui.lineEdit_cas.setText(strings[3])
            self.ui.lineEdit_order_num.setText(strings[5])

            vyska_or_sirka = int ( strings[4] )
            if vyska_or_sirka == 1:
                self.ui.label_sirka_vyska_2.setText('VYSKA')
                self.ui.label_LSL_sirka.setText('LSL vyska:')
                self.ui.label_USL_sirka.setText('USL vyska:')
                self.wlist_meze_sirka[0].setText(str(meze_vyska[0]))
                self.wlist_meze_sirka[1].setText(str(meze_vyska[1]))
            else:
                if vyska_or_sirka == 2:
                    self.ui.label_sirka_vyska_2.setText('SIRKA')
                    self.ui.label_LSL_sirka.setText('LSL sirka:')
                    self.ui.label_USL_sirka.setText('USL sirka:')
                    self.wlist_meze_sirka[0].setText(str(meze_sirka[0]))
                    self.wlist_meze_sirka[1].setText(str(meze_sirka[1]))
                else:
                    self.ui.label_sirka_vyska.setText('!!!')
                    self.wlist_meze_sirka[0].setText('!!!')
                    self.wlist_meze_sirka[1].setText('!!!')
        except:
            IO.show_message("WARNING!", "Import se nezdaril. Zkontrolujte jestli jsou data ve spravnem formatu.")

        ##############

    def tb1_import_CSV(self):
        try:
            path = IO.get_input_path('Vyberte hlavni vstupni soubor (.out).',[('CSV','*.csv')])
            self.reset_all_fields()
            lines = IO.read_CSV_to_array(path)
            start_line = 14

            for i in range(50):
                if i < (len(lines) - start_line):
                    poradi = np.int(lines[i + start_line][0])-1
                    print('poradie: ', poradi)
                    self.wlist_sirka[poradi].setText(lines[i + start_line][1])
                    self.wlist_sirka[poradi+50].setText(lines[i + start_line][2])
                    self.wlist_delka[poradi].setText(lines[i + start_line][3])
                    self.wlist_U_PD[poradi].setText(lines[i + start_line][4])
                    self.wlist_U_PH[poradi].setText(lines[i + start_line][5])
                    self.wlist_U_LH[poradi].setText(lines[i + start_line][6])
                    self.wlist_U_LD[poradi].setText(lines[i + start_line][7])
            for i in range(2):
                self.wlist_meze_sirka[i].setText(lines[8][i+1])
                self.wlist_meze_delka[i].setText(lines[9][i+1])
                self.wlist_meze_uhel[i].setText(lines[10][i+1])
                self.wlist_meze_suma_uhlu[i].setText(lines[11][i+1])
            ############
            self.ui.label_path_in_2.setText(path)
            self.ui.lineEdit_path_out.setText(path[:-4]+'_OUT.csv')
            self.ui.lineEdit_datum.setText(lines[1][1])
            self.ui.lineEdit_cas.setText(lines[2][1])
            self.ui.lineEdit_order_num.setText(lines[5][1])

            vyska_or_sirka = lines[3][1]
            if vyska_or_sirka == 'VYSKA':
                self.ui.label_sirka_vyska_2.setText('VYSKA')
                self.ui.label_LSL_sirka.setText('LSL vyska:')
                self.ui.label_USL_sirka.setText('USL vyska:')
            else:
                if vyska_or_sirka == 'SIRKA':
                    self.ui.label_sirka_vyska_2.setText('SIRKA')
                    self.ui.label_LSL_sirka.setText('LSL sirka:')
                    self.ui.label_USL_sirka.setText('USL sirka:')
                else:
                    self.ui.label_sirka_vyska.setText('!!!')
                    self.wlist_meze_sirka[0].setText('!!!')
                    self.wlist_meze_sirka[1].setText('!!!')
        except:
            IO.show_message("WARNING!", "Import se nezdaril. Zkontrolujte jestli jsou data ve spravnem formatu.")
            pass
        ##############

    ##############################################

    def export_all_CSV(self):

        try:
            self.update_field_states()
            output_path = self.ui.lineEdit_path_out.text()
            if output_path == '':
                IO.show_message("WARNING!", "Prazdna cesta pro vystupni soubor! Pred exportem zadejte platnou cestu.")
                return

            ofile2 = open(output_path[:-4]+'_ALL.csv','wt', newline='')
            writer2 = csv.writer(ofile2,delimiter=';')

            writer2.writerow(['sep=;'])
            writer2.writerow(['Datum: ',self.ui.lineEdit_datum.text()])
            writer2.writerow(['Cas: ',self.ui.lineEdit_cas.text()])
            writer2.writerow(['Sirka/Vyska: ',self.ui.label_sirka_vyska_2.text()])
            writer2.writerow(['Production Record No.: ',self.ui.lineEdit_production_number.text()])
            writer2.writerow(['Order No.: ',self.ui.lineEdit_order_num.text()])
            writer2.writerow([''])
            writer2.writerow(['Meze:','LSL','USL'])
            writer2.writerow(['Sirka:',self.ui.lineEdit_LSL_sirka.text(),self.ui.lineEdit_USL_sirka.text()])
            writer2.writerow(['Delka:',self.ui.lineEdit_LSL_delka.text(),self.ui.lineEdit_USL_delka.text()])
            writer2.writerow(['Uhel:',self.ui.lineEdit_LSL_uhel.text(),self.ui.lineEdit_USL_uhel.text()])
            writer2.writerow(['Suma uhlu:',self.ui.lineEdit_LSL_suma_uhlu.text(),self.ui.lineEdit_USL_suma_uhlu.text()])
            writer2.writerow([''])
            writer2.writerow(['Poradi v platu','Sirka_bliz','Sirka_dal','Delka','U_PD','U_PH','U_LH','U_LD','U_suma'])

            for i in range(50):
                 if self.field_state[i+1][7] != -1:
                     writer2.writerow([str(i+1),self.wlist_sirka[i].text(),self.wlist_sirka[i+50].text(),self.wlist_delka[i].text(),self.wlist_U_PD[i].text(),self.wlist_U_PH[i].text(),self.wlist_U_LH[i].text(),self.wlist_U_LD[i].text(),self.wlist_suma_uhlu[i].text()])

            ofile2.close()
            IO.show_message('INFO','Data byla exportovana do souboru: '+output_path[:-4]+'_ALL.csv')

        except:
            IO.show_message("WARNING!", "Export dat do CSV souboru se nezdaril. Zkontrolujte jestli se vystupni soubor uz nepouziva.")
            pass

        ##############################################

    def export_bad_CSV(self):

        try:
            self.update_field_states()
            output_path = self.ui.lineEdit_path_out.text()
            if output_path == '':
                IO.show_message("WARNING!", "Prazdna cesta pro vystupni soubor! Pred exportem zadejte platnou cestu.")
                return

            ofile2 = open(output_path[:-4]+'_VADNE.csv','wt', newline='')
            writer2 = csv.writer(ofile2,delimiter=';')

            writer2.writerow(['sep=;'])
            writer2.writerow(['Datum: ',self.ui.lineEdit_datum.text()])
            writer2.writerow(['Cas: ',self.ui.lineEdit_cas.text()])
            writer2.writerow(['Sirka/Vyska: ',self.ui.label_sirka_vyska_2.text()])
            writer2.writerow(['Production Record No.: ',self.ui.lineEdit_production_number.text()])
            writer2.writerow(['Order No.: ',self.ui.lineEdit_order_num.text()])
            writer2.writerow([''])
            writer2.writerow(['Meze:','LSL','USL'])
            writer2.writerow(['Sirka:',self.ui.lineEdit_LSL_sirka.text(),self.ui.lineEdit_USL_sirka.text()])
            writer2.writerow(['Delka:',self.ui.lineEdit_LSL_delka.text(),self.ui.lineEdit_USL_delka.text()])
            writer2.writerow(['Uhel:',self.ui.lineEdit_LSL_uhel.text(),self.ui.lineEdit_USL_uhel.text()])
            writer2.writerow(['Suma uhlu:',self.ui.lineEdit_LSL_suma_uhlu.text(),self.ui.lineEdit_USL_suma_uhlu.text()])
            writer2.writerow([''])
            writer2.writerow(['Poradi v platu','Sirka_bliz','Sirka_dal','Delka','U_PD','U_PH','U_LH','U_LD','U_suma'])

            for i in range(50):
                 if self.field_state[i+1][7] == 0:
                     writer2.writerow([str(i+1),self.wlist_sirka[i].text(),self.wlist_sirka[i+50].text(),self.wlist_delka[i].text(),self.wlist_U_PD[i].text(),self.wlist_U_PH[i].text(),self.wlist_U_LH[i].text(),self.wlist_U_LD[i].text(),self.wlist_suma_uhlu[i].text()])

            ofile2.close()
            IO.show_message('INFO','Data byla exportovana do souboru: '+output_path[:-4]+'_VADNE.csv')

        except:
            IO.show_message("WARNING!", "Export dat do CSV souboru se nezdaril. Zkontrolujte jestli se vystupni soubor uz nepouziva.")
            pass

     ##############################################

    def export_good_CSV(self):

        try:
            self.update_field_states()
            output_path = self.ui.lineEdit_path_out.text()
            if output_path == '':
                IO.show_message("WARNING!", "Prazdna cesta pro vystupni soubor! Pred exportem zadejte platnou cestu.")
                return

            ofile2 = open(output_path[:-4]+'_OK'+'.csv','wt', newline='')
            writer2 = csv.writer(ofile2,delimiter=';')

            writer2.writerow(['sep=;'])
            writer2.writerow(['Datum: ',self.ui.lineEdit_datum.text()])
            writer2.writerow(['Cas: ',self.ui.lineEdit_cas.text()])
            writer2.writerow(['Sirka/Vyska: ',self.ui.label_sirka_vyska_2.text()])
            writer2.writerow(['Production Record No.: ',self.ui.lineEdit_production_number.text()])
            writer2.writerow(['Order No.: ',self.ui.lineEdit_order_num.text()])
            writer2.writerow([''])
            writer2.writerow(['Meze:','LSL','USL'])
            writer2.writerow(['Sirka:',self.ui.lineEdit_LSL_sirka.text(),self.ui.lineEdit_USL_sirka.text()])
            writer2.writerow(['Delka:',self.ui.lineEdit_LSL_delka.text(),self.ui.lineEdit_USL_delka.text()])
            writer2.writerow(['Uhel:',self.ui.lineEdit_LSL_uhel.text(),self.ui.lineEdit_USL_uhel.text()])
            writer2.writerow(['Suma uhlu:',self.ui.lineEdit_LSL_suma_uhlu.text(),self.ui.lineEdit_USL_suma_uhlu.text()])
            writer2.writerow([''])
            writer2.writerow(['Poradi v platu','Sirka_bliz','Sirka_dal','Delka','U_PD','U_PH','U_LH','U_LD','U_suma'])

            for i in range(50):
                 if self.field_state[i+1][7] == 1:
                     writer2.writerow([str(i+1),self.wlist_sirka[i].text(),self.wlist_sirka[i+50].text(),self.wlist_delka[i].text(),self.wlist_U_PD[i].text(),self.wlist_U_PH[i].text(),self.wlist_U_LH[i].text(),self.wlist_U_LD[i].text(),self.wlist_suma_uhlu[i].text()])

            ofile2.close()
            IO.show_message('INFO','Data byla exportovana do souboru: '+output_path[:-4]+'_OK.csv')

        except:
            IO.show_message("WARNING!", "Export dat do CSV souboru se nezdaril. Zkontrolujte jestli se vystupni soubor uz nepouziva.")
            pass

     ##############################################

    def update_field_states(self):
        for i in range(1,51):
            self.field_state[i,7] = self.field_state[i,0] and self.field_state[i,1] and self.field_state[i,2] and self.field_state[i,3] and self.field_state[i,4] and self.field_state[i,5] and self.field_state[i,6]

            if self.wlist_delka[i-1].text() != '':
                if np.float (self.wlist_delka[i-1].text()) == 0:
                    self.field_state[i,7] = -1 # chybejici tramecek
            else: self.field_state[i,7] = -1

     ##############################################

    def sirka_change(self):
        field_changed = self.sender()
        object_name = field_changed.objectName()
        column = int(object_name[-3:])//100
        row = int(object_name[-3:])%100
        text_inserted = field_changed.text()
        print(text_inserted)
        if text_inserted != '':
            value = np.float64 (text_inserted.replace(',','.'))   #.str.replace(',','.')
            if (value < self.meze_sirka[0]) or (value > self.meze_sirka[1]):
                field_changed.setStyleSheet("QWidget {background-color: rgb(255,0,0) }")
                self.field_state[row,column] = 0
            else:
                field_changed.setStyleSheet("QWidget {background-color: rgb(255,255,255) }")
                self.field_state[row,column] = 1

    def delka_change(self):
        field_changed = self.sender()
        object_name = field_changed.objectName()
        column = int(object_name[-3:])//100
        row = int(object_name[-3:])%100
        text_inserted = field_changed.text()
        if text_inserted != '':
            value = np.float64 (text_inserted.replace(',','.'))
            if (value < self.meze_delka[0]) or (value > self.meze_delka[1]):
                field_changed.setStyleSheet("QWidget {background-color: rgb(255,0,0) }")
                self.field_state[row,column] = 0
            else:
                field_changed.setStyleSheet("QWidget {background-color: rgb(255,255,255) }")
                self.field_state[row,column] = 1

    def uhel_change(self):
        field_changed = self.sender()
        object_name = field_changed.objectName()
        column = int(object_name[-3:])//100
        row = int(object_name[-3:])%100
        text_inserted = field_changed.text()
        if text_inserted != '':
            value = np.float64 (text_inserted.replace(',','.'))
            if (value < self.meze_uhel[0]) or (value > self.meze_uhel[1]):
                field_changed.setStyleSheet("QWidget {background-color: rgb(255,100,0) }")
                self.field_state[row,column] = 0
            else:
                field_changed.setStyleSheet("QWidget {background-color: rgb(255,255,255) }")
                self.field_state[row,column] = 1

    def suma_update(self):
        field_changed = self.sender()
        object_name = field_changed.objectName()
        #column = int(object_name[-3:])/100
        row = int(object_name[-3:])%100
        text_inserted = field_changed.text()
        if text_inserted != '':
            new_suma = round(
                             np.float(self.wlist_U_LD[row-1].text().replace(',','.')) +\
                             np.float(self.wlist_U_PD[row-1].text().replace(',','.')) +\
                             np.float(self.wlist_U_LH[row-1].text().replace(',','.')) +\
                             np.float(self.wlist_U_PH[row-1].text().replace(',','.')),3)
            self.wlist_suma_uhlu[row-1].setText(str(new_suma))
            if (new_suma < self.meze_suma_uhlu[0]) or (new_suma > self.meze_suma_uhlu[1]):
                self.wlist_suma_uhlu[row-1].setStyleSheet("QWidget {background-color: rgb(255,100,50) }")
                self.field_state[row,7] = 0
            else:
                self.wlist_suma_uhlu[row-1].setStyleSheet("QWidget {background-color: rgb(255,255,255) }")
                self.field_state[row,7] = 1

    def meze_sirka_change(self):
        field_changed = self.sender()
        field_name = field_changed.objectName()
        text_inserted = field_changed.text()
        if text_inserted != '':
            value = np.float64 (text_inserted)
            if field_name == 'lineEdit_LSL_sirka':
                self.meze_sirka[0] = value
            if field_name == 'lineEdit_USL_sirka':
                self.meze_sirka[1] = value
            for i in range(100):
                if self.wlist_sirka[i].text() != '':
                    temp = self.wlist_sirka[i].text()
                    self.wlist_sirka[i].setText(str(0))
                    self.wlist_sirka[i].setText(temp)

    def meze_delka_change(self):
        field_changed = self.sender()
        field_name = field_changed.objectName()
        text_inserted = field_changed.text()
        if text_inserted != '':
            value = np.float64 (text_inserted)
            if field_name == 'lineEdit_LSL_delka':
                self.meze_delka[0] = value
            if field_name == 'lineEdit_USL_delka':
                self.meze_delka[1] = value
            for i in range(50):
                if self.wlist_delka[i].text() != '':
                    temp = self.wlist_delka[i].text()
                    self.wlist_delka[i].setText(str(0))
                    self.wlist_delka[i].setText(temp)

    def meze_uhel_change(self):
        field_changed = self.sender()
        field_name = field_changed.objectName()
        text_inserted = field_changed.text()
        if text_inserted != '':
            value = np.float64 (text_inserted)
            if field_name == 'lineEdit_LSL_uhel':
                self.meze_uhel[0] = value
            if field_name == 'lineEdit_USL_uhel':
                self.meze_uhel[1] = value
            for it0 in (self.wlist_U_PD,self.wlist_U_LH,self.wlist_U_LD,self.wlist_U_PH):
              for it in it0:
                  if it.text() != '':
                    temp = it.text()
                    it.setText(str(0))
                    it.setText(temp)

    def meze_suma_uhlu_change(self):
        field_changed = self.sender()
        field_name = field_changed.objectName()
        text_inserted = field_changed.text()
        if text_inserted != '':
            value = np.float64 (text_inserted)
            if field_name == 'lineEdit_LSL_suma_uhlu':
                self.meze_suma_uhlu[0] = value
            if field_name == 'lineEdit_USL_suma_uhlu':
                self.meze_suma_uhlu[1] = value
            for it in self.wlist_U_PD:
                if it.text() != '':
                    temp = it.text()
                    it.setText(str(0))
                    it.setText(temp)

    def konec(self):
        sys.exit()

    def state_update(self):
        pass

    def reset_all_fields(self):
        for it in self.wlist_all_other_inputs:
            it.setText('')
            it.setStyleSheet("QWidget {background-color: rgb(250,250,250) }")

        for it in self.wlist_all_input_datafields:
            for ittt in it:
                ittt.setText('0')
                ittt.setStyleSheet("QWidget {background-color: rgb(250,250,250) }")

        # for it in self.wlist_all_other_inputs:
        #     it.setStyleSheet("QWidget {background-color: rgb(250,250,250) }")

    #################################################################################################################### TAB 1 - functions - END

    #################################################################################################################### TAB T - functions

    def process_trameckomat_data(self):
        path = IO.get_input_paths('Vyberte hlavni vstupni soubor (.csv).',[('CSV','*.csv')])
        self.matrix, self.wavelength, self.counts, self.labels, self.others = TS.process_trameckomat_data(path)
        self.ui.lineEdit_tabT_out_path.setText(path[0][:-4]+'_group_OUT.csv')
        self.ui.lineEdit_tabT_out_path.setStyleSheet("QWidget {background-color: rgb(255,255,255) }")

    def import_trameckomat_data_to_table(self):
        IO.form_and_populate_table_widget(self.ui.tableWidget_2,self.matrix,self.labels)

        self.ui.pushButton_tabT_show_char.setEnabled(True)
        self.ui.pushButton_tabT_show_spec.setEnabled(True)
        self.ui.pushButton_tabT_saveT.setEnabled(True)

        self.ui.comboBox_tabT_choose_char.setStyleSheet("QWidget {background-color: rgb(255,255,255) }")
        self.ui.comboBox_tabT_choose_spectrum.setStyleSheet("QWidget {background-color: rgb(255,255,255) }")
        self.ui.comboBox_tabT_choose_char.clear()
        self.ui.comboBox_tabT_choose_spectrum.clear()
        for i in range(2,len(self.labels)):
            self.ui.comboBox_tabT_choose_char.addItem(self.labels[i])
        for i in range(self.ui.tableWidget_2.rowCount()):
            self.ui.comboBox_tabT_choose_spectrum.addItem(str(i+1))

    def save_trameckomat_results(self):
        path = self.ui.lineEdit_tabT_out_path.text()
        array = IO.get_data_from_table_widget(self.ui.tableWidget_2)
        IO.write_arrays_into_csv(path,array, 0)
        #IO.write_arrays_into_csv(path,[[self.labels],self.matrix], 1)
        IO.show_message('INFO','Data byla exportovana do souboru: ' + path)

    def process_and_show_trameckomat_data(self):
        self.process_trameckomat_data()
        self.import_trameckomat_data_to_table()

    def proc_and_save_trameckomat_data(self):
        self.process_trameckomat_data()
        self.save_trameckomat_results()

    def proc_show_save_trameckomat_data(self):
        self.process_trameckomat_data()
        self.import_trameckomat_data_to_table()
        self.save_trameckomat_results()

    def show_characteristic(self,savef=0,path=''):
        row_len = self.ui.tableWidget_2.rowCount()
        data = np.zeros(row_len,dtype=np.float)
        char = self.ui.comboBox_tabT_choose_char.currentText()
        column = self.getcolumn(self.ui.tableWidget_2,char)

        for i in range(row_len):
            data[i] = np.float(self.ui.tableWidget_2.item(i,column).text())

        self.tabT_sc.update_figure(range(1,len(data)+1),data,0,savefg=savef,out_path=path,label_x='Tramecek #',label_y=char)


    def show_spectrum(self,savef=0,path=''):
        row_num = np.int(self.ui.comboBox_tabT_choose_spectrum.currentText())
        checkBox_states = [self.ui.checkBox_tabT_spek.checkState(), self.ui.checkBox_tabT_blue_peak.checkState(),
                           self.ui.checkBox_tabT_po_odecteni.checkState(), self.ui.checkBox_tabT_L50.checkState(),
                           self.ui.checkBox_tabT_peak_max_avg.checkState(),self.ui.checkBox_tabT_peak_max_fit.checkState()]
        self.tabT_sc.update_figure(self.wavelength,self.counts[row_num-1],1,to_show=checkBox_states,
                                   trameckomat_data=self.others, tramecek_num=row_num-1,
                                   label_x='Wavelength', label_y='Counts',savefg=savef,out_path=path)

    def show_spectrum_automatic(self):
        if self.ui.checkBox_tabT_show_automatic.checkState():
            self.show_spectrum()

    def show_characteristic_automatic(self):
        if self.ui.checkBox_tabT_show_automatic.checkState():
            self.show_characteristic()

    def save_plot_char(self):
        path = self.ui.lineEdit_tabT_out_path.text()
        path = path[:-4]+'_out_'+strftime("%Y_%m_%d %H_%M_%S", gmtime())+'.pdf'
        self.show_characteristic(savef=1,path=path)

    def save_plot_spec(self):
        path = self.ui.lineEdit_tabT_out_path.text()
        path = path[:-4]+'_out_'+strftime("%Y_%m_%d %H_%M_%S", gmtime())+'.pdf'
        self.show_spectrum(savef=1,path=path)

    ###
    def tabT_home(self):
            self.tabT_toolbar.home()
    def tabT_zoom(self):
            self.tabT_toolbar.zoom()
    def tabT_pan(self):
            self.tabT_toolbar.pan()

    def getcolumn(self,widget,columnname):
        headercount = widget.columnCount()
        for x in range(0,headercount,1):
            headertext = widget.horizontalHeaderItem(x).text()
            if columnname == headertext:
                matchcol = x
                break
        return matchcol

    def check_other_checkboxes(self):
        if self.ui.checkBox_tabT_show_all.checkState() == 2:
            self.ui.checkBox_tabT_spek.setChecked(True)
            self.ui.checkBox_tabT_blue_peak.setChecked(True)
            self.ui.checkBox_tabT_po_odecteni.setChecked(True)
            self.ui.checkBox_tabT_L50.setChecked(True)
            self.ui.checkBox_tabT_peak_max_avg.setChecked(True)
            self.ui.checkBox_tabT_peak_max_fit.setChecked(True)

    #################################################################################################################### TAB T - functions - END

    #################################################################################################################### TAB D - functions

    def tbD_import_data(self):
        try:
            path = IO.get_input_path('Vyberte hlavni vstupni soubor (.csv).',[('CSV','*.csv')])

            self.ui.tableWidget.setRowCount(50)
            self.ui.tableWidget.setColumnCount(9)

            lines = IO.read_CSV_to_array(path)
            for i in range(len(lines)):
                if (i > 13):
                    for j in range(9):
                         self.ui.tableWidget.setItem(i-14,j, QTableWidgetItem(lines[i][j]))

            self.ui.tableWidget.setHorizontalHeaderLabels(lines[7])
        except:
            pass

    def tabD_home(self):
            self.tabD_toolbar.home()
    def tabD_zoom(self):
            self.tabD_toolbar.zoom()
    def tabD_pan(self):
            self.tabD_toolbar.pan()

    #################################################################################################################### TAB D - functions - END