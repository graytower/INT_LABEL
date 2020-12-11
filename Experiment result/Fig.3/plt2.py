# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re
from sklearn.preprocessing import minmax_scale
from IPython.core.pylabtools import figsize
from matplotlib.ticker import MultipleLocator


def process_data():
    rootdir = './data/'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for type in list:
        l = os.listdir(rootdir + type)
        if type == 'HULA':
            for dir2 in l:
                dir3 = rootdir + type + '/' + dir2
                Oint = 0
                Odata = 0
                for file_name in os.listdir(dir3):
                    df = pd.read_csv(dir3 + '/' + file_name)
                    total_overhead = float(df.iloc[0]['Average']) * float(df.iloc[0]['Rate (ms)'])
                    data_overhead = float(df.iloc[7]['Average']) * float(df.iloc[7]['Rate (ms)'])
                    int_overhead = total_overhead - data_overhead
                    if file_name[0] == '1':  # 发端
                        Oint += 2 * int_overhead
                        Odata += 2 * data_overhead
                    elif file_name[0] == '2':  # 收端
                        Oint += 6 * int_overhead
                        Odata += 6 * data_overhead
                        # print(dir2, type)
                        # print(Oint, '\t', Odata)
                        # print(Oint/Odata)
        if type == 'NEW':
            for dir2 in l:
                dir3 = rootdir + type + '/' + dir2
                Oint = 0
                Odata = 0
                for file_name in os.listdir(dir3):
                    df = pd.read_csv(dir3 + '/' + file_name)
                    int_overhead = (float(df.iloc[7]['Average']) - 1016) * float(df.iloc[7]['Rate (ms)'])
                    data_overhead = 1016 * float(df.iloc[7]['Rate (ms)'])
                    if file_name[0] == '1':  # 发端
                        Oint += 2 * int_overhead
                        Odata += 2 * data_overhead
                    elif file_name[0] == '2':  # 收端
                        Oint += 6 * int_overhead
                        Odata += 6 * data_overhead
                        # print(dir2, type)
                        # print(Oint, '\t', Odata)
                        # print(Oint/Odata)


if __name__ == '__main__':
    figsize(5, 3)
    font_legend = {'family': 'Arial',
                   'weight': 'normal',
                   'size': 12,
                   }
    font_label = {'family': 'Arial',
                  'weight': 'normal',
                  'size': 18,
                  }
    data = pd.read_excel('./data.xlsx',sheetname=1)

    fig, left_axis = plt.subplots()
    right_axis = left_axis.twinx()

    lns1=right_axis.plot(np.array(data['traffic'])*8 / 1000, np.array(data['B_int'])*32/1000, color='red', linewidth=1, linestyle='solid', markersize=8,
                   marker='^', label='B Occupation')
    lns2 = left_axis.plot(np.array(data['traffic'])*8 / 1000, list(data['B_coverage']), color='purple', linewidth=1,
                          linestyle='solid', markersize=8,
                          marker='+', label='B Coverage')
    lns3=right_axis.plot(np.array(data['traffic'])*8/1000, np.array(data['A_int'])*32/1000, color='seagreen', linewidth=1, linestyle='solid', markersize=8,
                    marker='x', c='', label='A Occupation')
    lns4 = left_axis.plot(np.array(data['traffic'])*8/1000, list(data['A_coverage']), color='royalblue', linewidth=1,
                           linestyle='solid', markersize=8,
                           marker='o', mfc='none', mec='b', label='A Coverage')

    plt.grid()
    left_axis.tick_params(labelsize=13)
    right_axis.tick_params(labelsize=13)
    left_axis.set_ylim(0.2,1.1)
    right_axis.set_ylim(0.03,0.14)

    lns = lns4 + lns2 + lns3+lns1
    labs = [l.get_label() for l in lns]
    ax = plt.gca()
    box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
    ax.legend(lns, labs, loc='right',bbox_to_anchor=(1, 0.51),ncol=1,prop=font_legend)
    # ax.legend(loc='center left', bbox_to_anchor=(+0.02, 1.24), ncol=2, prop=font_legend)

    left_axis.annotate('', xy=(data['traffic'][10]*8 / 1000, data['A_coverage'][10]),
                 xytext=(data['traffic'][10]*8 / 1000 - 0.5, data['A_coverage'][10]  + 0.08),
                 arrowprops=dict(shrink=0.05, width=2, color='r'))
    t = left_axis.text(data['traffic'][10]*8 / 1000 - 1.8, data['A_coverage'][10]  + 0.07, "turning point", ha="center", va="center",
                size=13, )

    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    left_axis.set_xlabel('Background Traffic Rate (Mbps)', font_label)
    left_axis.set_ylabel('Coverage Rate',font_label)
    right_axis.set_ylabel('Bandwidth Occupation', font_label)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    left_axis.yaxis.set_major_locator(MultipleLocator(0.2))
    # right_axis.yaxis.set_major_locator(MultipleLocator(0.5))
    foo_fig = plt.gcf()  # 'get current figure'
    plt.tight_layout()
    foo_fig.savefig('./send.eps', format='eps', dpi=1000, bbox_inches='tight')
    plt.show()
