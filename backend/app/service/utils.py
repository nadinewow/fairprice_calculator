from numpy import random
from app.service.variables import N


def white_noise(std=1, size=N):
    return random.normal(0, std, size)
