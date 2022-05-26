# %%

import sys

import matplotlib.pyplot as plt

from NumericalMethods import *


def run():
    xi, fxi = gather_data()

    plt.scatter(xi, fxi, label="Scatter of Data", color='black')
    x_lim = plt.xlim()
    y_lim = plt.ylim()

    tolerance = 0.05
    
    print("Cubic Spline:")
    #spline(xi, fxi)
    print("=-=-=-" * 6 + "=")

    money = 50000
    shares = 0

    interpolationPoints = []
    
    print("Numerical Differentiation:")

    data = [[] for _ in range(len(xi))]
    for i in range(len(xi)):
        try:
            if i == len(xi):
                deriv = estimate(fxi, xi[1]-xi[0])
            else:
                deriv = estimate(fxi[0:i], xi[1]-xi[0])

            #plt.plot([xi[i-1], xi[i]], [deriv[-2], deriv[-1]], label="Deriv at x={0}".format(xi[i]))
            print("Derivative at {0}: {2} --- derivative at {1}: {3}".format(xi[i-1], xi[i], deriv[-2], deriv[-1]))

            #print(xi[0:i])
            #print(deriv[0:i])

            

            #if deriv[-1] - tolerance <= 0 and 0 <= deriv[-1] + tolerance:
            #    print("Close to a direction change")

            second_deriv = (deriv[-1]-deriv[-2])/(xi[i]-xi[i-1])
            print("Second derivative between x={0} and x={1}: {2}".format(xi[i-1], xi[i], second_deriv))

            data[i] = [xi[i], fxi[i], deriv[-1], second_deriv]
            current_price = fxi[i]
            
            could_buy = math.floor(money / current_price)

            if abs(second_deriv) >= tolerance:
                if deriv[-2] < 0 and deriv[-1] > 0:
                    print("Should buy at x={0}".format(xi[i]))
                    if could_buy > 0:
                        print("Can buy")
                        plt.scatter(xi[i], fxi[i], color='blue')
                        #make a tuple of xi[i] and fxi[i] and append to interpolation point list
                        interpolationPoints.append((xi[i], fxi[i]))
                        money -= could_buy * current_price
                        shares += could_buy
                if deriv[-2] > 0 and deriv[-1] < 0:
                    print("Should sell at x={0}".format(xi[i]))
                    if shares > 0:
                        print("Can sell")
                        plt.scatter([xi[i]], [fxi[i]], color='red')
                        #make a tuple of xi[i] and fxi[i] and append to interpolation point list
                        interpolationPoints.append((xi[i], fxi[i]))
                        money += shares * current_price
                        shares = 0
            print("=====")
        except IndexError:
            print("Not enough datapoints for current method at x={0}".format(xi[i]))

    print(tabulate(data, headers=["x", "f(x)", "f'(x)", "f''(x)"]))
            
    print("=-=-=-" * 6 + "=")
    money += shares*current_price
    print("We have ${0}".format(money))
    print("The stock market rose: {0}".format(fxi[-1]-fxi[0]))
    print("We made ${0}".format(money-50000))
    print("We outperformed by ${0}".format((money-50000)-(fxi[-1]-fxi[0])))
    print("Interpolation points: " + str(interpolationPoints[0][0]))

    #building a cubic spline with the interpolation points
    my_xis = []
    my_fxis = []
    for i in range(len(interpolationPoints)):
        my_xis.append(interpolationPoints[i][0])
        my_fxis.append(interpolationPoints[i][1])
    
    cubic_spline = spline(my_xis, my_fxis)

    
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.title("Price of Bitcoin 5/1/2022 8:00 am - 5/7/2022 4:00 am")
    plt.ylabel("Price USD")
    plt.xlabel("Minutes Since 5/1/2022 8:00 am")
    #plt.ylim((-5, 5))
    plt.grid(which='major', axis='both')
    plt.legend(loc="upper left")
    plt.show()


def gather_data():
    xi = get_values("xFile.txt")
    fxi = get_values("yFile.txt")

    data = [[] for _ in range(len(xi))]
    for i in range(len(xi)):
        data[i] = [xi[i], fxi[i]]
    print(tabulate(data, headers=["x", "F(x)"]))

    return xi, fxi

def get_values(filename):
    try:
        with open(filename, 'r') as file:
            data = []
            for line in file:
                data.append(float(line.strip("\n").replace(" ", "")))
    except FileNotFoundError:
        print("File not found")
        sys.exit()
    return data


if __name__ == "__main__":
    run()

# %%
