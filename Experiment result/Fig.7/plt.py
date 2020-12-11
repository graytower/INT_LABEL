# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re
from sklearn.preprocessing import minmax_scale
from IPython.core.pylabtools import figsize
from matplotlib.ticker import MultipleLocator



if __name__ == '__main__':
    figsize(5, 3)
    font_legend = {'family': 'Arial',
                   'weight': 'normal',
                   'size': 11,
                   }
    font_label = {'family': 'Arial',
                  'weight': 'normal',
                  'size': 18,
                  }
    data = pd.read_excel('./data.xlsx')

    fig, left_axis = plt.subplots()
    right_axis = left_axis.twinx()

    lns1=left_axis.plot(np.array(data['interval']), list(data['A_coverage']), color='red', linewidth=1, linestyle='solid', markersize=8,
                   marker='^', label='A Coverage')
    lns2 = left_axis.plot(np.array(data['interval']), list(data['B_coverage']), color='purple', linewidth=1,
                          linestyle='solid', markersize=8,
                          marker='+', label='B Coverage')
    lns3=right_axis.plot(np.array(data['interval']), np.array(data['A_int'])*573.4808*8/1000*32/1000, color='seagreen', linewidth=1, linestyle='solid', markersize=8,
                    marker='x', c='', label='A Bandwidth')
    lns4 = right_axis.plot(np.array(data['interval']), np.array(data['B_int'])*573.4808*8/1000*32/1000, color='royalblue', linewidth=1,
                           linestyle='solid', markersize=8,
                           marker='o', mfc='none', mec='b', label='B Bandwidth')

    plt.grid()
    left_axis.tick_params(labelsize=13)
    left_axis.set_ylim(0.805,)
    right_axis.tick_params(labelsize=13)
    plt.ylim(-0.08,)

    lns = lns1 + lns2 + lns3+lns4
    labs = [l.get_label() for l in lns]
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
    ax.legend(lns, labs, loc='lower left',bbox_to_anchor=(0.01, 0.01),ncol=2,prop=font_legend)
    # ax.legend(loc='center left', bbox_to_anchor=(+0.02, 1.24), ncol=2, prop=font_legend)

    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    left_axis.set_xlabel('Label Interval (ms)', font_label)
    left_axis.set_ylabel('Coverage Rate',font_label)
    right_axis.set_ylabel('INT Bandwidth (Mbps)', font_label)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    left_axis.yaxis.set_major_locator(MultipleLocator(0.03))
    # right_axis.yaxis.set_major_locator(MultipleLocator(0.5))
    foo_fig = plt.gcf()  # 'get current figure'
    plt.tight_layout()
    foo_fig.savefig('./redundancy_interval.eps', format='eps', dpi=1000, bbox_inches='tight')
    plt.show()
