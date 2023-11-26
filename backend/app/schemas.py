from pydantic import BaseModel


class HestonCreate(BaseModel):
    V0: float
    T: int
    k: float
    theta: float
    r: float
    S0: float
    K: float
    ro: float


class BlackScholesData(BaseModel):
    S0: float
    K: float
    r: float
    sigma: float
    T: int
