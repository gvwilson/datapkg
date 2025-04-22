import csv
from functools import cached_property
from importlib import resources

DATA_DIR = "data"

class _loader:

    @cached_property
    def machines(self):
        return _load_csv("machines.csv")

    @cached_property
    def persons(self):
        return _load_csv("persons.csv")

    
def _load_csv(filename):
    """Load data from a CSV file."""
    print(f"loading {filename}")
    with resources.files(DATA_DIR).joinpath(filename).open("r") as stream:
        return [r for r in csv.reader(stream)]

datapkg = _loader()

__all__ = ["datapkg"]
