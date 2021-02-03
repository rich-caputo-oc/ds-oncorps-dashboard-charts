from flask import Blueprint, request
from flask_cors import cross_origin

from data.DataETL import DataETL


def construct_data_endpoints(store):
    """
    Blueprint for anything data related.
    """

    data_endpoints = Blueprint('data-endpoints', __name__)

    @data_endpoints.route('/data-endpoints/etl')
    @cross_origin() # CORS allow all origins all methods
    def etl():
        """ Data endpoint. """
        data_etl = DataETL(store=store)
        data_etl.etl()
        return "ETL pipeline performed!"

    return data_endpoints
