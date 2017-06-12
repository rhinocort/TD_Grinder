from scipy.optimize import curve_fit
import numpy as np
import csv
import os
import input_output as IO


def func(x, *params):
    # funkce kterou se fituje modry peak
        y = np.zeros_like(x)
        for i in range(0, len(params), 3):
            ctr = params[i]
            amp = params[i+1]
            wid = params[i+2]
            y = y + amp * np.exp(-((1.0/x - ctr)/(1.0*wid))**2)
        return y


def find_L50(wavelength,counts):
    # urceni polohy L50; vstup: (vlnova delka, prislusny count daneho tramecku -
    # pozor - v hlavnim programu je counts definovano jinak (jako pole vsech tramecku))
        poly = []
        L0_50_value = 500
        L0_50_index = 0

        max_peak_0 = np.max(counts[330:1023])
        max_position_0 = np.argmax(counts[330:1023])
        for ijk in range(330,330 + max_position_0):
            if np.abs(counts[ijk] - max_peak_0/2.0) < np.abs(L0_50_value - max_peak_0/2.0):
                L0_50_value = counts [ijk]
                L0_50_index = ijk

        wav = wavelength[L0_50_index - 3: L0_50_index + 4]   # okoli bodu L0_50 se aproximuje linearni funkci
        cou = counts[L0_50_index-3:L0_50_index + 4]
        if len(wav) == 7 and len(cou) == 7:
            poly.append(np.polyfit(wav, cou, 1))
        else:
            poly.append([0.00001, 0])

        L0_50 = ((max_peak_0/2.0) - poly[0][1]) / (poly[0][0]*1.0)

        return L0_50, L0_50_value, L0_50_index


def odecet_modreho_peaku(wavelength, counts_1, L0_50_index):
    x = np.append(wavelength[100:210],wavelength[278:320])          # peak je na pozici cca 400-430 nm (140-200 v poli counts) a 465-475 nm (280-300 v poli counts)
    y = np.append(counts_1[100:210],counts_1[278:320])
    popt, pcov = curve_fit(func, x, y, p0=[0.0022,130,0.0001])

    counts_no_blue_1 = np.zeros([1024], dtype=np.float64)
    for l in range(280):
        counts_no_blue_1[l] = 0
    for l in range(280,L0_50_index):
        counts_no_blue_1[l] = 1.0*(counts_1[l] - func(wavelength[l],*popt))/(1.0+(L0_50_index-330)*(L0_50_index-330)*np.exp((-l+280)/9.0))  # exponencialni prechod mezi odectenym peakem a zbytkem spektra
    for l in range(L0_50_index,1024):
        counts_no_blue_1[l] = counts_1[l]
    return counts_no_blue_1, popt


def resample_counts(wavelength,counts_no_blue_1,start_wavelength,end_wavelength):
    # prumerovani dat - pro kazdou vlnovou delku (integer) se vybere jedna hodnota (prumer nejblizsich)
    size = end_wavelength - start_wavelength + 1

    wavelengths_averaging = np.zeros([size],dtype=np.float64)     # 471 prvku pole predstavuje vlnove delky od 360 do 830 nm !!!
    counts_no_blue_averaged = np.zeros([size],dtype=np.float64)  # 471 prvku pole predstavuje vlnove delky od 360 do 830 nm !!!

    for kk in range(0,len(wavelength)):
        if int(wavelength[kk]) >= start_wavelength:
            wavelengths_averaging[int(wavelength[kk])- start_wavelength] = wavelengths_averaging[int(wavelength[kk]) - start_wavelength] + 1
            counts_no_blue_averaged [int(wavelength[kk])- start_wavelength] = counts_no_blue_averaged [int(wavelength[kk])- start_wavelength] + counts_no_blue_1[kk]
            # potrebujeme dostat data pro vlnove delky od 360 do 830 nm - to odpovida cislovani pole 0:471  (471 hodnot)

    for mm in range(size):
            if wavelengths_averaging[mm] > 0:
                counts_no_blue_averaged[mm] = 1.0 * counts_no_blue_averaged[mm] / wavelengths_averaging[mm]
            else:
                counts_no_blue_averaged[mm] = 0
    return counts_no_blue_averaged


def sum_to_CIE(sumXYZ):
    CIE_x = 1.0 * sumXYZ[0] / ( sumXYZ[0] + sumXYZ[1] + sumXYZ[2] )
    CIE_y = 1.0 * sumXYZ[1] / ( sumXYZ[0] + sumXYZ[1] + sumXYZ[2] )
    return [CIE_x,CIE_y]


