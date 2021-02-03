import os
import sys
import subprocess
import json
import requests
from src.ui_builder.UserEngagementPage import UserEngagementPage

UI_REPO_NAME = 'ui-dashboard-oncorps'
HOST = "localhost:4000"


def fetch_generic_ui(ui_repo_name=UI_REPO_NAME):
    if ui_repo_name not in os.listdir('..'):
        subprocess.run(
            f"git clone https://github.com/OnCorps/ui-dashboard-generic ../{ui_repo_name}".split(' '))


def get_chart_endpoints(host=HOST):
    endpoints = requests.get(f'http://{host}/all_endpoints').content
    endpoints = endpoints.decode('utf8').replace("'", '"')
    endpoints = json.loads(endpoints)
    chart_endpoints = []
    for endpoint in endpoints:
        sp_endpoint = endpoint[1:].split('/')
        if len(sp_endpoint) >= 2 and sp_endpoint[0] not in ['data_endpoints', 'model_endpoints', 'static']:
            chart_endpoints.append(endpoint)
    return chart_endpoints


if __name__ == "__main__":
    fetch_generic_ui()
    path = f'../{UI_REPO_NAME}/src/app/modules/dashboard/pages/user-engagement/pages'
    chart_endpoints = get_chart_endpoints()
    blueprints = {}
    for endpoint in chart_endpoints:
        bp = endpoint.split('/')[1]
        if bp not in blueprints:
            blueprints[bp] = [endpoint]
        else:
            blueprints[bp].append(endpoint)

    for k, v in blueprints.items():
        page = UserEngagementPage(k)
        page.build_page(v, path=path)
