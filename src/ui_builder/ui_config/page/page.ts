import {
  Component,
  OnDestroy,
  OnInit
} from "@angular/core";
import {
  IDashboard
} from "src/app/interfaces/IDashboard";
import {
  RenderType
} from "src/app/shared/components/chart/enums/render-type/render-type.enum";
import {
  FilterType
} from "src/app/shared/components/filter/enums/filter-type/filter-type.enum";
import {
  IGlobalChartInstances
} from "src/app/shared/components/filter/interfaces/global-chart/IGlobalChartInstances";
import {
  IPageConfig
} from "src/app/shared/components/shared/interfaces/page-config/IPageConfig";
import {
  FileManagerService
} from "src/app/shared/services/file-manager/file-manager.service";
import {
  FilterService
} from "src/app/shared/services/filter/filter.service";
import {
  environment
} from "src/environments/environment";

PAGE_IMPORTS

COMPONENT

export class PAGE_CLASS extends BASE_PAGE_CLASS implements OnInit, IDashboard, OnDestroy {
  constructor(fileManager: FileManagerService, private filterService: FilterService) {
    super(fileManager, PAGE_NAME);
  }

  setupPageConfiguration(): IPageConfig {
    const ocDataScienceBaseUrl = environment.ocDataScienceBaseUrl;
    const colorway = COLORWAY;


    return CHARTS;
  }

  setupAllChartData(): IGlobalChartInstances {
    return {
      charts: ( < IPageConfig > this.pageConfig).tiles.map(tile => tile.charts)[0],
      filterRef: this.filterRef,
      filterConfig: {
        filters: [{
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
        }, {
          name: 'User type',
          options: [{
            value: 'all',
            label: 'All',
            default: true
          }, {
            value: 'external',
            label: 'External',
            default: false
          }, {
            value: 'internal',
            label: 'Internal',
            default: false
          }],
          type: FilterType.PREDEFINED,
          fieldName: 'user_type',
          created: new Date()
        }]
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

}
