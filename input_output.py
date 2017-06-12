import tkinter.filedialog as tkFileDialog
import string
import csv
import numpy as np
from decimal import getcontext, Decimal
import tkinter
import tkinter.messagebox as tkMessageBox
import sys
from PyQt5.QtWidgets import *

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def show_message(window_name,message):
    root = tkinter.Tk()
    root.withdraw()
    tkMessageBox.showinfo(window_name, message)


def get_input_path(message,types):
    root = tkinter.Tk()
    root.withdraw()
    path = tkFileDialog.askopenfilename(title=message,filetypes=types,parent=root)
    return path

def get_input_paths(message,types):
    root = tkinter.Tk()
    root.withdraw()
    path = tkFileDialog.askopenfilenames(title=message,filetypes=types,parent=root)
    return path


def read_CSV_to_array(path,delimiter=';'):
    lines = []
    with open(path, 'rt') as f:
        reader = csv.reader(f,delimiter = delimiter)
        for row in reader:
            lines.append(row)
    return lines

def read_OUT_to_array_Mitutoyo(path,delimiter=' '):
    lines = []
    with open(path, 'rt') as f:
        reader = csv.reader(f,delimiter = delimiter)
        for line in reader:
            while '' in line: line.remove('')
            #line.str.replace(',','.')
            lines.append(line)
    return lines


def deg_to_dec(stupne,minuty,sekundy):
    dec = 1.0*stupne + 1.0*minuty/60 + 1.0*sekundy/3600
    return Decimal(dec)


def min_from_string(input_str):
    pos_minuta = input_str.find("'")
    if pos_minuta > 1:
        minuta = (input_str[ pos_minuta-2 : pos_minuta])
    else:
        minuta = (input_str[  : pos_minuta])
    return int(minuta)


def sek_from_string(input_str,input_str_2):
    pos_sekunda = input_str.find('"')
    if pos_sekunda > 0 :
        sekunda = (input_str[ pos_sekunda-2 : pos_sekunda])
    else:
        pos_sekunda = input_str_2.find('"')
        if pos_sekunda > 1:
            sekunda = (input_str_2[ pos_sekunda-2 : pos_sekunda])
        else:
            sekunda = (input_str_2[  : pos_sekunda])

    return int(sekunda)

######################################################################################################################## Mitutoyo


def read_input_file_Mitutoyo():
    rounding = 3
    strings = ['input_file_path','output_file_name','date','time','type = 1(vyska) or 2(sirka)','order number']
    sirka_bliz_inp = np.zeros(50,np.float)
    sirka_dal_inp = np.zeros(50,np.float)
    delka_inp = np.zeros(50,np.float)
    U_PD_inp = np.zeros(50,np.float)
    U_PH_inp = np.zeros(50,np.float)
    U_LH_inp = np.zeros(50,np.float)
    U_LD_inp = np.zeros(50,np.float)

    file_path_input = get_input_path('Vyberte hlavni vstupni soubor (.out).',[('OUT','*.out')])

    poloha_lomitka = str.rfind(file_path_input, '/')
    file_path_output = file_path_input[0:poloha_lomitka+1]+'out_'+file_path_input[poloha_lomitka+1:-4]+'.csv'
    strings[0],strings[1] = file_path_input, file_path_output

    number_of_lines = file_len(file_path_input)
    index = -2
    indices = []
    for i in range(50):
        index = index + 16
        if (index > 333 and index < 353) or (index > 657 and index < 676):
            index = index + 4
        if index < number_of_lines:
            indices.extend([index])

    lines = read_OUT_to_array_Mitutoyo(file_path_input,' ')

    for i in range(len(indices)):
        sirka_bliz_inp[i] = round(np.float(lines[indices[i]][2]), rounding)
        sirka_dal_inp[i] = round(np.float(lines[indices[i]+2][2]), rounding)
        delka_inp[i] = round(np.float(lines[indices[i]+4][2]), rounding)
        U_PD_inp[i] = round(deg_to_dec(
                                        np.float(lines[indices[i]+6][2]),
                                        min_from_string(lines[indices[i]+6][3]),
                                        sek_from_string(lines[indices[i]+6][3],lines[indices[i]+6][4])
                                        ), rounding)
        U_PH_inp[i] = round(deg_to_dec(
                                        np.float(lines[indices[i]+8][2]),
                                        min_from_string(lines[indices[i]+8][3]),
                                        sek_from_string(lines[indices[i]+8][3],lines[indices[i]+8][4])
                                        ), rounding)
        U_LH_inp[i] = round(deg_to_dec(
                                        np.float(lines[indices[i]+10][2]),
                                        min_from_string(lines[indices[i]+10][3]),
                                        sek_from_string(lines[indices[i]+10][3],lines[indices[i]+10][4])
                                        ), rounding)
        U_LD_inp[i] = round(deg_to_dec(
                                        np.float(lines[indices[i]+12][2]),
                                        min_from_string(lines[indices[i]+12][3]),
                                        sek_from_string(lines[indices[i]+12][3],lines[indices[i]+12][4])
                                        ),rounding)

    strings[2] = lines[0][0] [ lines[0][0].find(':')+1 : ]
    strings[3] = lines[0][1]
    strings[4] = lines[2][11]
    strings[5] = lines[6][1] [ lines[6][1].find(':')+1 : ]

    return (strings,sirka_bliz_inp,sirka_dal_inp,delka_inp,U_PD_inp,U_PH_inp,U_LH_inp,U_LD_inp)