def CIExy_to_CIEuv(CIE_xy):
    CIE_u= 4.0 * CIE_xy[0] / (-2*CIE_xy[0] + 12*CIE_xy[1] + 3)
    CIE_v= 9.0 *  CIE_xy[1] / (-2*CIE_xy[0] + 12*CIE_xy[1] + 3)
    return [CIE_u,CIE_v]


def CIExy_to_CCT(CIE_xy):
    n = (CIE_xy[0] - 0.332) / (CIE_xy[1] - 0.1858)
    CCT = (- 449 * np.power(n, 3)) + (3525 * np.power(n, 2)) - (6823.3 * n) + 5520.33
    return CCT


def sum_matching_functions(counts_no_blue_averaged_1, xyz_aux):
    sumXYZ = np.zeros([3],dtype=np.float)
    for aII in range(3):
        for JJJ in range(471):
            sumXYZ[aII] = sumXYZ[aII] + counts_no_blue_averaged_1[JJJ] * xyz_aux[aII,JJJ]
    return sumXYZ


def find_PWL_in_fit(counts_no_blue_averaged, max_peak_lambda, max_peak_index, fit_range):
    poly_fit = np.polyfit(range(max_peak_lambda - fit_range,max_peak_lambda + 2*fit_range),
                                counts_no_blue_averaged[max_peak_index - fit_range : max_peak_index + 2*fit_range], 6)
    polly = np.poly1d(poly_fit)
    crit = polly.deriv().r
    r_crit = crit[crit.imag == 0].real
    test = polly.deriv(2)(r_crit)

    x_max = r_crit[test < 0]
    x_max_max = 0
    for oj in x_max:
        if 600 > oj > 475:
            x_max_max = oj
    y_max = polly(x_max_max)
    if x_max_max == 0:
        y_max = 0

    poly_fit_normalized = tuple(1.0*x/y_max for x in poly_fit)
    return x_max_max, y_max, poly_fit, poly_fit_normalized, polly


