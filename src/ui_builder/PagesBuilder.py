import os
from .Page import Page
from .BasePage import BasePage
from .Dashboard import Dashboard
from .DashboardRouting import DashboardRouting

class PagesBuilder():
    """ Class for abstracting the page building process. """
    def __init__(self, endpoint_dict):
        print(os.getcwd())
        self.endpoint_dict = endpoint_dict

    def build_pages(self, path):
        """ Class for building out pages subfolder. """
        orig_path = path
        path += '/pages'
        for tab, page_arr in self.endpoint_dict.items():
            curr_dir = path + '/' + tab + '/pages'
            try:
                os.mkdir(curr_dir)
            except:
                pass
            BasePage(page_arr, name=tab).build_page(curr_dir)
            for curr_page in page_arr:
                name = curr_page[1:].split('/')[1]
                temp_path = curr_dir + '/' + name
                Page(name).build_page([curr_page], path=temp_path)
        Dashboard(self.endpoint_dict).build_page(orig_path)
        DashboardRouting(self.endpoint_dict).build_page(orig_path)

if __name__ == "__main__":
    pb = PagesBuilder({})
