# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re
from sklearn.preprocessing import minmax_scale
from IPython.core.pylabtools import figsize
from matplotlib.ticker import MultipleLocator
import seaborn as sns


def process(str):
	return list(map(float, str.split(' ')))


def list_generator(mean, dis, number):  # 封装一下这个函数，用来后面生成数据
	return np.random.normal(mean, dis * dis, number)  # normal分布，输入的参数是均值、标准差以及生成的数量


def process_data():
	df_A = pd.read_excel('./data2.xlsx', sheetname='A')
	df_B = pd.read_excel('./data2.xlsx', sheetname='B')
	df_P = pd.read_excel('./data2.xlsx', sheetname='Pro')
	df = pd.DataFrame(columns=['coverage', 'algorithm', 'interval'])
	for column in df_A.columns:
		df_new = pd.DataFrame()
		df_new['coverage'] = df_A[column]
		df_new['algorithm'] = 'Base A'
		df_new['interval'] = column
		df = df.append(df_new)
	for column in df_B.columns:
		df_new = pd.DataFrame()
		df_new['coverage'] = df_B[column]
		df_new['algorithm'] = 'Base B'
		df_new['interval'] = column
		df = df.append(df_new)
	for column in df_P.columns:
		df_new = pd.DataFrame()
		df_new['coverage'] = df_P[column]
		df_new['algorithm'] = 'Pro'
		df_new['interval'] = column
		df = df.append(df_new)
	return df


if __name__ == '__main__':
	font_legend = {'family': 'Arial',
				   'weight': 'normal',
				   'size': 15,
				   }
	font_label = {'family': 'Arial',
				  'weight': 'normal',
				  'size': 18,
				  }
	figsize(5, 3)
	plt.figure()
	df=process_data()

	print(df.head())
	sns.boxplot(x='interval',y='coverage',data=df,hue='algorithm',color='blue',fliersize=1)

	# plt.xlim(-1, 51)
	plt.grid()
	plt.tick_params(labelsize=13)
	ax = plt.gca()
	# ax.xaxis.set_major_locator(MultipleLocator(5))
	ax.yaxis.set_major_locator(MultipleLocator(0.05))
	labels = ax.get_xticklabels() + ax.get_yticklabels()
	[label.set_fontname('Arial') for label in labels]
	plt.xlabel('Label Interval (ms)', font_label)
	plt.ylabel('Coverage Rate', font_label)
	# # box = ax.get_position()
	# # ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
	plt.legend(prop=font_legend)
	foo_fig = plt.gcf()  # 'get current figure'
	plt.tight_layout()
	foo_fig.savefig('./mean_std.eps', format='eps', dpi=1000, bbox_inches='tight')
	plt.show()
