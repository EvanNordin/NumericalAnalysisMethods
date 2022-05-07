import sys

import matplotlib.pyplot as plt

from NumericalMethods import *


def run():
    xi, fxi = gather_data()

    plt.scatter(xi, fxi, label="Scatter of Data", color='black')
    x_lim = plt.xlim()
    y_lim = plt.ylim()


    """
    print("Cubic Spline:")
    spline(xi, fxi)
    print("=-=-=-" * 6 + "=")
    """
    day_vals = [[] for _ in range(len(xi)+1)]
    for i in range(3, len(xi)+1):
        day_vals[i] = [xi[x] for x in range(i)]
    day_vals = day_vals[3:]

    money = 5000
    starting_money = money
    open_price = fxi[0]
    close_price = fxi[-1]
    value_at_time = 0
    shares_held = 0
    
    for day_val in day_vals:
        action = spline(day_val, fxi)

        time = day_val[-1]
        value_at_time = fxi[xi.index(time)]
        could_buy = math.floor(money/value_at_time)
        
        if action == "buy":
            if could_buy > 0:
                print("Buying at x={0}, f(x)={1}".format(time, value_at_time))
                shares_held += could_buy
                money -= could_buy * value_at_time
        elif action == "sell":
            if shares_held > 0:
                print("Selling at x={0}, f(x)={1}".format(time, value_at_time))
                money += shares_held * value_at_time
                shares_held = 0

    #EOD sale
    money += shares_held * value_at_time

    price_diff = close_price - open_price
    data = [[open_price, close_price, price_diff, money, money - starting_money, (money - starting_money) - price_diff]]
    print(tabulate(data, headers=["Open Price", "Close Price", "Price Change", "Total Money", "Day Profit", "Profit Over Average"]))
    
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.grid(which='major', axis='both')
    plt.legend(loc="upper left")
    plt.show()


def gather_data():
    xi = get_x_values()
    fxi = get_y_values(xi)

    if not xi:
        xi = [i for i in range(len(fxi))]

    data = [[] for _ in range(len(xi))]
    for i in range(len(xi)):
        data[i] = [xi[i], fxi[i]]
    print(tabulate(data, headers=["x", "F(x)"]))

    return xi, fxi


def get_x_values():
    try:
        #xi = input("Enter x values separated by comma, path and name of datafile, or nothing: ")
        #if xi == "":
        #    pass
        #elif "," in xi:
        #    xi = [float(f) for f in xi.split(",")]
        #else:
        with open("xFile.txt", 'r') as file:
            xi = []
            for line in file:
                xi.append(float(line.strip("\n").replace(" ", "")))
    except FileNotFoundError:
        print("File not found")
        sys.exit()
    except ValueError:
        print("Bad dataset")
        sys.exit()
    return xi


def get_y_values(xi):
    try:
        #fxi = input("Enter y values separated by comma, or path and name of datafile: ")
        #if "," in fxi:
        #    fxi = [float(f) for f in fxi.split(",")]
        #else:
        #    try:
        #        f = sp.sympify(fxi)
        #        x = sp.symbols('x')
        #        fxi = [f.subs(x, i) for i in xi]
        #        print(f)
        #        print(fxi)
        #    except ValueError:
        with open("yFile.txt", 'r') as file:
            fxi = []
            for line in file:
                if line.strip("\n"):
                    fxi.append(float(line.strip("\n").replace(" ", "")))
    except FileNotFoundError:
        print("File not found")
        sys.exit()
    except ValueError:
        print("Bad dataset")
        sys.exit()
    return fxi


if __name__ == "__main__":
    run()
