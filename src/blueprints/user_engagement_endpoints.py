from flask import Blueprint, request
from flask_cors import cross_origin

from charts.ExampleChart import ExampleChart


def construct_user_engagement_endpoints(store):
    """
    Example charting blueprint for reference. Each blueprint should follow this syntax.
    Charting endpoints should always be of the form:
    /<sidebar-name>/<tab-name>/<chart-name>
    """

    example_endpoints = Blueprint('user-engagement', __name__)

    @example_endpoints.route('/side-nav/user-engagement')
    @cross_origin() # CORS allow all origins all methods
    def side_nav():
        """
        Every blueprint must have this function.
        Returns cs-values for side-nav html file.
        Return format must be: <default-link>,<icon>,<name>
        Example: "/user-engagement/all,people,User Engagement"

        For more info on icons, visit: https://jossef.github.io/material-design-icons-iconfont/
        """
        return "/user-engagement/all,people,User Engagement"

    @example_endpoints.route('/user-engagement/example-endpoints/example-endpoint')
    @cross_origin() # CORS allow all origins all methods
    def example_endpoint():
        """ Example endpoint. """
        chart = ExampleChart(store=store, filters=request.args)
        return chart.render_chart()

    @example_endpoints.route('/user-engagement/all/all')
    @cross_origin() # CORS allow all origins all methods
    def all():
        """ Example endpoint. """
        chart = ExampleChart(store=store, filters=request.args)
        return chart.render_chart()

    @example_endpoints.route('/user-engagement/something/something')
    @cross_origin() # CORS allow all origins all methods
    def something():
        """ Example endpoint. """
        chart = ExampleChart(store=store, filters=request.args)
        return chart.render_chart()



    return example_endpoints
