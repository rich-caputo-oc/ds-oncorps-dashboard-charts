import logging
from abc import ABC, abstractmethod

import pandas as pd


class BaseChart(ABC):
    """
    This is the base class for charts.
    """

    def __init__(self, store, filters=None, table_header_color='#a1c6e1'):
        """
        -Each chart has a MongoDB Arctic connection (store).
        -Each child class must supply get_data() and create_chart() methods.
            -These methods are used by the render_chart() method to produce the chart in JSON format.
        """
        self.store = store
        self.filters = filters
        self.table_header_color = table_header_color

    def render_chart(self) -> str:
        """
        Coordinates the creation of a chart and returns
        a plotly chart in JSON format.
        """
        data = self.get_data()
        chart_json = self.create_chart(data)
        return chart_json

    @abstractmethod
    def get_data(self, name='data', lib='universe') -> pd.DataFrame:
        """
        Queries the MongoDB Arctic connection to get data.
        """
        pass

    @abstractmethod
    def create_chart(self, data: pd.DataFrame) -> str:
        """
        Takes Pandas DataFrame from get_data
        and produces a plotly chart in JSON format.
        """
        pass

    def apply_page_filters(self, query):
        """ Applies global filters. """
        return query

    def apply_chart_filters(self, query):
        """ Applies chart-specific filters. """
        return query
