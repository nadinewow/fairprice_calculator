import math
import random
import numpy as np

from app.schemas import HestonCreate
from app.service.utils import white_noise
from app.service.variables import *


def heston_norm(data: HestonCreate):
    h = data.T/N
    sum_f = 0

    for i in range(M):
        eps1 = white_noise()
        eps2 = white_noise()
        for i in range(N):
            eps2[i] = eps1[i] * data.ro + eps2[i] * math.sqrt(1 - data.ro ** 2)

        V = data.V0
        y = y0
        for i in range(1, N):

            y += ((data.r - V / 2) * h + math.sqrt(V * h) * eps1[i])
            V += data.k * (data.theta - V) * h + sigma * math.sqrt(V * h) * eps2[i]

        S = data.S0 * math.exp(y)
        sum_f += (max(S - data.K, 0))

    C = math.exp(-data.r * data.T) * sum_f / M
    return C


# #
# def heston_norm(data: HestonCreate):
#
#     sum_f = 0
#     arr = []
#     N_ = np.arange(0, 50, 1)
#     N_ = list(N_)
#     for N in N_:
#         sum_f = 0
#         print(N)
#         h = data.T / N
#         for i in range(M):
#             eps1 = white_noise(1, N)
#             eps2 = white_noise(1, N)
#             for i in range(N):
#                 eps2[i] = eps1[i] * data.ro + eps2[i] * math.sqrt(1 - data.ro ** 2)
#
#             V = data.V0
#             y = y0
#             for i in range(1, N - 1):
#
#                 y += ((data.r - V / 2) * h + math.sqrt(V * h) * eps1[i])
#                 V += data.k * (data.theta - V) * h + sigma * math.sqrt(V * h) * eps2[i]
#
#             S = data.S0 * math.exp(y)
#             sum_f += (max(S - data.K, 0))
#
#         C = math.exp(-data.r * data.T) * (sum_f / M)
#         arr.append(C)
#         print(C)
#     plt.xlabel("N")
#     plt.ylabel("ylabel")
#     plt.plot(N_, arr)
#     plt.show()
#     # return(C)
# def heston_norm(data: HestonCreate):
#     h = data.T/N
#     sum_f = 0
#     arr = []
#     for k in range(100):
#         sum_f = 0
#         for i in range(M):
#             eps1 = white_noise()
#             eps2 = white_noise()
#             for i in range(N):
#                 eps2[i] = eps1[i] * data.ro + eps2[i] * math.sqrt(1 - data.ro ** 2)
#
#             V = data.V0
#             y = y0
#             for i in range(1, N - 1):
#
#                 y += ((data.r - V / 2) * h + math.sqrt(V * h) * eps1[i])
#                 V += data.k * (data.theta - V) * h + sigma * math.sqrt(V * h) * eps2[i]
#
#             S = data.S0 * math.exp(y)
#             sum_f += (max(S - data.K, 0))
#
#         C = math.exp(-data.r * data.T) * (sum_f / M)
#         arr.append(C)
#
#     plt.plot(arr)
#     print(min(arr))
#     plt.show()
#     # return(C)


def heston_interval(data: HestonCreate):
    arr = []
    for k in range(100):
        C = heston_norm(data)
        arr.append(C)
    return arr, [min(arr), max(arr)]


def heston_bin(data: HestonCreate):
    h = data.T / N
    sum_f = 0
    for i in range(M):
        V = data.V0
        y = y0
        delta_values = [1, 0]
        for n in range(1, N):
            p1 = 1/2 + (data.r - V/2) * math.sqrt(h) / (2 * math.sqrt(V))
            p2 = 1/2 + data.k * (data.theta - V) * math.sqrt(h) / (2 * sigma * math.sqrt(V))
            delta1 = random.choices(delta_values, weights=[p1, 1 - p1])[0]
            if delta1 == 1:
                delta2 = random.choices(delta_values, weights=[data.ro / p1 + p2, 1 - (data.ro / p1 + p2)])[0]
            else:
                delta2 = random.choices(delta_values, weights=[p2 - data.ro / (1 - p1), 1 - (p2 - data.ro / (1 - p1))])[0]

            y += math.sqrt(V * h) * (-1)**(1 + delta1)
            V += sigma * math.sqrt(V * h) * (-1)**(1 + delta2)

        S = data.S0 * math.exp(y)
        sum_f += (max(S - data.K, 0))

    C = math.exp(-data.r * data.T) * sum_f / M

    return(C)

d = HestonCreate(
    V0=0.05,
    T=1,
    k=0.25,
    theta=0.25,
    r=0.1,
    S0=5,
    K=1,
    ro=0.5
)
