import os
import shutil
from .Page import Page
from .BasePage import BasePage
from .Dashboard import Dashboard
from .DashboardRouting import DashboardRouting

class PagesBuilder():
    """ Class for abstracting the page building process. """
    def __init__(self, endpoint_dict, clear_pages=False):
        self.endpoint_dict = endpoint_dict
        self.clear_pages = clear_pages

    def build_pages(self, path):
        """ Class for building out pages subfolder. """
        orig_path = path
        path += '/pages'
        if self.clear_pages:
            try:
                shutil.rmtree(path)
            except:
                pass
        try:
            os.mkdir(path)
        except:
            pass
        for tab, page_arr in self.endpoint_dict.items():
            try:
                os.mkdir(path + '/' + tab)
            except:
                pass
            curr_dir = path + '/' + tab + '/pages'
            try:
                os.mkdir(curr_dir)
            except:
                pass
            BasePage(page_arr, name=tab).build_page(curr_dir)
            for curr_page in page_arr:
                name = curr_page[1:].split('/')[1]
                base_name = curr_page[1:].split('/')[0]
                temp_path = curr_dir + '/' + name
                Page(name, base_name).build_page([curr_page], path=temp_path)
        Dashboard(self.endpoint_dict).build_page(orig_path)
        DashboardRouting(self.endpoint_dict).build_page(orig_path)
