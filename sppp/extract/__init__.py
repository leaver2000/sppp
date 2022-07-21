"""extract functions and classes"""
__all__ = ["ArchiveTrawler", "download_archive_data"]
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from requests import Session, HTTPError

from sppp.extract.trawler import ArchiveTrawler


def download_archive_data(
    start: str | datetime,
    end: str | datetime,
    freq: str = "2min",
    outdir: Path = Path("/home/leaver2000/sppp/archive"),
) -> None:
    """accepts a daterange and downloads probsevere data from the archive"""
    template = "https://mtarchive.geol.iastate.edu/%Y/%m/%d/mrms/ncep/ProbSevere/MRMS_PROBSEVERE_%Y%m%d_%H%M00.json"
    urls = pd.date_range(start=start, end=end, freq=freq).strftime(template)
    with Session() as session:
        for url in urls:
            try:
                r = session.get(url, stream=True)
                r.raise_for_status()
                outfile = outdir / r.url.split("/")[-1]

                with outfile.open("w") as f:
                    json.dump(r.json(), f, indent=4)

            except (ConnectionError, HTTPError):
                print("error downloading", url)
