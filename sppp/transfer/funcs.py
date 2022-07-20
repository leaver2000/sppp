__all__ = ["mask_a_and_b", "mask_frames_by_id"]
import pandas as pd
import numpy as np
from numpy.typing import NDArray


def mask_a_and_b(
    index_a: pd.Index, index_b: pd.Index
) -> tuple[NDArray[np.bool_], NDArray[np.bool_]]:
    """tuple ndarray where index's overlap"""
    return index_a.isin(index_b), index_b.isin(index_a)


def mask_frames_by_id(
    frame_a: pd.DataFrame, frame_b: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """mask the provided dataframes where they share a common index"""
    mask_a, mask_b = mask_a_and_b(
        frame_a.index.unique("ID"), frame_b.index.unique("ID")
    )
    return frame_a[mask_a], frame_b[mask_b]
