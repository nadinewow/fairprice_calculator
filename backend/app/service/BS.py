import math
import sympy as sym


def fill_matrix(h, y0, level, S0, K, sigma):
    res = [[None for i in range(2**(level))] for j in range(level + 1)]
    res[0][0] = y0
    for i in range(1, level + 1):
        for j in range(0, 2**i, 2):
            res[i][j] = res[i - 1][j // 2] - sigma * math.sqrt(h)
            res[i][j + 1] = res[i - 1][j // 2] + sigma * math.sqrt(h)

    for j in range(len(res[0])):
        res[-1][j] = sym.Max(S0 * sym.exp(res[-1][j]) - K, 0)

    return res


def probability(level, p):
    res = [[None for i in range(2 ** (level))] for j in range(level + 1)]
    res[0][0] = 1
    for i in range(1, level + 1):
        for j in range(0, 2 ** i, 2):
            res[i][j] = res[i - 1][j // 2] * (1 - p)
            res[i][j + 1] = res[i - 1][j // 2] * p
    return res


def black_sholes_interval(r, T, N, S0, K):
    sigma = sym.Symbol('sigma', real=True)
    interv = sym.Interval(0.05, 0.15)
    lower_bound = 0.05
    upper_bound = 0.15
    h = T/N
    res = 0
    p = 0.5 + (r - sigma ** 2 / 2) * math.sqrt(h) / (2 * sigma)
    matrix = fill_matrix(h, 0, N, S0, K, sigma)
    prob = probability(N, p)

    for j in range(len(matrix[0])):
        # print(matrix[-1][j],'----', prob[-1][j])
        res += matrix[-1][j] * prob[-1][j]
    sym.plot(res, (sigma, 0.05, 0.15),axis_center=(0.05,0.52))
    res_min = res.subs(sigma, 0.05).evalf()
    res_max = res.subs(sigma, 0.15).evalf()

    C_lower = math.exp(-r * T) * res_min
    C_upper = math.exp(-r * T) * res_max
    print(C_lower, C_upper)
    # zeros = sym.solveset(res, sigma, domain=interv)
    # res_min = sym.Min(res.subs(sigma, lower_bound), res.subs(sigma, upper_bound), *[res.subs(sigma, i) for i in zeros])
    # res_max = sym.Max(res.subs(sigma, lower_bound), res.subs(sigma, upper_bound), *[res.subs(sigma, i) for i in zeros])
    # print(res_min, res_max)
    # inf = sym.calculus.util.minimum(res, sigma, interv)
    # sup = sym.calculus.util.maximum(res, sigma, interv)
    # print(inf, sup)

#
# black_sholes_interval(0.1, 1, 10, 5, 5)