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
	# print("Input array: {0}\nOutput array: {1}\nWith an h value of h={2}".format(fxi, fxi_est, h))
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


def divided_differences(xi, fxi, verbose, use_prime):
	n = len(fxi)
	orders = [[0 for _ in range(n)] for _ in range(n)]

	# TODO: change h=1 to something better
	fxi_estimate = []
	hermite_ldd = xi[0] == xi[1]
	for i in range(n):
		if hermite_ldd:
			if i % 2 == 0:
				fxi_estimate.append(fxi[i])
		else:
			fxi_estimate.append(fxi[i])

	fxi_prime = []
	if use_prime: 	
		if len(fxi_estimate) < 5:
			fxi_prime = [float(f) for f in input("Enter the derivative values separated by a comma: ").replace(" ", "").split(",")]
		else:
			fxi_prime = estimate(fxi_estimate, 1)

	# fxi_prime = [round(f, 10) for f in fxi_prime]

	prime_count = 0
	for i in range(n):
		if i == 0:
			orders[0] = fxi
		else:
			for x in range(n):
				if x >= i:
					try:
						var = (orders[i - 1][x] - orders[i - 1][x - 1]) / (xi[x] - xi[x - i])
					except ZeroDivisionError:
						# get derivative at x_0 with numerical derivative method
						var = fxi_prime[prime_count]
						prime_count += 1

					# TODO: change values here
					"""
					round_var = round(var, 20)
					if round_var == 0:
						round_var = round(var, 20)
					"""
					orders[i][x] = var

	equation = ""
	for i in range(n):
		if i == 0:
			eqn = "{0}".format(orders[0][0])
		else:
			eqn = "+{0}*".format(orders[i][i])
			for j in range(i):
				eqn += "(x-{0})*".format(xi[j])
			eqn += ")"
			eqn = eqn.replace("*)", "")

		equation += eqn

	equation = sp.sympify(equation)

	equal_count = 0
	data = [[] for _ in range(n)]
	for i in range(n):
		f = round(float(fxi[i]), 10)
		p = round(float(calc(equation, xi[i])), 10)
		equal_count += abs(f - p) < 0.01
		data[i] = [xi[i], f, p, abs(f - p) < 0.01]

	if verbose:
		print("Numerically Approximated Derivative Values at x_i:")
		print(fxi_prime)

		print("Divided Differences triangle:")
		for row in orders:
			print(row)

		print("=-=-=-" * 6 + "=")
		print("Derived equation:")
		print(equation)

		print("=-=-=-" * 6 + "=")
		print("Equality check:")
		print(tabulate(data, headers=["x", "Real Value", "Calculated Value", "Equality"]))
		print("Are all given points equal: {0}".format("Yes" if equal_count == n else "No"))

		if equal_count != n:
			print("Go to the TODO and change the round value if points don't all match up")

	try:
		x_vals, y_vals = evaluate(equation, xi[0] - (xi[1]-xi[0]), xi[-1] + (xi[1]-xi[0]), (xi[1]-xi[0])/10)
	except ZeroDivisionError:
		x_vals, y_vals = evaluate(equation, xi[0] - (xi[2] - xi[0]), xi[-1] + (xi[2] - xi[0]), (xi[2] - xi[0]) / 20)

	return equation, x_vals, y_vals


def hermite(xi, fxi):
	xi_hermite = []
	fxi_hermite = []

	for x in xi:
		xi_hermite.append(x)
		xi_hermite.append(x)
	for f in fxi:
		fxi_hermite.append(f)
		fxi_hermite.append(f)

	eqn, x_vals, y_vals = divided_differences(xi_hermite, fxi_hermite, True, True)
	return eqn, x_vals, y_vals


def spline(xi, fxi):
	n = len(fxi)
	a = fxi
	h = []
	for i in range(n-1):
		h.append(xi[i+1]-xi[i])
	print(h)
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

	print("a_j = {0}".format(a))
	print("b_j = {0}".format(matrix_bj))
	print("c_j = {0}".format(matrix_cj))
	print("d_j = {0}".format(matrix_dj))

	x = sp.symbols('x')
	eqns = ["" for _ in range(n-1)]
	for i in range(n-1):
		eqn = "{1}+{2}*(x-{0})+{3}*(x-{0})**2+{4}*(x-{0})**3".format(xi[i], a[i], matrix_bj[i], matrix_cj[i], matrix_dj[i])
		eqn = sp.sympify(eqn)
		eqns[i] = eqn

	for i in range(len(eqns)):
		print("S_{0} = {1}".format(i, eqns[i]))
		x_vals, y_vals = evaluate(eqns[i], xi[i], xi[i+1], 0.1)
		plt.plot(x_vals, y_vals)






