import os
import sys
import subprocess
import io
import json
import requests
import shutil
import yaml
from src.ui_builder.PagesBuilder import PagesBuilder
from src.ui_builder.SideNav import SideNav
from src.ui_builder.AppNamer import AppNamer


APP_NAME = 'Generic Dashboard'
BASE_UI_LINK = "https://github.com/rich-caputo-oc/ui-dashboard-generic.git"
CLEAR_PAGES = True
CONFIG_FILE = "config.yml"
HOST = "localhost:4000"
UI_REPO_NAME = 'ui-dashboard-generic'
WORKING_BRANCH = "2.x"


def fetch_generic_ui(base_ui_link=BASE_UI_LINK, ui_repo_name=UI_REPO_NAME, working_branch=WORKING_BRANCH):
    """
    Looks for ui_repo_name in current super-directory.
    Clones generic UI fro base_ui_link if not found.
    For best practice, please use your forked version of ui-dashboard-oncorps as base_ui_link.
    """
    if ui_repo_name not in os.listdir('..'):
        subprocess.run(
            f"git clone {base_ui_link} ../{ui_repo_name}".split(' '))
        os.chdir(f"../{ui_repo_name}")
        subprocess.run(f"git fetch".split(' '))
        subprocess.run(f"git checkout {working_branch}".split(' '))
        os.chdir(f"../ds-oncorps-dashboard-charts")


def get_endpoints(host=HOST):
    """ Calls /all-enpoints endpoint and keeps charting and side-nav endpoints. """
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


def get_config(config_file=CONFIG_FILE):
    config = json.dumps(yaml.load(io.open(config_file, 'r', encoding='utf8'), Loader=yaml.FullLoader))
    return config


def main():
    """ Main build_ui function. """
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
    config = get_config()
    PagesBuilder(endpoint_dict, chart_configs=config, clear_pages=CLEAR_PAGES).build_pages(path)
    SideNav(navs).build_page(side_nav_path)
    AppNamer(APP_NAME).build_pages(f'../{UI_REPO_NAME}')
    print("UI build complete!")


if __name__ == "__main__":
    main()
