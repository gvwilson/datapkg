from functools import cached_property
from datapkg.package import BaseDatasetLoader

class _Loader(BaseDatasetLoader):
    """Example dataset loader."""

    @cached_property
    def machines(self):
        return self.load_csv("machines.csv")
    
    @cached_property
    def persons(self):
        return self.load_csv("persons.csv")

# Set up lazy loading - automatically discovers cached properties
_Loader.install(__name__)
