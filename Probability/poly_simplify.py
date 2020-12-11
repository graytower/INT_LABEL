# -*- coding: UTF-8 -*-
from sympy import *
import numpy as np
import pandas as pd


def calculate_E():
	# H function
	r = Symbol('r')
	k = Symbol('k', integer=True)
	H1 = (k / 2 - 1) / (k ** 3 / 4 - 1)
	H3 = (k / 2 - 1) * (k / 2) / (k ** 3 / 4 - 1)
	H5 = (k - 1) * (k / 2) ** 2 / (k ** 3 / 4 - 1)
	# Y function
	s = Symbol('s', integer=True)
	Y1 = factorial(1) / (factorial(s) * factorial(1 - s)) * r ** s * (1 - r) ** (1 - s)
	Y3 = factorial(3) / (factorial(s) * factorial(3 - s)) * r ** s * (1 - r) ** (3 - s)
	Y5 = factorial(5) / (factorial(s) * factorial(5 - s)) * r ** s * (1 - r) ** (5 - s)
	# E(ZA)
	Pza = H1 * Y1 + H3 * Y3 + H5 * Y5
	Eza = 1 * Pza.subs(s, 1) + 2 * Pza.subs(s, 2) + 3 * Pza.subs(s, 3) + 4 * Pza.subs(s, 4) + 5 * Pza.subs(s, 5)
	# C function
	i = Symbol('i', integer=True)
	f = Function('f')
	x = Symbol('x')
	# m=Symbol('m')
	g = r - x * r
	# C1
	C1_0 = 1 - r
	C1_1 = r
	C1_2 = 0
	C1_3 = 0
	C1_4 = 0
	C1_5 = 0
	# C2
	C2_0 = C1_0 * (1 - r - f(0))
	C2_1 = C1_1 * (1 - g.subs(x, f(1)) - f(1)) + C1_0 * (r + f(0))
	C2_2 = C1_2 * (1 - g.subs(x, f(2)) - f(2)) + C1_1 * (g.subs(x, f(1)) + f(1))
	C2_3 = C1_3 * (1 - g.subs(x, f(3)) - f(3)) + C1_2 * (g.subs(x, f(2)) + f(2))
	C2_4 = C1_4 * (1 - g.subs(x, f(4)) - f(4)) + C1_3 * (g.subs(x, f(3)) + f(3))
	C2_5 = C1_5 * (1 - g.subs(x, f(5)) - f(5)) + C1_4 * (g.subs(x, f(4)) + f(4))
	# C3
	C3_0 = C2_0 * (1 - r) * (1 - f(0))
	C3_1 = C2_1 * (1 - g.subs(x, f(1)) - f(1)) + C2_0 * (r + f(0))
	C3_2 = C2_2 * (1 - g.subs(x, f(2)) - f(2)) + C2_1 * (g.subs(x, f(1)) + f(1))
	C3_3 = C2_3 * (1 - g.subs(x, f(3)) - f(3)) + C2_2 * (g.subs(x, f(2)) + f(2))
	C3_4 = C2_4 * (1 - g.subs(x, f(4)) - f(4)) + C2_3 * (g.subs(x, f(3)) + f(3))
	C3_5 = C2_5 * (1 - g.subs(x, f(5)) - f(5)) + C2_4 * (g.subs(x, f(4)) + f(4))
	# C4
	C4_0 = C3_0 * (1 - r) * (1 - f(0))
	C4_1 = C3_1 * (1 - g.subs(x, f(1)) - f(1)) + C3_0 * (r + f(0))
	C4_2 = C3_2 * (1 - g.subs(x, f(2)) - f(2)) + C3_1 * (g.subs(x, f(1)) + f(1))
	C4_3 = C3_3 * (1 - g.subs(x, f(3)) - f(3)) + C3_2 * (g.subs(x, f(2)) + f(2))
	C4_4 = C3_4 * (1 - g.subs(x, f(4)) - f(4)) + C3_3 * (g.subs(x, f(3)) + f(3))
	C4_5 = C3_5 * (1 - g.subs(x, f(5)) - f(5)) + C3_4 * (g.subs(x, f(4)) + f(4))
	# C5
	C5_0 = C4_0 * (1 - r) * (1 - f(0))
	C5_1 = C4_1 * (1 - g.subs(x, f(1)) - f(1)) + C4_0 * (r + f(0))
	C5_2 = C4_2 * (1 - g.subs(x, f(2)) - f(2)) + C4_1 * (g.subs(x, f(1)) + f(1))
	C5_3 = C4_3 * (1 - g.subs(x, f(3)) - f(3)) + C4_2 * (g.subs(x, f(2)) + f(2))
	C5_4 = C4_4 * (1 - g.subs(x, f(4)) - f(4)) + C4_3 * (g.subs(x, f(3)) + f(3))
	C5_5 = C4_5 * (1 - g.subs(x, f(5)) - f(5)) + C4_4 * (g.subs(x, f(4)) + f(4))

	# E(ZA)
	print('Eza:', Eza)
	# Pza1
	print('Pza1:', Pza.subs({s: 1}))
	# Pza2
	print('Pza2:', Pza.subs({s: 2}))
	# Pza3
	print('Pza3:', Pza.subs({s: 3}))
	# Pza4
	print('Pza4:', Pza.subs({s: 4}))
	# Pza5
	print('Pza5:', Pza.subs({s: 5}))

	# E(ZB)
	Pzb0 = H1 * C1_0 + H3 * C3_0 + H5 * C5_0
	Pzb1 = H1 * C1_1 + H3 * C3_1 + H5 * C5_1
	Pzb2 = H1 * C1_2 + H3 * C3_2 + H5 * C5_2
	Pzb3 = H1 * C1_3 + H3 * C3_3 + H5 * C5_3
	Pzb4 = H1 * C1_4 + H3 * C3_4 + H5 * C5_4
	Pzb5 = H1 * C1_5 + H3 * C3_5 + H5 * C5_5
	Ezb = 1 * Pzb1 + 2 * Pzb2 + 3 * Pzb3 + 4 * Pzb4 + 5 * Pzb5
	# Save Ezb
	df_Ezb = pd.DataFrame()
	p_Ezb = Poly(Ezb)
	print('Ezb.gens:', p_Ezb.gens)
	df_Ezb['monoms'] = p_Ezb.as_dict().keys()
	df_Ezb['coef'] = p_Ezb.as_dict().values()
	df_Ezb.to_excel('Ezb.xlsx', index=False)
	# Save Pzb1
	df_Pzb1 = pd.DataFrame()
	p_Pzb1 = Poly(Pzb1)
	print('Pzb1.gens:', p_Pzb1.gens)
	df_Pzb1['monoms'] = p_Pzb1.as_dict().keys()
	df_Pzb1['coef'] = p_Pzb1.as_dict().values()
	df_Pzb1.to_excel('Pzb1.xlsx', index=False)
	# Save Pzb2
	df_Pzb2 = pd.DataFrame()
	p_Pzb2 = Poly(Pzb2)
	print('Pzb2.gens:', p_Pzb2.gens)
	df_Pzb2['monoms'] = p_Pzb2.as_dict().keys()
	df_Pzb2['coef'] = p_Pzb2.as_dict().values()
	df_Pzb2.to_excel('Pzb2.xlsx', index=False)
	# Save Pzb3
	df_Pzb3 = pd.DataFrame()
	p_Pzb3 = Poly(Pzb3)
	print('Pzb3.gens:', p_Pzb3.gens)
	df_Pzb3['monoms'] = p_Pzb3.as_dict().keys()
	df_Pzb3['coef'] = p_Pzb3.as_dict().values()
	df_Pzb3.to_excel('Pzb3.xlsx', index=False)
	# Save Pzb4
	df_Pzb4 = pd.DataFrame()
	p_Pzb4 = Poly(Pzb4)
	print('Pzb4.gens:', p_Pzb4.gens)
	df_Pzb4['monoms'] = p_Pzb4.as_dict().keys()
	df_Pzb4['coef'] = p_Pzb4.as_dict().values()
	df_Pzb4.to_excel('Pzb4.xlsx', index=False)
	# Save Pzb5
	df_Pzb5 = pd.DataFrame()
	p_Pzb5 = Poly(Pzb5)
	print('Pzb5.gens:', p_Pzb5.gens)
	df_Pzb5['monoms'] = p_Pzb5.as_dict().keys()
	df_Pzb5['coef'] = p_Pzb5.as_dict().values()
	df_Pzb5.to_excel('Pzb5.xlsx', index=False)


