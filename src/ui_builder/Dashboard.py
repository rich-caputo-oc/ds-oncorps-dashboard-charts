import os

class Dashboard():

    def __init__(self, endpoint_dict):
        """
        To be structured such that
        endpoint_dict[sidebar_tab] = <list of pages>
        """
        self.imports = """
        import { CommonModule } from '@angular/common';
        import { NgModule } from '@angular/core';
        import { MaterialModule } from '../../shared/material/material.module';
        import { SharedModule } from '../../shared/shared.module';
        import { DashboardRoutingModule } from './dashboard-routing.module';
        """
        page_names = []
        for tab, page_arr in endpoint_dict.items():
            for curr in page_arr:
                scurr = curr[1:].split('/')[1]
                page_name = ''.join([x.capitalize() for x in scurr.split('-')]) + 'Page'
                self.imports += f"""
                import {{ {page_name} }} from './pages/{tab}/pages/{scurr}/{scurr}.page'
                """
                page_names.append(page_name)

        self.body = f"""
        @NgModule({{
          declarations: {str(page_names).replace("'", "")},
          imports: [
            CommonModule,
            DashboardRoutingModule,
            SharedModule,
            MaterialModule
          ]
        }})

        export class DashboardModule {{ }}
        """

    def build_ts(self):
        return self.imports + self.body

    def build_page(self, path):
        with open(f"{path}/dashboard.module.ts", 'w') as ts_file:
            ts_file.write(self.build_ts())
