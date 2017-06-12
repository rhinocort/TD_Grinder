#from __future__ import unicode_literals
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import  QtWidgets
import trameckomat_spectra as TS
import numpy as np
import input_output as IO

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def get_range(name_velicina_ID):
    path = 'graph_ranges.csv'
    csv_array = IO.read_CSV_to_array(path,delimiter=',')
    dict = {csv_array[i][0] : [np.float(csv_array[i][1]),np.float(csv_array[i][2])] for i in range(1,len(csv_array))}
    return dict[name_velicina_ID]

def data_v_rozsahu(data_x,data_y,rozsah_y_low,rozsah_y_high):
    indices = [index for index, value in enumerate(data_y) if ((value > rozsah_y_low) and (value < rozsah_y_high))]
    data_x_v_rozsahu = [data_x[i] for i in indices]
    data_y_v_rozsahu = [data_y[i] for i in indices]
    return (data_x_v_rozsahu, data_y_v_rozsahu)

#print (data_v_rozsahu(range(10),np.multiply(range(10),2),2,15))


class MyCanvas_simple(FigureCanvas):

    def __init__(self, data_x, data_y, label_x='', label_y='', parent=None, width=5, height=4, dpi=100):
        self.data_x = data_x
        self.data_y = data_y
        self.label_x = label_x
        self.label_y = label_y

        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=(0.9,0.9,0.95))
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.clear()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


        self.axes.plot(self.data_x, self.data_y,'ro',markersize=5)


    def update_figure(self,data_x,data_y,label_x='', label_y=''):
            self.axes.plot(data_x, data_y, 'ro',markersize=5)

            self.draw()


class MyCanvas_trameckomat(FigureCanvas):
    def __init__(self, data_x, data_y, trameckomat_data_presence, to_show=(0,0,0,0,0,0), trameckomat_data=(),
                 tramecek_num=0, label_x='', label_y='', parent=None, width=5, height=4, dpi=200, savefg=0, out_path=''):
        self.data_x = data_x
        self.data_y = data_y
        self.label_x = label_x
        self.label_y = label_y
        self.trameckomat_data = trameckomat_data
        self.tramecek_num = tramecek_num
        self.trameckomat_data_presence = trameckomat_data_presence
        self.to_show = to_show
        self.savefig = savefg
        self.out_path = out_path

        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=(0.9,0.9,0.95))
        self.graf = self.fig.add_subplot(111)
        self.graf.clear()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


        self.graf.plot(self.data_x, self.data_y,'ro',markersize=5)


    def update_figure(self, data_x, data_y, trameckomat_data_presence, to_show=(0,0,0,0,0,0), trameckomat_data=(), tramecek_num=0, label_x='', label_y='', savefg=0, out_path=''):
            # trameckomat_data structure:
            # trameckomat_data[0] = counts_no_blue_out
            # trameckomat_data[1] = single_values_out
            #       single_values_out[0] = L0_50, L0_50_value[k], max_peak_lambda[k], max_peak_value[k], fit_range, max_peak_lambda_fit[k]
            # trameckomat_data[2] = poly_fits
            # trameckomat_data[3] = popt

            if trameckomat_data_presence:
                TD = trameckomat_data
                ms = 15
                hand = []
                self.graf.cla()
                if to_show[0]:
                    raw, = self.graf.plot(data_x, data_y,'go',markersize=3, label='Measured data', zorder=1)
                    hand.append(raw)
                self.graf.set_xlabel(label_x)
                self.graf.set_ylabel(label_y)
                #self.graf.hold(True)

                if to_show[3]:
                    L50_pos, = self.graf.plot(TD[1][0][tramecek_num], TD[1][1][tramecek_num], 'g+', zorder=3, label='L50', markersize=ms,)
                    hand.append(L50_pos)
                if to_show[1]:
                    blue_peak_line, = self.graf.plot(data_x[100:400], TS.func(data_x[100:400], TD[3][tramecek_num][0], TD[3][tramecek_num][1], TD[3][tramecek_num][2]), 'b-', zorder=2, label='Blue peak fit')
                    hand.append(blue_peak_line)
                if to_show[2]:
                    corr_data_line, = self.graf.plot(data_x, TD[0][tramecek_num],'r-', zorder=2, label='Corrected data', linewidth=2)
                    hand.append(corr_data_line)
                if to_show[4]:
                    yellow_peak_averaged_data, = self.graf.plot(TD[1][2][tramecek_num],TD[1][3][tramecek_num],'m+', markersize=ms, label='Yellow peak maximum (averaged data)', zorder=3)
                    hand.append(yellow_peak_averaged_data)
                xp = np.linspace(TD[1][2][tramecek_num] - TD[1][4][tramecek_num], TD[1][2][tramecek_num] + 2*TD[1][4][tramecek_num], 100)
                polly = np.poly1d(TD[2][tramecek_num])
                if to_show[5]:
                    poly_fit_line, = self.graf.plot(xp,polly(xp), 'y-', label='Yellow peak polynomial fit', zorder=2)
                    yellow_peak_max_fit, = self.graf.plot(TD[1][5][tramecek_num], polly(TD[1][5][tramecek_num]), '+', zorder=3, markersize=ms, label='Yellow peak maximum (polynomial fit)')
                    hand.append(poly_fit_line)
                    hand.append(yellow_peak_max_fit)
                self.graf.legend(handles=hand,prop={'size':8})

            else:

                self.graf.cla()


                average_all = np.mean(data_y)
                stdev_all = np.std(data_y)
                average_all_points = np.multiply(np.ones(len(data_x)), average_all)
                stdev_all_points_up = np.multiply(np.ones(len(data_x)), average_all + stdev_all)
                stdev_all_points_down = np.multiply(np.ones(len(data_x)), average_all - stdev_all)

                rozsah = get_range(label_y)
                data_in_range = data_v_rozsahu(data_x,data_y,rozsah[0],rozsah[1])

                average_in_range = np.mean(data_in_range[1])
                stdev_in_range = np.std(data_in_range[1])
                average_in_range_points = np.multiply(np.ones(len(data_in_range[0])), average_in_range)
                stdev_in_range_points_up = np.multiply(np.ones(len(data_in_range[0])), average_in_range + stdev_in_range)
                stdev_in_range_points_down = np.multiply(np.ones(len(data_in_range[0])), average_in_range - stdev_in_range)

                self.graf.plot(data_in_range[0], data_in_range[1], 'ro', markersize=5, zorder=1)

                self.graf.plot(data_x, average_all_points, 'r-', zorder=0)
                self.graf.plot(data_in_range[0], average_in_range_points, 'y-', zorder=0)

                self.graf.plot(data_x,stdev_all_points_up,'g-', zorder=2)
                self.graf.plot(data_x, stdev_all_points_down,'g-', zorder=2)
                self.graf.plot(data_in_range[0],stdev_in_range_points_up,'b-', zorder=2)
                self.graf.plot(data_in_range[0], stdev_in_range_points_down,'b-', zorder=2)


                # for i in range(1,50):
                #     stdev_points_up = np.multiply(np.ones(len(data_x)),average+stdev*1.0*i/50)
                #     stdev_points_down = np.multiply(np.ones(len(data_x)),average-stdev*1.0*i/50)
                #     self.graf.fill_between(data_x,stdev_points_down,stdev_points_up,facecolor='blue',alpha=0.007,zorder=1)









                self.graf.set_xlabel(label_x)
                self.graf.set_ylabel(label_y)
                print(label_y)
                print(get_range(label_y))
                self.graf.set_ylim(get_range(label_y))


            if savefg:
                self.fig.savefig(out_path)
            else:
                self.draw()