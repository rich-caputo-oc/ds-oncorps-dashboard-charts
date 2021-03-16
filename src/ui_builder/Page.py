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
        self.component = f"""
        @Component({{
          selector: 'app-{self.name}',
          templateUrl: './{self.name}.page.html',
          styleUrls: ['./{self.name}.page.scss']
        }})
        """
        ### Get page defaults if necessary ###
        if imports is None:
            imports = """
            import { Component, OnDestroy, OnInit } from "@angular/core";
            import { IDashboard } from "src/app/interfaces/IDashboard";
            import { RenderType } from "src/app/shared/components/chart/enums/render-type/render-type.enum";
            import { FilterType } from "src/app/shared/components/filter/enums/filter-type/filter-type.enum";
            import { IGlobalChartInstances } from "src/app/shared/components/filter/interfaces/global-chart/IGlobalChartInstances";
            import { IPageConfig } from "src/app/shared/components/shared/interfaces/page-config/IPageConfig";
            import { FileManagerService } from "src/app/shared/services/file-manager/file-manager.service";
            import { FilterService } from "src/app/shared/services/filter/filter.service";
            import { environment } from "src/environments/environment";
            """
            imports += f"""
            import {{ {''.join([x.capitalize() for x in self.base_name.split('-')]) + 'BasePage'} }} from '../base/{self.base_name}-base.page';
            """

        if html is None:
            html = """
<div class="dashboard-content">
    <div class="dashboard-content__header">
      <h1>{{ pageTitle }}</h1>

      <oc-filter [globalChartInstances]="allCharts"></oc-filter>
    </div>

    <nav mat-tab-nav-bar>
      <a mat-tab-link
         *ngFor="let link of navLinks"
         [routerLink]="link.path"
         [active]="link.isActive">
         {{link.label}}
      </a>
    </nav>

    <oc-dashboard [pageConfig]="pageConfig"></oc-dashboard>

    <div class="dashboard--actions">
      <button mat-raised-button (click)="clickCsvDownload()">
        <mat-icon>arrow_downward</mat-icon> Download as CSV
      </button>
    </div>
  </div>
            """
        if scss is None:
            scss = """
            :host {
              display: block;

              & > .dashboard-content {
                margin: 24px;

                .dashboard-content__header {
                  display: flex;
                  align-items: baseline;
                  justify-content: space-between;
                  margin-bottom: 24px;
                }
              }
            }

            .dashboard--actions {
              margin: 24px;
              text-align: center;
            }
            """
        if colorway is None:
            colorway = ['#000000', '#FFDB00', '#797878', '#2ca02c',
                        '#d62728', '#9467bd', '#8c564b', '#e377c2']
        self.imports = imports
        self.html = html
        self.scss = scss
        self.colorway = colorway

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
        ts = """
        setupAllChartData(): IGlobalChartInstances {
        return {
          charts: (<IPageConfig>this.pageConfig).tiles.map(tile => tile.charts)[0],
          filterRef: this.filterRef,
          filterConfig: {
            filters: [
              {
                name: 'Date range',
                options: [],
                type: FilterType.DATE_PICKER,
                dateRangeEnabled: true,
                dateRangeDefaultInDays: 90,
                fieldName: 'date_range',
                transientFieldNames: [
                  'date_from',
                  'date_to'
                ],
                created: new Date()
              },
              {
                name: 'User type',
                options: [
                  {
                    value: 'all',
                    label: 'All',
                    default: true
                  },
                  {
                    value: 'external',
                    label: 'External',
                    default: false
                  },
                  {
                    value: 'internal',
                    label: 'Internal',
                    default: false
                  }
                ],
                type: FilterType.PREDEFINED,
                fieldName: 'user_type',
                created: new Date()
              }
            ]
          }
        };
        }

        ngOnInit() {
        this.pageConfig = this.setupPageConfiguration();
        this.allCharts = this.setupAllChartData();
        this.exportCsvUrl = environment.ocDataScienceBaseUrl + '/export/user_actions_report';
        }

        ngOnDestroy() {
        this.filterService.flushChartSpecificFilters();
        }
        """
        return ts

    def get_imports(self):
        return self.imports

    def get_component(self):
        return self.component

    def get_page_config(self, endpoints, chart_config=None):
        """ Joins each chart to build page config. """
        page_config = """
        return {
          tiles: [
        """
        for endpoint in endpoints:
            page_config += self.dashboardify(endpoint, chart_config=chart_config)
        return page_config[:-1] + ']}'

    def build_ts(self, endpoints, chart_config=None):
        c_name = ''.join([x.capitalize()
                          for x in self.name.split('-')]) + 'Page'
        b_name = ''.join([x.capitalize() for x in self.base_name.split('-')]) + 'BasePage'
        return f"""
        {self.imports}

        {self.component}

        export class {c_name} extends {b_name} implements OnInit, IDashboard, OnDestroy {{
          constructor(fileManager: FileManagerService, private filterService: FilterService) {{
            super(fileManager, '{' '.join([x.capitalize() for x in self.name.split('-')])}');
          }}

          setupPageConfiguration(): IPageConfig {{
            const ocDataScienceBaseUrl = environment.ocDataScienceBaseUrl;
            const colorway = {self.colorway};

            {self.get_page_config(endpoints, chart_config)};
          }}
            {self.build_filters()}
        }}
        """

    def build_page(self, endpoints, path, chart_config=None):
        curr_dir = path
        try:
            os.mkdir(curr_dir)
        except:
            pass
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        opts.max_preserve_newlines = 30
        # Save HTML file
        with open(f"{curr_dir}/{self.name}.page.html", 'w') as html_file:
            html_file.write(self.html)
        # Save SCSS file
        with open(f"{curr_dir}/{self.name}.page.scss", 'w') as scss_file:
            scss_file.write(cssbeautifier.beautify(self.scss, opts))
        # Save TypeScript file
        with open(f"{curr_dir}/{self.name}.page.ts", 'w') as ts_file:
            ts_file.write(jsbeautifier.beautify(
                self.build_ts(endpoints, chart_config), opts))
