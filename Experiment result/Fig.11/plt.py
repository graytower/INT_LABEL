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
    font_legend = {'family': 'Arial',
                   'weight': 'normal',
                   'size': 15,
                   }
    font_label = {'family': 'Arial',
                  'weight': 'normal',
                  'size': 18,
                  }
    data = pd.read_excel('./data.xlsx')
    figsize(5, 3)
    plt.figure()

    plt.plot(np.array(data['T']), np.array(data['A']), linewidth=1, linestyle='solid',
             markersize=8,
             marker='o', mfc='none', mec='b', label='Base A')
    plt.plot(np.array(data['T']), np.array(data['B']), color='red', linewidth=1,
             linestyle='solid', markersize=8,
             marker='x', c='', label='Base B')
    plt.plot(np.array(data['T']), np.array(data['HULA']), color='seagreen', linewidth=1,
             linestyle='solid', markersize=8,
             marker='^', c='', label='HULA')
    # plt.ylim(0.4, 1.05)
    plt.xlim(8, 102)
    plt.grid()
    plt.tick_params(labelsize=13)
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(0.02))
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    plt.xlabel('Probe/Label Interval (ms)', font_label)
    plt.ylabel('Packet Loss Rate', font_label)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
    ax.legend(loc='center left',bbox_to_anchor=(0,0.4),ncol=1, prop=font_legend)
    # for tick in ax.get_xticklabels():
    #     tick.set_rotation(30)
    foo_fig = plt.gcf()  # 'get current figure'
    plt.tight_layout()
    foo_fig.savefig('./inter-loss.eps', format='eps', dpi=1000,bbox_inches='tight')
    plt.show()