import json
from glob import glob
from pathlib import Path
from typing import Iterator
from datetime import datetime
from warnings import warn
import pandas as pd
import numpy as np
from geopandas import GeoDataFrame

from sppp.schema import FeatureCollection

idx: slice = pd.IndexSlice


def iterpaths(glob_path: str) -> Iterator[Path]:

    yield from (Path(file) for file in sorted(glob(glob_path)))


def to_numeric(
    df: pd.DataFrame,
    string_okay: tuple[str, ...] = ("MAXRC_ICECF", "MAXRC_EMISS", "geometry"),
) -> pd.DataFrame:
    condition = df.columns[~df.columns.isin(string_okay)]
    df[condition] = df[condition].astype(np.float32)
    return df


def to_midf(glob_path: str) -> pd.DataFrame:
    """/workspaces/sppp/data/probsevere/2021/**/*.json"""

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

    # df =
    return (
        pd.concat(generate())
        .set_index(["validTime", "ID"])
        .drop(columns=["AVG_BEAM_HGT"])
        .pipe(to_numeric)
    )
