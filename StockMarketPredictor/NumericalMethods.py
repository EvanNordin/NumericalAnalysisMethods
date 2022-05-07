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

    #print(xi)
    index = 0
    shares_held = 0
    money = 50000
    current_value = 0
    open_price = 0
    close_price = 0
    risky_strat = False
    open_price = fxi[0]
    action_ledger = []
    for _ in eqns:
        derivs = n_deriv(eqns[index], 3)
        first_deriv = derivs[1]
        second_deriv = derivs[2]
        third_deriv = derivs[3]

        current_value = calc(derivs[0], xi[index+1])
        first_deriv_y = calc(first_deriv, xi[index+1])
        second_deriv_y = calc(second_deriv, xi[index+1]-1)
        third_deriv_y = calc(third_deriv, xi[index+1])

        #print(second_deriv_y)

        could_buy = math.floor(money / current_value)
        
        if xi[index+1] != 390:
            if first_deriv_y >= 0 and second_deriv_y >= 0:
                #if could_buy > 0:
                action_ledger.append("buy")
                    #print("Definite buy at x={0}".format(xi[index+1]))
                    #shares_held += could_buy
                    #money -= current_value * could_buy
            elif first_deriv_y >= 0 and second_deriv_y <= 0:
                
                #if risky_strat:
                action_ledger.append("sell")
                    #print("Risky sell at x={0}".format(xi[index+1]))
                    #money += current_value * shares_held
                    #shares_held = 0

            elif first_deriv_y <= 0 and second_deriv_y >= 0:
                
                #if risky_strat and could_buy > 0:
                action_ledger.append("buy")
                    #print("Risky buy at x={0}".format(xi[index+1]))
                    #shares_held += could_buy
                    #money -= current_value * could_buy

            elif first_deriv_y <= 0 and second_deriv_y <= 0:
                action_ledger.append("sell")
                #print("Definite sell at x={0}".format(xi[index+1]))
                #money += current_value * shares_held
                #shares_held = 0
            
            

        #print("Shares held: {0} -- Money: {1}".format(shares_held, money))
        index += 1
    #print(eqns[-1])
    #return action_ledger[-1]
    #close_price = current_value
    #value = shares_held*current_value + money
    #print("Shares at the end of the day: {0}\nPrice per share: {1}".format(shares_held, current_value))
    #print("You made: {0}\nIndex rose: {1}\nGain over expected: {2}".format(value, close_price - open_price, value - (close_price - open_price)))
    #price_diff = close_price - open_price
    #data = [[open_price, close_price, price_diff, shares_held, value, value - price_diff]]
    #print(tabulate(data, headers=["Open Price", "Close Price", "Price Change", "User Shares Held", "Total Value", "Change Over Holding"]))
    
    #for i in range(len(eqns)):
    #    print("S_{0} = {1}".format(i, eqns[i]))
    #    x_vals, y_vals = evaluate(eqns[i], xi[i], xi[i+1], 0.1)
    #    plt.plot(x_vals, y_vals)

    print("({0}<= x <= {1})\nS_{2} = {3}".format(xi[-2], xi[-1], len(eqns)-1, eqns[-1]))
    x_vals, y_vals = evaluate(eqns[-1], xi[-2], xi[-1], 0.1)
    plt.plot(x_vals, y_vals)
    return action_ledger[-1]

