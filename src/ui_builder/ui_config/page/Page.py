import os
import jsbeautifier
import cssbeautifier
import pprint
from bs4 import BeautifulSoup


class Page():
    """ Class for building a page. """

    def __init__(self, name, base_name, imports=None, html=None, scss=None, colorway=None, chart_config=None):
        self.name = name
        self.base_name = base_name
        self.ts_var_lookup = {}
        self.ts_var_lookup['PAGE_NAME'] = name
        self.ts_var_lookup['COMPONENT'] = f"""
        @Component({{
          selector: 'app-{self.name}',
          templateUrl: './{self.name}.page.html',
          styleUrls: ['./{self.name}.page.scss']
        }})
        """
        self.ts_var_lookup['BASE_PAGE_CLASS'] = ''.join([x.capitalize() for x in self.base_name.split('-') + 'BasePage'
        self.ts_var_lookup['PAGE_IMPORTS'] = f"""
        import {{ {self.ts_var_lookup['BASE_PAGE_CLASS']} }} from '../base/{self.base_name}-base.page';
        """
        if colorway is None:
            self.ts_var_lookup['COLORWAY'] = [
            '#000000', '#FFDB00', '#797878', '#2ca02c',
            '#d62728', '#9467bd', '#8c564b', '#e377c2'
        ]
        else:
            self.ts_var_lookup['COLORWAY'] = colorway

    def dashboardify(self, endpoint, chart_config=None):
        """ Maps endpoint to dashboard-like python object. """
        chart_title = ' '.join([x.capitalize() for x in endpoint.split('/')[-1].split('-')])
        if chart_config is None:
            dashboard = f"""
            {{
              shouldShow: true,
              cols: 2,
              elevated: true,
              charts: [
                {{
                  id: 1,
                  overrides: {{
                    layout: {{
                      margin: {{
                        t: 10
                      }},
                      title: {{}},
                      colorway: colorway,
                    }}
                  }},
                  chartTitle: '{chartTitle}',
                  endpoint: ocDataScienceBaseUrl + '{endpoint}',
                  enableGlobalFiltration: true,
                  renderAs: RenderType.PLOTLY,
                  chartConfig: {{
                    displayModeBar: false,
                    responsive: true
                  }},
                  shouldShow: true
                }}
              ]
            }},
            """
        else:
            dashboard = chart_config
            dashboard['charts'][0]['chartTitle'] = chart_title
            dashboard['charts'][0]['endpoint'] = 'ocDataScienceBaseUrl' + endpoint
            dashboard = str(dashboard).replace("'", "").replace("True", "true").replace("False", "false")
        return dashboard

    def build_filters(filters=None):
        """
        Builds filter related ts.
        """
        pass

    def get_page_config(self, endpoints, chart_config=None):
        """ Joins each chart to build page config. """
        self.ts_var_lookup['CHARTS'] = """
        {
          tiles: [
        """
        for endpoint in endpoints:
            self.ts_var_lookup['CHARTS'] += self.dashboardify(endpoint, chart_config=chart_config)
        self.ts_var_lookup['CHARTS'] = self.ts_var_lookup['CHARTS'][:-1] + ']}'

    def build_ts(self, endpoints, chart_config=None, ts_load_file="base_page.ts"):
        self.get_page_config(endpoints, chart_config)
        with open(ts_load_file, 'r') as ts_file:
            data = ts_file.read()
            data = data.replace('\n', '')
        for key, val in self.ts_var_lookup.items():
            # print(key, val)
            data = data.replace(key, val)
        return data

    def build_page(self, endpoints, path, chart_config=None):
        curr_dir = path
        try:
            os.mkdir(curr_dir)
        except:
            pass
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        opts.max_preserve_newlines = 30
        # Save TypeScript file
        with open(f"{curr_dir}/{self.name}.page.ts", 'w') as ts_file:
            ts_file.write(jsbeautifier.beautify(
                self.build_ts(endpoints, chart_config), opts))
