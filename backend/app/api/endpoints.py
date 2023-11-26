from fastapi import APIRouter
from app.service.heston import heston_norm, heston_bin, heston_interval
from app.service.black_scholes import black_scholes, monte_karlo, binomial
from app.schemas import HestonCreate, BlackScholesData

router = APIRouter()


@router.post("/heston_norm")
def calculate_price_heston_norm(data: HestonCreate):
    res = heston_norm(data)
    return res


@router.post("/heston_bin")
def calculate_price_heston_bin(data: HestonCreate):
    res = heston_bin(data)
    return res


@router.post("/heston_interval")
def calculate_price_interval_heston(data: HestonCreate):
    res = heston_interval(data)
    return res


@router.post("/black_scholes")
def calculate_price_black_scholes(data: BlackScholesData):
    res = black_scholes(data)
    return res


@router.post("/black_scholes_monte_carlo")
def calculate_price_black_scholes_monte_carlo(data: BlackScholesData):
    res = monte_karlo(data)
    return res


@router.post("/black_scholes_binomial")
def calculate_price_black_scholes_binomial(data: BlackScholesData):
    res = binomial(data)
    return res