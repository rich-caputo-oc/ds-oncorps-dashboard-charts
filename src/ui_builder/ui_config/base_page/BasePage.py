import os
import jsbeautifier

class BasePage():

    def __init__(self, pages, base_page_name):
        self.name = base_page_name
        self.ts_var_lookup = {}
        self.ts_var_lookup['BASE_PAGE_NAME'] = base_page_name
        self.ts_var_lookup['NAV_LINKS']  = "["
        for page in pages:
            scurr = page[1:].split('/')[1]
            self.ts_var_lookup['NAV_LINKS'] += f"""
            {{
              path: '../{scurr}',
              label: '{' '.join([x.capitalize() for x in scurr.split('-')])}'
            }},
            """
        self.ts_var_lookup['NAV_LINKS'] += "]"
        self.ts_var_lookup['BASE_PAGE_TITLE'] = ' '.join([x.capitalize() for x in base_page_name.split('-')])
        self.ts_var_lookup['BASE_PAGE_TITLE'] = f"'{self.ts_var_lookup['BASE_PAGE_TITLE']}'"

    def build_ts(self, ts_load_file="base_page.ts"):
        with open(ts_load_file, 'r') as ts_file:
            data = ts_file.read()
            data = data.replace('\n', '')
        for key, val in self.ts_var_lookup.items():
            print(key, val)
            data = data.replace(key, val)
        return data

    def build_page(self, path=os.getcwd()):
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


if __name__ == '__main__':
    base_page = BasePage(pages=['/example-sidebar/example-header/example-chart'], base_page_name='example')
    base_page.build_page()
