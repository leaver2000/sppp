__all__ = ["GridSpace"]
import numpy as np
import pandas as pd


class GridSpace:
    def __init__(
        self, x_resolution: int = 7000, y_resolution: int = 3500, **kwargs: int
    ):
        self.__x = np.linspace(
            -129.995,
            -60.005002000040975,
            x_resolution,
            dtype=np.float32,
        )
        self.__y = np.linspace(
            54.995,
            20.005000000002696,
            y_resolution,
            dtype=np.float32,
        )  # mrms_grid(**kwargs)

        self.__zeros = pd.DataFrame(
            columns=np.arange(len(self.__x))[::-1], index=np.arange(len(self.__y))[::-1]
        ).fillna(0)

    @property
    def x(self) -> np.ndarray:
        return self.__x

    @property
    def y(self) -> np.ndarray:
        return self.__y

    def position(self, crd: tuple[float, float]) -> tuple[int, int]:
        x, y = crd
        return np.argmin(abs(self.x - x)), np.argmin(abs(self.y - y))

    def zeros_grid(self) -> pd.DataFrame:
        return self.__zeros.copy()

    def reward_matrix(self, x: int, y: int, box_size: int = 5) -> pd.DataFrame:
        def reward_map() -> np.ndarray:
            """creates 11x11 matrix"""
            a = list(np.linspace(0, 0.25, 5))
            a2 = np.array(a + [0.5] + list(reversed(a)))
            return a2 + a2[:, np.newaxis]

        gamefield = (
            self.__zeros.loc[
                y - box_size : y + box_size,
                x - box_size : x + box_size,
            ].copy()
            + reward_map()
        )
        return gamefield

    def min(self) -> tuple[float, float]:
        return self.x.min(), self.y.min()

    def max(self) -> tuple[float, float]:
        return self.x.max(), self.y.max()
