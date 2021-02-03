import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as plio

from charts.BaseChart import BaseChart

class ExampleChart(BaseChart):

    def get_data(self, symbols=['data']):
        """
        Gets data using MongoDB store.
        """
        data = [
            self.store['universe'].read(s).data for s in symbols
            if self.store['universe'].has_symbol(s)
        ]
        return pd.concat(data, axis=1)

    def create_chart(self, data):
        """ Creates chart using example data. """
        table = [
            go.Table(
                header={
                    'values': list(data.columns),
                    'fill': {
                        'color': self.table_header_color
                    },
                    'align': 'left'
                },
                cells={
                    'values': [data[c] for c in data.columns],
                    'align': ['right' for c in data.columns]
                },
                columnwidth=[.1 for c in data.columns]
            )
        ]
        fig = dict(data=table)
        return plio.to_json(fig)
