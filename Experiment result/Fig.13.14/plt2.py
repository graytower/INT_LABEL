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
				   'size': 11,
				   }
	font_label = {'family': 'Arial',
				  'weight': 'normal',
				  'size': 15,
				  }
	df = pd.read_excel('data.xlsx', sheetname=1)
	data = [df['INT-path'].values.astype('int'), df['pingmesh'].values.astype('int'), df['HULA'].values.astype('int'), df['INT-label'].values.astype('int')]
	labels = ['INT-path', 'Pingmesh', 'HULA', 'INT-label']
	figsize(5, 3)
	plt.figure()
	patterns = ('/', '//', '\\', 'x')
	colors = ('white', 'lemonchiffon', 'lightgreen', 'lightsteelblue')
	x = list(range(len(df['INT-path'].values)))
	total_width, n = 1, 5
	width = total_width / n
	for i in range(len(data)):
		for j in range(len(data[i])):
			if i==0:
				plt.text(x[j]-0.05, data[i][j] + 1, str(data[i][j]),ha='center')
			elif i==2:
				plt.text(x[j], data[i][j] + 100, str(data[i][j]), ha='center')
			elif i==3:
				plt.text(x[j] + 0.03, data[i][j] + 40, str(data[i][j]), ha='center')
			else:
				plt.text(x[j], data[i][j] + 20, str(data[i][j]), ha='center')
		plt.bar(x, data[i], width=width, label=labels[i], color=colors[i], hatch=patterns[i], edgecolor='blue')
		x = [t + width for t in x]
	plt.ylim(1, 500000000)
	plt.grid()
	plt.tick_params(labelsize=15)
	ax = plt.gca()
	ax.set_xticks(np.arange(len(df['INT-path'])) + 1.5 * width)
	ax.set_xticklabels(('10', '20', '30'))

	labels = ax.get_xticklabels() + ax.get_yticklabels()
	[label.set_fontname('Arial') for label in labels]
	plt.xlabel('Pod Number k', font_label)
	plt.ylabel('Bandwidth Cost (Mbps)', font_label)
	# plt.ylim(0,2400)
	plt.yscale('log')
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
	ax.legend(ncol=2, prop=font_legend)
	foo_fig = plt.gcf()  # 'get current figure'
	plt.tight_layout()
	foo_fig.savefig('./comparision2.eps', format='eps', dpi=1000, bbox_inches='tight')
	plt.show()
