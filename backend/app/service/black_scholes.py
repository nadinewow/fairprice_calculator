import math

import sympy as sym
from app.schemas import BlackScholesData
from app.service.utils import white_noise
from app.service.variables import *
import numpy as np


def fill_matrix(h, y0, level, S0, K, sigma):
    res = [[None for i in range(2**(level))] for j in range(level + 1)]
    res[0][0] = y0
    for i in range(1, level + 1):
        for j in range(0, 2**i, 2):
            res[i][j] = res[i - 1][j // 2] - sigma * math.sqrt(h)
            res[i][j + 1] = res[i - 1][j // 2] + sigma * math.sqrt(h)

    for j in range(len(res[0])):
        res[-1][j] = max(S0 * math.exp(res[-1][j]) - K, 0)

    return res


def refill_matrix(matrix, p):
    for i in range(len(matrix) - 1, 0, -1):
        for j in range(0, 2**i, 2):
            matrix[i-1][j // 2] = matrix[i][j] * (1 - p) + matrix[i][j + 1] * p

# from pprint import pprint
# m = fill_matrix(0, 4)
# pprint(m)
# refill_matrix(m)
# pprint(m)


def black_scholes(data: BlackScholesData):
    z = sym.Symbol('z')

    temp1 = (math.log(data.S0 / data.K) + data.T * (data.r + data.sigma * data.sigma / 2)) / (data.sigma * math.sqrt(data.T))
    temp2 = (math.log(data.S0 / data.K) + data.T * (data.r - data.sigma * data.sigma / 2)) / (data.sigma * math.sqrt(data.T))

    expr1 = 1 / sym.sqrt(2 * sym.pi) * sym.integrate(sym.exp(-z * z / 2), (z, 0, temp1)) + 0.5
    expr2 = 1 / sym.sqrt(2 * sym.pi) * sym.integrate(sym.exp(-z * z / 2), (z, 0, temp2)) + 0.5
    C = data.S0 * expr1 - data.K * math.exp(-data.r * data.T) * expr2
    C = C.evalf()
    print(C)
    return float(C)


def monte_karlo(data: BlackScholesData):
    h = data.T / N
    S = 0
    for i in range(M):
        y = 0
        eps = white_noise()
        for j in range(1, N):
            y += (data.r - data.sigma ** 2 / 2) * h + data.sigma * math.sqrt(h) * eps[j]
        S += max(data.S0 * math.exp(y) - data.K, 0)
    C = math.exp(-data.r * data.T) * S / M
    print(C)
    return C


def binomial(data: BlackScholesData):
    h = data.T / N
    p = 0.5 + (data.r - data.sigma**2 / 2) * math.sqrt(h) / (2 * data.sigma)
    matrix = fill_matrix(h, 0, N, data.S0, data.K, data.sigma)
    # print(matrix)
    refill_matrix(matrix, p)
    # print(matrix)
    C = math.exp(-data.r * data.T) * matrix[0][0]
    print(C)
    return C

d = BlackScholesData( S0=5,
    K=3,
    r=0.1,
    sigma=0.15,
    T=1)
