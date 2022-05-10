import sys

import matplotlib.pyplot as plt

from NumericalMethods import *


def run():
    xi, fxi = gather_data()

    plt.scatter(xi, fxi, label="Scatter of Data", color='black')
    x_lim = plt.xlim()
    y_lim = plt.ylim()


    
    print("Cubic Spline:")
    spline(xi, fxi)
    print("=-=-=-" * 6 + "=")

    print("Numerical Differentiation:")
    estimate(fxi, 30)
    print("=-=-=-" * 6 + "=")

    plt.xlim(x_lim)
    plt.ylim(y_lim)
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
