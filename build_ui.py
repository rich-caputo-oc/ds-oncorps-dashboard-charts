import os
import sys
import subprocess
import json
import requests
import shutil
from src.ui_builder.PagesBuilder import PagesBuilder
from src.ui_builder.SideNav import SideNav


HOST = "localhost:4000"
UI_REPO_NAME = 'ui-dashboard-oncorps'
BASE_UI_LINK = "https://github.com/OnCorps/ui-dashboard-generic"
CLEAR_PAGES = True


def fetch_generic_ui(base_ui_link=BASE_UI_LINK, ui_repo_name=UI_REPO_NAME):
    if ui_repo_name not in os.listdir('..'):
        subprocess.run(
            f"git clone {base_ui_link} ../{ui_repo_name}".split(' '))


def get_endpoints(host=HOST):
    endpoints = requests.get(f'http://{host}/all-endpoints').content
    endpoints = endpoints.decode('utf8').replace("'", '"')
    endpoints = json.loads(endpoints)
    chart_endpoints = []
    navs = []
    for endpoint in endpoints:
        sp_endpoint = endpoint[1:].split('/')
        if len(sp_endpoint) >= 2 and sp_endpoint[0] not in ['side-nav', 'data-endpoints', 'model-endpoints', 'filter-endpoints', 'static']:
            chart_endpoints.append(endpoint)
        if sp_endpoint[0] == 'side-nav':
            nav = requests.get(f'http://{host}{endpoint}').content
            nav = nav.decode('utf8').split(',')
            navs.append(nav)
    return chart_endpoints, sorted(navs, key=lambda x: x[-1])


if __name__ == "__main__":
    fetch_generic_ui()
    path = f'../{UI_REPO_NAME}/src/app/modules/dashboard'
    side_nav_path = f'../{UI_REPO_NAME}/src/app/shared/components/side-nav'
    chart_endpoints, navs = get_endpoints()
    endpoint_dict = {}
    for endpoint in chart_endpoints:
        total = endpoint[1:].split('/')
        bp = total[0]
        tail = endpoint
        if bp not in endpoint_dict:
            endpoint_dict[bp] = [tail]
        else:
            endpoint_dict[bp].append(tail)
    PagesBuilder(endpoint_dict, clear_pages=CLEAR_PAGES).build_pages(path)
    SideNav(navs).build_page(side_nav_path)
    print("UI build complete!")
