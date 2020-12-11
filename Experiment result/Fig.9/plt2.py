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
	data = pd.read_excel('data.xlsx')

	figsize(5, 3)
	plt.figure()

	# print(str_process(df[10][0]))
	plt.plot(np.array(data['interval']), np.array(data['A']) , linewidth=1, linestyle='solid',
						  markersize=8,
						  marker='o', mfc='none', mec='b', label='Base A')
	plt.plot(np.array(data['interval']), np.array(data['B']) , color='red', linewidth=1,
						   linestyle='solid', markersize=8,
						   marker='x', c='', label='Base B')
	plt.plot(np.array(data['interval']), np.array(data['Pro']), color='seagreen', linewidth=1,
			 linestyle='solid', markersize=8,
			 marker='^', c='', label='Pro')

	# plt.ylim(0.4, 1.05)
	plt.xlim(77, 102)
	plt.grid()
	plt.tick_params(labelsize=15)
	ax = plt.gca()
	ax.xaxis.set_major_locator(MultipleLocator(5))
	ax.yaxis.set_major_locator(MultipleLocator(0.02))
	# plt.annotate('', xy=(data['rate'][5], data['A'][5]-0.005),
	# 			 xytext=(data['rate'][5] + 0.05, data['A'][5] - 0.03),
	# 			 arrowprops=dict(shrink=0.05, width=3, color='r'))
	# t = ax.text(data['rate'][5] + 0.05, data['A'][5] - 0.05, "Turning point", ha="center", va="center",
	# 			size=13, )

	labels = ax.get_xticklabels() + ax.get_yticklabels()
	[label.set_fontname('Arial') for label in labels]
	plt.xlabel('Label Interval (ms)', font_label)
	plt.ylabel('Coverage Rate', font_label)
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
	ax.legend(ncol=1, prop=font_legend)
	foo_fig = plt.gcf()  # 'get current figure'
	plt.tight_layout()
	foo_fig.savefig('./Pro_coverage.eps', format='eps', dpi=1000, bbox_inches='tight')
	plt.show()