# # f: distribution function k: pod num	r:Ts/T
# temp = {f(0): 0, f(1): 1, f(2): 1, f(3): 1, f(4): 1, k: 20, r: 1 / 1000}
# print('Pza:')
# print(Pza.subs({k: 2, r: 1 / 10, s: 1}))
# print(Pza.subs({k: 2, r: 1 / 10, s: 2}))
# print(Pza.subs({k: 2, r: 1 / 10, s: 3}))
# print(Pza.subs({k: 2, r: 1 / 10, s: 4}))
# print(Pza.subs({k: 2, r: 1 / 10, s: 5}))
# print('Pzb:')
# print(Pzb1.subs(temp))
# print(Pzb2.subs(temp))
# print(Pzb3.subs(temp))
# print(Pzb4.subs(temp))
# print(Pzb5.subs(temp))
# print(C5_2.subs(temp))


# # k: pod num	r:Ts/T
# EzaV1 = []
# EzbV1 = []
# for _ in list(np.linspace(2, 20, num=10)):
# 	temp = {k: _, r: 1 / 100}
# 	EzaV1.append(Eza.subs(temp))
# 	EzbV1.append(Ezb.subs(temp))
# EzaV2 = []
# EzbV2 = []
# for _ in list(np.linspace(1 / 1000, 1 / 100, num=10)):
# 	temp = {k: 20, r: _}
# 	EzaV2.append(Eza.subs(temp))
# 	EzbV2.append(Ezb.subs(temp))
# return EzaV1,EzbV1,EzaV2,EzbV2

if __name__ == '__main__':
	calculate_E()
