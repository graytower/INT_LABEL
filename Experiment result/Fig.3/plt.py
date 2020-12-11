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
    rootdir = './send/'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    file_names = os.listdir(rootdir)
    for file_name in file_names:
        df = pd.read_csv(rootdir + file_name)
        send_rate = float(df.iloc[7]['Average']) * float(df.iloc[0]['Rate (ms)'])*8/1000 #Mbps

        print(2 * send_rate)

    # rootdir = './bw/'
    # list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    # for num in list:
	#
    #     l = os.listdir(rootdir + num)
    #     Oint = 0
    #     Odata = 0
    #     for file_name in l:
    #         df = pd.read_csv(rootdir +num+ '/' + file_name)
    #         int_overhead = (float(df.iloc[7]['Average']) - 1016) * float(df.iloc[7]['Rate (ms)'])
    #         data_overhead = 1016 * float(df.iloc[7]['Rate (ms)'])
    #         if file_name[0] == '1':  # 发端
    #             Oint += 2 * int_overhead
    #             Odata += 2 * data_overhead
    #         elif file_name[0] == '2':  # 收端
    #             Oint += 6 * int_overhead
    #             Odata += 6 * data_overhead
    #             # print(dir2, type)
    #             # print(Oint, '\t', Odata)
    #             print(Oint/Odata)


if __name__ == '__main__':
    process_data()
#     font_legend = {'family': 'Arial',
#                    'weight': 'normal',
#                    'size': 15,
#                    }
#     font_label = {'family': 'Arial',
#                   'weight': 'normal',
#                   'size': 18,
#                   }
#     data = pd.read_excel('./data.xlsx')
#     figsize(5.5, 3)
#     plt.figure()
#     plt.plot(list(data['send rate']), list(data['coverage']), color='red', linewidth=1, linestyle=':', markersize=7,
#              marker='^')
#     # plt.plot(list(data.index), list(data['NEW']), color='springgreen', linewidth=1, linestyle=':', markersize=7,
#     #          marker='x', c='', label='NEW')
#     plt.ylim(-0.05, )
#     plt.xlim(-3.35, 264)
#     plt.grid()
#     plt.tick_params(labelsize=15)
#     ax = plt.gca()
#     ax.xaxis.set_major_locator(MultipleLocator(20))
#     ax.yaxis.set_major_locator(MultipleLocator(0.2))
#     labels = ax.get_xticklabels() + ax.get_yticklabels()
#     [label.set_fontname('Arial') for label in labels]
#     plt.xlabel('Send Throughput (kbps)', font_label)
#     plt.ylabel('Coverage Rate', font_label)
#     box = ax.get_position()
#     ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
#     # ax.legend(loc='center left', bbox_to_anchor=(0.1, 1.15), ncol=3, prop=font_legend)
#     for tick in ax.get_xticklabels():
#         tick.set_rotation(30)
#     foo_fig = plt.gcf()  # 'get current figure'
#     plt.tight_layout()
#     foo_fig.savefig('./send.eps', format='eps', dpi=1000, bbox_inches='tight')
#     plt.show()
