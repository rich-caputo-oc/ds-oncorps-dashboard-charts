import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as plio

from charts.BaseChart import BaseChart

np.random.seed(3)

class ExampleChart(BaseChart):

    def get_data(self):
        """
        Gets data using MongoDB store.
        """
        if self.store['universe'].has_symbol('data'):
            return self.store['universe'].read('data').data
        # Store some example data if being run for the first time.
        data = pd.DataFrame(np.random.randn(100, 3), columns=['a', 'b', 'c'])
        self.store['universe'].write('data', data)

    def create_chart(self, data):
        """ Creates chart using example data. """
        table = [
            go.Table(
                header={
                    'values': ['a', 'b', 'c'],
                    'fill': {
                        'color': self.table_header_color
                    },
                    'align': 'left'
                },
                cells={
                    'values': [data.a, data.b, data.c],
                    'align': ['left', 'left', 'right']
                },
                columnwidth=[.1, .1, .1]
            )
        ]
        fig = dict(data=table)
        return plio.to_json(fig)