"""
def p_n(deriv_list, x_0, x):
	exp = ""
	for i in range(len(deriv_list)):
		f = deriv_list[i]
		if i > 0:
			fx = str(sp.simplify(f.subs(x, x_0) * (((x - x_0) ** (i)) / (math.factorial(i)))))
		else:
			fx = str(f.subs(x, x_0))

		if i != len(deriv_list) - 1:
			exp += fx + ' + '
		else:
			exp += fx

	exp = sp.parse_expr(exp)
	return exp


def r_n(f, n, x_0, x, xi):
	f = n_deriv(f, n)[-1]

	if math.ceil(xi) == xi:
		xi = math.ceil(xi)
	else:
		print("Remainder evaulation might be messy due to xi being a float")
	fx = str(f.subs(x, xi) * (((x - x_0) ** n) / math.factorial(n)))
	return sp.parse_expr(fx)


def find_max_error(f, n, x_0, x, bounds, step):
	f = n_deriv(f, n)[-1]
	# print(f)
	maxY = None
	maxX = None
	for i in np.arange(bounds[0], bounds[1] + step, step):
		y = abs(calc(f, i))
		if (maxY is None and maxX is None) or y > maxY:
			maxY = y
			maxX = i
	return maxX

def taylor(f, xi, fxi, x_0, n):
	x = sp.symbols('x')

	derivList = n_deriv(f, n)
	poly = p_n(derivList, x_0, x)
	err = find_max_error(f, n + 1, x_0, x, [xi[0], xi[-1]], 0.1)
	error = r_n(f, n + 1, x_0, x, xi)

	x = []
	# y = []
	PList = []
	RList = []
	EList = []

	for i in np.arange(xi[0], xi[-1], 1):
		x.append(i)
		# y.append(f(i))
		PList.append(calc(poly, i))
		RList.append(calc(error, i))
		EList.append(calc(poly, i) + calc(error, i))

	data = [[] for y in range(len(fxi))]
	index = 0
	for i in range(len(fxi)):
		xTest = xi[i]
		real = fxi[i]
		pred = calc(poly, xTest) + calc(error, xTest)
		absErr = abs(real - pred)
		relErr = abs(absErr / real)
		data[index] = [xTest, round(real, 5), round(pred, 5), round(absErr, 5), round(relErr, 5)]
		index += 1
	print(tabulate(data, headers=["x", "Real Value", "Estimated Value", "Absolute Error", "Relative Error"]))

	return PList, RList, EList
"""

# plt.plot(x, PList, label="Polynomial")
# plt.plot(x, RList, label="Error")
# plt.plot(x, EList, label="Taylor Approximation n={0} x_0={1}".format(n, x_0))


class NumericalMethods:
	def __init__(self):
		print("Numerical methods class instantiated")


	def estimate(self, fxi, h):
		fxi_est = []
		for i in range(len(xi)):
			fxi_est.append(self.derive(fxi, i, h))
		# print("Input array: {0}\nOutput array: {1}\nWith an h value of h={2}".format(fxi, fxi_est, h))
		return fxi_est

	def NumericalApprox(self, xi, fxi, divPoints):
		# xi= [2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7]
		# fxi = [-1.709847, -1.373823, -1.119214, -0.9160143, -0.7470223, -0.6015966, -0.5123467]
		h = 0.1
		self.estimate(fxi, h)

		print("=====" * 5)

		# e^x
		nVals = [11, 21, 41]
		start = xi[0]
		end = xi[-1]

		for n in nVals:
			h = (end - start) / (n - 1)

			"""
			xi = []
			fx_calc = []
			for i in np.arange(start, end + h, h):
				x = round(i, 5)
				xi.append(x)
				fx_calc.append(e(x))
			"""

			fx_est = self.estimate(divPoints, h)

			sumErr = 0
			for i in range(len(xi)):
				absErr = abs(divPoints[i] - fx_est[i])
				relErr = abs(absErr / divPoints[i])
				sumErr += relErr
			sumErr /= len(xi)
			print("Average error of estimate n={0} is %{1}".format(n, round(sumErr * 100, 5)))
			plt.plot(xi, fx_est, label="Estimate n={0}".format(n))

		# only plot the most detailed scatter plot for clarity
		# if n == 41:
		#    plt.scatter(xi, fx_calc, label="e^x")

