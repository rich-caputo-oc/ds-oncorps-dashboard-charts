# ds-oncorps-charts

### Set up
0. Ensure environment hosts necessary packages
1. `docker-compose build`
2. `docker-compose up` with optional `-d` parameter to run detached
3. If not in a local dev environment, change `FLASK_DEBUG: 0` in `docker-compose.override.yml`
4. Ensure `docker-compose.override.yml` contains correct MongoDB info
5. Calls are of the form: `localhost:4000/<blueprint_name/sidebar_tab>/<top_tab>/<endpoint_name>`


### Endpoints
Definitions/routes are contained in the `/src/blueprints/` folder and defined in each module

**Query parameters for filters** <br>
Endpoints are defined in src/blueprints.
