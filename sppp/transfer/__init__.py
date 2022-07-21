__all__ = ["to_midf"]
import json
from glob import glob
from pathlib import Path
from warnings import warn
from datetime import datetime
from typing import Iterator

import pandas as pd
import numpy as np
from geopandas import GeoDataFrame

from sppp.schema import FeatureCollection

idx: slice = pd.IndexSlice


def iterpaths(glob_path: str) -> Iterator[Path]:
    yield from (Path(file) for file in glob(glob_path))


def coord_lister(geom: pd.Series) -> list[tuple[float, float]]:
    coords = list(geom.exterior.coords)
    return coords


def to_numeric(df: pd.DataFrame, dont_float: tuple[str, ...]):

    condition = df.columns[~df.columns.isin(dont_float)]
    df[condition] = df[condition].astype(np.float32)
    return df


def to_midf(glob_path: str, raw_crds=True) -> pd.DataFrame:
    def generate():
        for path in iterpaths(glob_path):
            with path.open("rb") as f:
                try:
                    fc: FeatureCollection = json.load(f)
                except json.JSONDecodeError:
                    warn(f"json error decoding {path}")
                    continue
                df: GeoDataFrame = GeoDataFrame.from_features(fc["features"])
                df["validTime"] = datetime.strptime(fc["validTime"], "%Y%m%d_%H%M%S %Z")
                yield df

    dont_float = ("MAXRC_EMISS", "MAXRC_ICECF", "geometry")

    df = (
        pd.concat(generate())
        .drop(columns="AVG_BEAM_HGT")
        .set_index(["validTime", "ID"])
        .pipe(to_numeric, dont_float)
    )

    if raw_crds:
        df["geometry"] = df["geometry"].apply(coord_lister)

    return df
