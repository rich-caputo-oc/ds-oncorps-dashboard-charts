import os
import jsbeautifier

class DashboardRouting():

    def __init__(self, endpoint_dict, redirect='example-endpoints'):
        """
        To be structured such that
        endpoint_dict[sidebar_tab] = <list of pages>
        """
        self.imports = """
        import { NgModule } from '@angular/core';
        import { RouterModule, Routes } from '@angular/router';
        import { AuthGuardService } from 'src/app/core/auth/auth-guard.service';
        """
        self.routes = self.routes = """
        const routes: Routes = [
        """
        for tab, page_arr in endpoint_dict.items():
            self.routes += f"""
            {{
              path: '{tab}',
              canActivate: [AuthGuardService],
              children: [{{
                path: '',
                pathMatch: 'full',
                redirectTo: '{redirect}'
              }},
            """
            for curr in page_arr:
                scurr = curr[1:].split('/')[1]
                page_name = ''.join([x.capitalize() for x in scurr.split('-')]) + 'Page'
                self.imports += f"""
                import {{ {page_name} }} from './pages/{tab}/pages/{scurr}/{scurr}.page'
                """
                self.routes += f"""
                {{
                  path: '{scurr}', component: {page_name}
                }},
                """
            self.routes += ']},'

        self.lower_body = """
        ];

        @NgModule({
          imports: [
            RouterModule.forRoot(routes)
          ],
          exports: [
            RouterModule
          ]
        })

        export class DashboardRoutingModule { }

        """

    def build_ts(self):
        return self.imports + self.routes + self.lower_body

    def build_page(self, path):
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        opts.max_preserve_newlines = 30
        with open(f"{path}/dashboard-routing.module.ts", 'w') as ts_file:
            ts_file.write(jsbeautifier.beautify(self.build_ts(), opts))
