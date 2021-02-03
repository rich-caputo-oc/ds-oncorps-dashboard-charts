import os


class BasePage():

    def __init__(self, pages, name='User Engagement'):
        self.page_top = """
        import { ViewChild } from "@angular/core";
        import { FilterComponent } from "src/app/shared/components/filter/components/filter/filter.component";
        import { IGlobalChartInstances } from "src/app/shared/components/filter/interfaces/global-chart/IGlobalChartInstances";
        import { IPageConfig } from "src/app/shared/components/shared/interfaces/page-config/IPageConfig";
        import { FileManagerService } from "src/app/shared/services/file-manager/file-manager.service";

        export abstract class UserEngagementBasePage {
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
            self.page_middle += f"""
            {{
              path: '../{page}',
              label: '{' '.join([x.capitalize() for x in page.split('-')])}'
            }}
            """
        self.page_bot = f"""
                ];

            this.setActiveTab(activeTabName);
            this.setPageTitle('{self.name}');
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

    def build_page(self):
        return self.page_top + self.page_middle + self.page_bot
