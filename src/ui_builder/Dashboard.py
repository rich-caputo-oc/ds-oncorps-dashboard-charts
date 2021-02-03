import os

class Dashboard():

    def __init__(self, endpoint_dict):
        """
        To be structured such that
        endpoint_dict[sidebar_tab] = <list of pages>
        """
        self.imports = ""
        page_names = []
        for tab, page_arr:
            if len(page_arr) == 1:
                curr = page_arr[0]
                page_name = ''.join([x.capitalize() for x in curr.split('/')[-1].split('-')]) + 'Page'
                self.imports += f"""
                import {{ {page_name} }} from './pages/{tab}/{curr}.page'
                """
                page_names.append(page_name)
            else:
                for curr in page_arr:
                    page_name = ''.join([x.capitalize() for x in curr.split('/')[-1].split('-')]) + 'Page'
                    self.imports += f"""
                    import {{ {page_name} }} from './pages/{tab}/pages/{curr}.page'
                    """
                page_names.append(page_name)

        self.body = f"""
        @NgModule({{
          declarations: {page_names},
          imports: [
            CommonModule,
            DashboardRoutingModule,
            SharedModule,
            MaterialModule
          ]
        }})

        export class DashboardModule { }
        """

    def build_ts(self):
        return self.imports + self.body
