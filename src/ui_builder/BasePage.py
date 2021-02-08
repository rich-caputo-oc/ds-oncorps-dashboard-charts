import os
import jsbeautifier

class BasePage():

    def __init__(self, pages, name='user-engagement'):
        self.name = name
        self.page_top = """
        import { ViewChild } from "@angular/core";
        import { FilterComponent } from "src/app/shared/components/filter/components/filter/filter.component";
        import { IGlobalChartInstances } from "src/app/shared/components/filter/interfaces/global-chart/IGlobalChartInstances";
        import { IPageConfig } from "src/app/shared/components/shared/interfaces/page-config/IPageConfig";
        import { FileManagerService } from "src/app/shared/services/file-manager/file-manager.service";
        """
        self.page_top += f"""export abstract class {''.join([x.capitalize() for x in self.name.split('-')]) + 'BasePage'} {{"""
        self.page_top += """
          public allCharts: IGlobalChartInstances;
          public pageConfig: IPageConfig | IPageConfig[];
          public pageTitle: string;
          public shouldShowFilter: boolean;
          public navLinks: any[];

          public exportCsvUrl: string;

          @ViewChild(FilterComponent) filterRef: FilterComponent;

          constructor(protected fileManager: FileManagerService, private activeTabName: string) {
            this.navLinks = [
        """
        self.page_middle = ""
        for page in pages:
            scurr = page[1:].split('/')[1]
            self.page_middle += f"""
            {{
              path: '../{scurr}',
              label: '{' '.join([x.capitalize() for x in scurr.split('-')])}'
            }},
            """
        self.page_bot = f"""
                ];

            this.setActiveTab(activeTabName);
            this.setPageTitle('{' '.join([x.capitalize() for x in self.name.split('-')])}');
          }}

          /**
           * Toggles the filter for a chart
           */
          public toggleFilter() {{
            this.shouldShowFilter = !this.shouldShowFilter;
          }}

          /**
           * Click CSV Download button
           */
          public clickCsvDownload() {{
            this.fileManager.saveFileFromUrl(this.exportCsvUrl, 'user_actions_report.csv', 'text/csv');
          }}

          /**
           * Sets a page title
           *
           * @param pageTitle The title to set
           */
          protected setPageTitle(pageTitle: string) {{
            this.pageTitle = pageTitle;
          }}

          private setActiveTab(activeTabName: string) {{
            const activeTab = this.navLinks.filter(nav => nav.label === activeTabName)[0]

            activeTab.isActive = true;
          }}
        }}
        """

    def build_ts(self):
        return self.page_top + self.page_middle + self.page_bot

    def build_page(self, path):
        curr_dir = path + '/base'
        try:
            os.mkdir(curr_dir)
        except:
            pass
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        opts.max_preserve_newlines = 30
        with open(f"{curr_dir}/{self.name}-base.page.ts", 'w') as ts_file:
            s = jsbeautifier.beautify(self.build_ts(), opts)
            ts_file.write(s)
