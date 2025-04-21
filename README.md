# DataPkg

A simple Python data package with lazy loading.

## Installation

```bash
pip install .
```

## Usage

```python
import datapkg

# Access datasets as attributes (lazy loading)
print(datapkg.machines)
print(datapkg.persons)
```

## Available Datasets

- `machines`: some machines (CSV)
- `persons`: some people (CSV)

## Creating Your Own Data Package

To create your own data package:

1. Install this package: `pip install datapkg`

2. Create a Python package with your CSV files:

```
mydata/
├── __init__.py
├── data/
│   ├── students.csv
│   └── courses.csv
```

3. Define your dataset loader in `__init__.py`:

```python
from functools import cached_property
from datapkg.package import BaseDatasetLoader

class MyDataLoader(BaseDatasetLoader):
    """Custom dataset loader."""
    
    @cached_property
    def students(self):
        """Load students.csv data."""
        return self.load_csv("mydata.data", "students.csv")
    
    @cached_property
    def courses(self):
        """Load courses.csv data."""
        return self.load_csv("mydata.data", "courses.csv")

# Set up lazy loading - automatically discovers all @cached_property methods
MyDataLoader.install()
```

4. Use your data package:

```python
import mydata

# Data is loaded only when accessed
print(mydata.students)  # Loads and returns students data
print(mydata.courses)   # Loads and returns courses data
```
