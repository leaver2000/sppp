__all__ = ["GridSpace"]
import numpy as np


def mrms_grid(x_res: int = 7000, y_res: int = 3500):
    x = np.linspace(-129.995, -60.005002000040975, x_res)
    y = np.linspace(54.995, 20.005000000002696, y_res)
    return x, y


class GridSpace:
    def __init__(self, **kwargs: int):
        self.__x, self.__y = mrms_grid(**kwargs)

    @property
    def x(self) -> np.ndarray:
        return self.__x

    @property
    def y(self) -> np.ndarray:
        return self.__y

    def position(self, crd: tuple[float, float]) -> tuple[int, int]:
        x, y = crd
        return np.argmin(abs(self.x - x)), np.argmin(abs(self.y - y))

    def min(self) -> tuple[float, float]:
        return self.x.min(), self.y.min()

    def max(self) -> tuple[float, float]:
        return self.x.max(), self.y.max()
