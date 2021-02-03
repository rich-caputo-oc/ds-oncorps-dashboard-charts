import numpy as np
import pandas as pd

from typing import Dict

np.random.seed(3)

class DataETL():
    """
    This is a class for interacting with data
    """

    def __init__(self, store, lib='universe', reinit=True):
        """
        -MongoDB Arctic connection (store).
        """
        self.store = store
        self.lib = lib
        libs = set(self.store.list_libraries())
        if reinit:
            self.store.delete_library(self.lib)
        if self.lib not in libs or reinit:
            self.store.initialize_library(self.lib)

    def extract(self, **kwargs) -> Dict[str, pd.DataFrame]:
        """ Extracts data as dictionary of DataFrames. """
        # The following is an example.
        # Usually, we will need to extract from a (raw) source
        data = pd.DataFrame(np.random.randn(100, 1), columns=['X'])
        data['y'] = 3 * data['X'] + 0.1 * np.random.randn(100)
        return {'data': data}

    def transform(self, data_dict, **kwargs) -> Dict[str, pd.DataFrame]:
        """ Transforms provided dictionary of data_frames. """
        # Intermediate transformation steps would go here
        return data_dict

    def load(self, data_dict):
        """ Loads data using provided data_dict. """
        for name, data in data_dict.items():
            self.store[self.lib].write(name, data)

    def etl(self, **kwargs):
        """ Performs ETL pipeline. """
        data_dict = self.extract(**kwargs)
        data_dict = self.transform(data_dict, **kwargs)
        self.load(data_dict)
