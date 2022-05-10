import math
import matplotlib.pyplot as plt

import sympy as sp
import numpy as np

from tabulate import tabulate


def calc(f, a):
    x = sp.symbols('x')
    return f.subs(x, a)


def evaluate(f, start, end, step):
    x_vals = []
    y_vals = []
    for i in np.arange(start, end + step, step):
        x_vals.append(i)
        y_vals.append(calc(f, i))
    return x_vals, y_vals


def n_deriv(fx, n):
    x = sp.symbols('x')
    f = fx
    deriv_list = [f]
    for i in range(1, n + 1):
        df_i = deriv_list[-1].diff(x).replace(sp.Derivative, lambda *args: f(x))
        deriv_list.append(df_i)
    return deriv_list


def estimate(fxi, h):
	fxi_est = []
	for i in range(len(fxi)):
		fxi_est.append(derive(fxi, i, h))
	print("Input array: {0}\nOutput array: {1}\nWith an h value of h={2}".format(fxi, fxi_est, h))
	return fxi_est


def derive(fxi, n, h):
	est = 0
	if n < 2:
		# five point forward difference
		est = (-25 * fxi[n] + 48 * fxi[n + 1] - 36 * fxi[n + 2] + 16 * fxi[n + 3] - 3 * fxi[n + 4]) / (12 * h)
	elif n <= len(fxi) - 3:
		# five point midpoint
		est = (fxi[n - 2] - 8 * fxi[n - 1] + 8 * fxi[n + 1] - fxi[n + 2]) / (12 * h)
	elif n <= len(fxi) - 1:
		# five point backward difference
		est = (-25 * fxi[n] + 48 * fxi[n - 1] - 36 * fxi[n - 2] + 16 * fxi[n - 3] - 3 * fxi[n - 4]) / (-12 * h)
	return est


def spline(xi, fxi):
    n = len(xi)
    a = fxi
    h = []
    for i in range(n-1):
        h.append(xi[i+1]-xi[i])
    #print(h)
    matrix_a = [[0 for _ in range(n-2)] for _ in range(n-2)]
    for i in range(n-2):
        try:
            if i == 0:
                matrix_a[i][0] = 2*h[1]+2*h[0]
                matrix_a[i][1] = h[1]
            else:
                for j in range(i-1, i+2):
                    # print("({0},{1})".format(i, j))
                    if j < i:
                        matrix_a[i][j] = h[j+1]
                    if j == i:
                        matrix_a[i][j] = 2*(h[j+1]+h[j])
                    if j > i:
                        try:
                            matrix_a[i][j] = h[j]
                        except IndexError:
                            pass
        except IndexError:
            matrix_a[i][0] = 2*h[1]+2*h[0]

    matrix_b = [0 for _ in range(n-2)]
    for i in range(n-2):
        matrix_b[i] = (3/h[i+1])*(a[i+2]-a[i+1])-(3/h[i])*(a[i+1]-a[i])

    matrix_a = np.matrix(matrix_a)
    matrix_b = np.matrix(matrix_b)

    matrix_c = matrix_a.I*matrix_b.T

    matrix_cj = [0]
    for i in matrix_c.tolist():
        matrix_cj.append(i[0])
    matrix_cj.append(0)

    matrix_bj = [0 for _ in range(n)]
    matrix_dj = [0 for _ in range(n)]

    for j in range(n-1):
        matrix_bj[j] = (a[j+1]-a[j])/h[j]-(2*matrix_cj[j] + matrix_cj[j+1])*(h[j]/3)
        matrix_dj[j] = (matrix_cj[j+1]-matrix_cj[j])/(3*h[j])

    # print("a_j = {0}".format(a))
    # print("b_j = {0}".format(matrix_bj))
    # print("c_j = {0}".format(matrix_cj))
    # print("d_j = {0}".format(matrix_dj))

    x = sp.symbols('x')
    eqns = ["" for _ in range(n-1)]
    for i in range(n-1):
        eqn = "{1}+{2}*(x-{0})+{3}*(x-{0})**2+{4}*(x-{0})**3".format(xi[i], a[i], matrix_bj[i], matrix_cj[i], matrix_dj[i])
        eqn = sp.sympify(eqn)
        eqns[i] = eqn
        
    for i in range(len(eqns)):
        print("({2}<= x <= {3}): S_{0} = {1}".format(i, eqns[i], xi[i], xi[i+1]))
        x_vals, y_vals = evaluate(eqns[i], xi[i], xi[i+1], 0.1)
        plt.plot(x_vals, y_vals)


    x_vals, y_vals = evaluate(eqns[-1], xi[-2], xi[-1], 0.1)
    plt.plot(x_vals, y_vals)
    return
