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
	df=pd.read_excel('data.xlsx')
	data = [df['A'].values*10000, df['B'].values*10000]
	labels = ['Base A', 'Base B']
	figsize(5, 3)
	plt.figure()
	patterns = ('//',  'x')
	colors = ('lightgreen', 'lightsteelblue')
	x = list(range(len(df['A'].values)))
	total_width, n = 1, 5
	width = total_width / n
	for i in range(len(data)):
		plt.bar(x, data[i], width=width, label=labels[i], color=colors[i], hatch=patterns[i], edgecolor='blue')
		x = [t + width for t in x]
	# plt.ylim(ylim, 1)
	plt.grid()
	plt.tick_params(labelsize=15)
	ax = plt.gca()
	ax.set_xticks(np.arange(5) + 1.5 * width)
	ax.set_xticklabels(('1', '2', '3','4','5'))

	labels = ax.get_xticklabels() + ax.get_yticklabels()
	[label.set_fontname('Arial') for label in labels]
	plt.xlabel('INT Label Times', font_label)
	plt.ylabel('Packet Number', font_label)
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
	ax.legend(ncol=1, prop=font_legend)
	foo_fig = plt.gcf()  # 'get current figure'
	plt.tight_layout()
	foo_fig.savefig('./distribution.eps', format='eps', dpi=1000, bbox_inches='tight')
	plt.show()