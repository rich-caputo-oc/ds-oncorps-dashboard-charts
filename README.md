# ds-oncorps-charts

### Set up
- Navigate to this repo and run `pip install -r requirements.txt` (necessary for `build_ui.py` but likely pre-installed)
- Copy `docker-compose.yml` to `docker-compose.override.yml` and fill in necessary keys
- `docker-compose build`
- `docker-compose up` with optional `-d` parameter to run detached
- If not in a local dev environment, change `FLASK_DEBUG: 0` in `docker-compose.override.yml`
- Run `localhost:4000/data-endpoints/etl` to refresh data
- Chart calls are of the form: `localhost:4000/<sidebar-tab>/<top-tab>/<endpoint-name>` (very important! `build_ui.py` relies on this). Sidebar tabs should have their own blueprints to maintain organization
- Run `python build_ui.py` after making any changes to charting endpoints
- Run ui container (see https://github.com/rich-caputo-oc/ui-dashboard-oncorps for more details)


### Endpoints
Definitions/routes are contained in the `/src/blueprints/` folder and defined in each module.

### Charts
Charts are contained in `/src/charts/` folder. Each chart needs to have a corresponding Chart class which inherits from BaseChart (see `/src/charts/ExampleChart.py` for reference).

### Data
Chart-specific data pipeline is handled by `/src/data/DataETL.py`. Any helper classes for data purposes should be defined in the `/src/data/` folder. The `etl` method should handle the entire ETL process for preparing data for charting. Please see https://github.com/man-group/arctic for more information on how to use Arctic and MongoDB.

### Models
(To-do)
