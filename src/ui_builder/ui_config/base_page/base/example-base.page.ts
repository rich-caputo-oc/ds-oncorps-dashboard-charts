import {
  ViewChild
} from "@angular/core";
import {
  FilterComponent
} from "src/app/shared/components/filter/components/filter/filter.component";
import {
  IGlobalChartInstances
} from "src/app/shared/components/filter/interfaces/global-chart/IGlobalChartInstances";
import {
  IPageConfig
} from "src/app/shared/components/shared/interfaces/page-config/IPageConfig";
import {
  FileManagerService
} from "src/app/shared/services/file-manager/file-manager.service";
export abstract class example {
  public allCharts: IGlobalChartInstances;
  public pageConfig: IPageConfig | IPageConfig[];
  public pageTitle: string;
  public shouldShowFilter: boolean;
  public navLinks: any[];
  public exportCsvUrl: string;
  @ViewChild(FilterComponent) filterRef: FilterComponent;
  constructor(protected fileManager: FileManagerService, private activeTabName: string) {
    this.navLinks = [{
      path: '../example-header',
      label: 'Example Header'
    }, ];
    this.setActiveTab(activeTabName);
    this.setPageTitle('Example');
  } /**   * Toggles the filter for a chart   */
  public toggleFilter() {
    this.shouldShowFilter = !this.shouldShowFilter;
  } /**   * Click CSV Download button   */
  public clickCsvDownload() {
    this.fileManager.saveFileFromUrl(this.exportCsvUrl, 'user_actions_report.csv', 'text/csv');
  } /**   * Sets a page title   *   * @param pageTitle The title to set   */
  protected setPageTitle(pageTitle: string) {
    this.pageTitle = pageTitle;
  }
  private setActiveTab(activeTabName: string) {
    const activeTab = this.navLinks.filter(nav => nav.label === activeTabName)[0] activeTab.isActive = true;
  }
}