def read_meze():
    try:
        meze_sirka = [0,0]
        meze_vyska = [0,0]
        meze_delka = [0,0]
        meze_uhel = [0,0]
        meze_suma_uhlu = [0,0]

        f = open('meze.txt', 'r')
        f.readline()
        meze_delka[0] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_delka[1] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_sirka[0] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_sirka[1] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_vyska[0] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_vyska[1] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_uhel[0] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_uhel[1] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_suma_uhlu[0] = np.float (f.readline())
        f.readline()
        f.readline()
        meze_suma_uhlu[1] = np.float (f.readline())
        f.close()
    except:
        root = tkinter.Tk()
        root.withdraw()
        tkMessageBox.showinfo("WARNING!", "Problem pri nacitani souboru meze.txt!")
        sys.exit()

    print(meze_delka, meze_sirka, meze_vyska, meze_uhel, meze_suma_uhlu)

    return     meze_delka, meze_sirka, meze_vyska  , meze_uhel , meze_suma_uhlu

######################################################################################################################## Mitutoyo - END



######################################################################################################################## Trameckomat - spektra


def form_and_populate_table_widget(widget,array,labels):
        size = np.shape(array)
        widget.setRowCount(size[0])
        widget.setColumnCount(size[1])

        for i in range(size[0]):
            for j in range(size[1]):
                widget.setItem(i,j,QTableWidgetItem(str(array[i][j])))

        widget.setHorizontalHeaderLabels(labels)


def get_data_from_table_widget(widget):
        size0 = widget.rowCount()
        size1 = widget.columnCount()
        array = [['' for x in range(size1)] for y in range(size0+1)]

        for i in range(size0):
            for j in range(size1):
                array[i+1][j] = widget.item(i,j).text()
        for j in range(size1):
            array[0][j] = widget.horizontalHeaderItem(j).text()

        return array


def write_arrays_into_csv(output_filename,arrays,multiple_arrays):
    ofile = open(output_filename,'wb')
    writer = csv.writer(ofile,delimiter=';')
    writer.writerow(['sep=;'])

    if multiple_arrays:
        for array in arrays:
            for line in array:
                writer.writerow(line)
    else:
        for line in arrays:
                writer.writerow(line)

    ofile.close()

######################################################################################################################## Trameckomat - spektra - END


if __name__ == "__main__":
     path = get_input_paths('Vyberte hlavni vstupni soubory (.csv).',[('CSV','*.csv')])


