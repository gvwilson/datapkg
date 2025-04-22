import csv
from functools import cached_property
from importlib import resources

DATA_DIR = "data"
AVAILABLE = {
    "machines": {"filename": "machines.csv", "cached": None},
    "persons": {"filename": "persons.csv", "cached": None},
}


def __getattr__(name):
    if name not in AVAILABLE:
        raise AttributeError(f"{__name__} does not have {name}")
    if AVAILABLE[name]["cached"] is None:
        AVAILABLE[name]["cached"] = _load_csv(AVAILABLE[name]["filename"])
    return AVAILABLE[name]["cached"]

    
def _load_csv(filename):
    """Load data from a CSV file."""
    with resources.files(DATA_DIR).joinpath(filename).open("r") as stream:
        return [r for r in csv.reader(stream)]
