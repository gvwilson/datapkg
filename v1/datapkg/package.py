import csv
from functools import cached_property
from importlib import resources
import inspect
import sys
import types


class LazyModule(types.ModuleType):
    """A module that lazily loads datasets when attributes are accessed.
    
    This custom module replaces the original module and forwards attribute
    access to a loader instance.
    """
    
    def __init__(self, name, loader):
        """Initialize a LazyModule.
        
        Args:
            name: The name of the module
            loader_instance: An instance of a class that provides the datasets
        """
        super().__init__(name)
        self._loader = loader
    
    def __getattr__(self, name):
        """Get an attribute from the loader when not found in the module.
        
        Args:
            name: The name of the attribute to get
            
        Returns:
            The attribute from the loader
            
        Raises:
            AttributeError: If the attribute is not found in the loader
        """
        try:
            return getattr(self._loader, name)
        except AttributeError as exc:
            raise AttributeError(
                f"Module '{self.__name__}' has no attribute '{name}'"
            ) from exc


def create_lazy_package(package_name, loader, names=None):
    """Set up lazy loading for a data package.
    
    This function replaces the current module with a custom module that
    lazily loads datasets when their attributes are accessed.
    
    Args:
        package_name: The name of the package to modify
        loader: An instance of a class that provides the datasets
        names: A list of names to export in __all__ (None for empty).
    """
    original_module = sys.modules[package_name]
    lazy_module = LazyModule(package_name, loader)
    lazy_module.__dict__.update(original_module.__dict__)
    sys.modules[package_name] = lazy_module
    lazy_module.__all__ = [] if names is None else names


class BaseDatasetLoader:
    """Base class for dataset loaders.
    
    Extend this class to create dataset loaders with a @cached_property
    methods for each dataset.
    """

    DATA_DIR = "data"
    
    def load_csv(self, filename):
        """Load data from a CSV file.
        
        Args:
            package_name: The name of the package containing the data files
            filename: The name of the CSV file
            
        Returns:
            A list of rows from the CSV file
        """
        print(f"loading {filename}")
        with resources.files(BaseDatasetLoader.DATA_DIR).joinpath(filename).open("r") as stream:
            rows = [r for r in csv.reader(stream)]
            
        return rows
        
    @classmethod
    def discover_cached_properties(cls):
        """Discover all cached_property attributes in this class.
        
        Returns:
            A list of attribute names that are cached properties
        """
        return [
            name for name, attr in inspect.getmembers(cls)
            if (not name.startswith("_")) and isinstance(attr, cached_property)
        ]
    
    @classmethod
    def install(cls, package_name):
        """Set up lazy loading for a data package.
        
        Args:
            package_name: The name of the package to modify.
        """
        loader_instance = cls()
        exported_names = cls.discover_cached_properties()
        create_lazy_package(package_name, loader_instance, exported_names)