def process_trameckomat_data(file_path_input):

    ########### nacteni dat z pomocneho CSV souboru (X,Y,Z hodnoty matching funkce)
    file_path_input_aux = 'matching_functions.csv'
    pokus = 0
    while (not os.path.exists(file_path_input_aux) ) and ( pokus < 2 ) :
        pokus = pokus + 1
        IO.show_message('WARNING','Auxiliary file (matching function) missing in the main input folder.')

    rows_aux = IO.read_CSV_to_array(file_path_input_aux, delimiter=',')

    xyz_aux = np.zeros([3,471],dtype=np.float64)
    for i in range(3):
        for j in range(471):
            xyz_aux[i,j] = rows_aux[j+2][i+1]
    ########### nacteni dat z pomocneho CSV souboru - END

    labels =['Sample Identification', 'Sample Name', 'Carousel', 'Integral from Source File', 'Integral Calculated', 'CIE-x', 'CIE-y', 'CIE-u',
                 'CIE-v', 'CCT', 'MAX-value', 'MAX-lambda', 'Max-lambda-fit', 'L50', 'RLCE1', 'RLCE2', 'RLCE1_calculated', 'RLCE2_calculated',
                 'RLCE', 'CIE-u', 'L_50', 'Max-lambda-fit', 'PASS', 'A6', 'A5', 'A4', 'A3', 'A2', 'A1', 'A0', 'A6-norm', 'A5-norm', 'A4-norm',
                 'A3-norm', 'A2-norm', 'A1-norm', 'A0-norm']

    matrix_output = []
    counts_out = []
    counts_no_blue_out = []
    single_values_out = []
    polly_out = []
    popt_out = []

    for AAA in range(len(file_path_input)):                                     # hlavny cyklus - jednotlive soubory *.csv
        print(file_path_input[AAA])
        number_of_blocks = IO.file_len(file_path_input[AAA])//1038

        rows = IO.read_CSV_to_array(file_path_input[AAA])

        for III in range(number_of_blocks):                                    # cyklus - plata v jednotlivych souborech
            wavelength = np.zeros(1024, dtype=np.float64)
            counts = np.zeros([17,1024], dtype=np.float64)
            counts_no_blue = np.zeros([17,1024], dtype=np.float64)
            counts_no_blue_averaged = np.zeros([17,471], dtype=np.float64)  # 471 prvku pole predstavuje vlnove delky od 360 do 830 nm !!!
            integral = np.zeros([17], dtype=np.float64)
            L0_50 = np.zeros([17], dtype=np.float)
            L0_50_index = np.zeros([17], dtype=np.int)
            L0_50_value = np.multiply(np.ones([17], dtype=np.float), 500)
            CIE_xy = np.zeros([17,2], dtype=np.float)
            CIE_uv = np.zeros([17,2], dtype=np.float)
            corrected_integral = np.zeros([17], dtype=np.float)
            RLCE1 = np.zeros([17], dtype=np.float)
            RLCE2 = np.zeros([17], dtype=np.float)
            RLCE1_calculated = np.zeros([17], dtype=np.float)
            RLCE2_calculated = np.zeros([17], dtype=np.float)
            RLCE = np.zeros([17], dtype=np.float)
            max_peak_value = np.zeros([17], dtype=np.float)
            max_peak_lambda_fit = np.zeros([17], dtype=np.float)
            max_peak_index = np.zeros([17], dtype=np.int)
            max_peak_lambda = np.zeros([17], dtype=np.int)
            passs = ['-' for xxx in range(17)]
            CCT = np.zeros([17], dtype=np.float)
            poly_fits = np.zeros([17,7], dtype=np.float64)
            poly_fits_normalized = np.zeros([17,7], dtype=np.float64)
            matrix = [[0 for x in range(37)] for y in range(17)]
            carousel = rows[4+III*1038][1]

        ### standard check
            standard_10,standard_11 = float(rows[5+III*1038][1].replace(',','.')), float(rows[5+III*1038][2].replace(',', '.'))
            standard_20,standard_21 = float(rows[6+III*1038][1].replace(',','.')), float(rows[6+III*1038][2].replace(',', '.'))
            if ([standard_10,standard_11] != [120,501] and [standard_10,standard_11] != [112,502]) \
                    or ([standard_20,standard_21] != [120,501] and [standard_20,standard_21] != [112,502]):
                IO.show_message('WARNING!','POZOR, CHYBA V ZADANI STANDARDU !')
        ### standard check - END

        ### separace nazvu souboru a tramecku
            tramecky_names = ['' for q in range(17)]
            tramecky_ID = ['' for q in range(17)]
            tramecky_jmena = ['Names']
            for k in range(17):
                if rows[7+III*1038][k+1].find('/') == -1:
                    tramecky_ID[k] = rows[3++III*1038][1]+'/'+rows[7+III*1038][k+1]+'/'+str(III)
                    tramecky_names[k] = rows[7+III*1038][k+1]

                if rows[7+III*1038][k+1].find('/') >= 0:
                    tramecky_ID[k] = rows[7+III*1038][k+1]+'/'+str(III)
                    tramecky_names[k] = rows[7+III*1038][k+1][rows[7+III*1038][k+1].find('/')+1:len(rows[7+III*1038][k+1])]

                tramecky_jmena.append(tramecky_names[k])
        ### separace nazvu souboru a tramecku - END

        ### read spectra
            for i in range(14,1038):
                wavelength[i-14] = float(rows[i+III*1038][0].replace(',','.'))
                for j in range(17):
                    counts[j,i-14] = float(rows[i+III*1038][j+1].replace(',','.')) # mame 19 sloupcu - cislujeme od 0-18
        ### read spectra - END

            for k in range(17):
                integral[k] = float(rows[8+III*1038][k+1].replace(',','.'))

            for k in range(17):                                                 # cyklus - tramecky
                L0_50[k], L0_50_value[k], L0_50_index[k] = find_L50(wavelength, counts[k])
                counts_no_blue[k], popt = odecet_modreho_peaku(wavelength, counts[k], L0_50_index[k])
                counts_no_blue_averaged[k] = resample_counts(wavelength, counts_no_blue[k], 360, 830)
                sumXYZ = sum_matching_functions(counts_no_blue_averaged[k], xyz_aux)
                CIE_xy[k] = sum_to_CIE(sumXYZ)
                CIE_uv[k] = CIExy_to_CIEuv(CIE_xy[k])
                CCT[k] = CIExy_to_CCT(CIE_xy[k])
                corrected_integral[k] = np.sum(counts_no_blue_averaged[k,140:420],dtype=np.float)

            for k in range(17):
                RLCE1[k] = 1.0*integral[k]/integral[0]
                RLCE2[k] = 1.0*integral[k]/integral[16]
                RLCE1_calculated [k] = 1.0*corrected_integral[k]/corrected_integral[0]
                RLCE2_calculated [k] = 1.0*corrected_integral[k]/corrected_integral[16]
                RLCE[k] = (RLCE1_calculated[k] * standard_10 + RLCE2_calculated[k] * standard_20)/2.0

            ### pass
                if L0_50[k] < 498.5 or RLCE[k] < 105 or CIE_uv[k,0] < 0.1467:
                    passs[k] = '0'
                else:
                    passs[k] = '1'
                if CIE_uv[k, 0] > 0.153 or (L0_50[k]) > 502 or (RLCE[k] > 140):
                    passs[k] = 'P'
                if (corrected_integral[k] < 100) or (L0_50[k]) > 1000:
                    passs[k] = 'N'
            ### pass - END

                max_peak_value[k] = np.max(counts_no_blue_averaged[k])
                max_peak_index[k] = np.argmax(counts_no_blue_averaged[k])
                max_peak_lambda[k] = np.int(np.argmax(counts_no_blue_averaged[k]) + 360)

                fit_range = 25
                max_peak_lambda_fit[k], y_max, poly_fits[k], poly_fits_normalized[k], polly = \
                    find_PWL_in_fit(counts_no_blue_averaged[k], max_peak_lambda[k], max_peak_index[k], fit_range)

                if III == 0 and AAA == 0 and k < 1:
                    counts_out = counts[0]
                    counts_no_blue_out = counts_no_blue[0]
                    single_values_out = (L0_50[k], L0_50_value[k], max_peak_lambda[k], max_peak_value[k], fit_range, max_peak_lambda_fit[k])
                    polly_out = poly_fits[k]
                    popt_out = popt
                else:
                    counts_out = np.column_stack((counts_out, counts[k]))
                    counts_no_blue_out = np.column_stack((counts_no_blue_out, counts_no_blue[k]))
                    single_values_out = np.vstack ((single_values_out, (L0_50[k], L0_50_value[k],max_peak_lambda[k],max_peak_value[k],fit_range,max_peak_lambda_fit[k]) ))
                    polly_out = np.column_stack ((polly_out,poly_fits[k]))
                    popt_out = np.column_stack ((popt_out,popt))

            for i in range(17):
                matrix[i][0] = tramecky_ID[i]
                matrix[i][1] = tramecky_names[i]
                matrix[i][2] = carousel
                matrix[i][3] = rows[8+III*1038][i+1].replace(',', '.')
                matrix[i][4] = str(corrected_integral[i])
                matrix[i][5] = str(CIE_xy[i,0])
                matrix[i][6] = str(CIE_xy[i,1])
                matrix[i][7] = str(CIE_uv[i,0])
                matrix[i][8] = str(CIE_uv[i,1])
                matrix[i][9] = str(CCT[i])
                matrix[i][10] = str(max_peak_value[i])
                matrix[i][11] = str(max_peak_lambda[i])
                matrix[i][12] = str(max_peak_lambda_fit[i])
                matrix[i][13] = str(L0_50[i])
                matrix[i][14] = str(RLCE1[i])
                matrix[i][15] = str(RLCE2[i])
                matrix[i][16] = str(RLCE1_calculated[i])
                matrix[i][17] = str(RLCE2_calculated[i])
                matrix[i][18] = str(RLCE[i])
                matrix[i][19] = str(CIE_uv[i,0])
                matrix[i][20] = str(L0_50[i])
                matrix[i][21] = str(max_peak_lambda_fit[i])
                matrix[i][22] = str(passs[i])
                for j in range(7):
                    matrix[i][23+j] = poly_fits[i,j]
                for j in range(7):
                    matrix[i][30+j] = poly_fits_normalized[i,j]

            if III == 0 and AAA == 0:
                matrix_output = matrix
            else:
                matrix_output = np.concatenate((matrix_output,matrix),axis=0)

    return matrix_output, wavelength, counts_out.T, labels, (counts_no_blue_out.T, single_values_out.T, polly_out.T, popt_out.T),

# path = IO.get_input_paths('Vyberte hlavni vstupni soubor (.csv).',[('CSV','*.csv')])
# matrix, wavelength, spectra, labels, others  = process_trameckomat_data(path)

# print others[2]
# print spectra
