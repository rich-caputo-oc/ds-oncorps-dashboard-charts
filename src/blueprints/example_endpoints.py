from flask import Blueprint, request
from flask_cors import cross_origin

from charts.ExampleChart import ExampleChart


def construct_example_endpoints(store):
    """
    Example blueprint for reference. Each blueprint should follow this syntax.
    """

    example_blueprint = Blueprint('example_blueprint', __name__)

    @example_blueprint.route('/example_endpoints/example_endpoint')
    @cross_origin() # CORS allow all origins all methods
    def example_endpoint():
        """ Example endpoint. """
        chart = ExampleChart(store=store, filters=request.args)
        return chart.render_chart()

    return example_blueprint