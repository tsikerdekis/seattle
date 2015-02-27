from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    Incidents_Model,
    )

import time
import pytz
import math
import numpy as np


def epoch_time(dt):
    """Method to convert datetime object into epoch time in days."""
    utc = pytz.timezone('UTC')
    utc_dt = utc.normalize(dt.astimezone(utc))
    return time.mktime(utc_dt.timetuple())/60/60/24


def epoch_list(a_list):
    """Convert query.all() list into a sorted list with only epoch time."""
    date_list = []
    for item in a_list:
        date_list.append(epoch_time(item.date_time))
    return sorted(date_list)


@view_config(route_name='index', renderer='templates/index.jinja2')
def line_plot(request):
    "Returns epoch datetime params as a list."
    lat = 47.623636
    lon = -122.336072
    radius = 0.01

    try:
        incident_types = ['Fire', 'MVI', 'Crime']
        output = []
        start_time = time.time()
        for inc_type in incident_types:
            output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, inc_type, radius)))
        print 'time to call db for initial query: {}'.format(time.time()-start_time)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    output_percentages = {}
    output_count = {}
    for i in range(3):
        temp = Incidents_Model.percentage(output[i])
        output_percentages[incident_types[i]] = temp['string']
        output_count[incident_types[i]] = temp['year_count']
        print '{} count: {}'.format(incident_types[i], temp['year_count'])

    min_date = min(min(output[0]), min(output[1]), min(output[2]))
    max_date = max(max(output[0]), max(output[1]), max(output[2]))
    number_months = int(math.ceil((max_date - min_date)/30))
    months = [min_date + 30*i for i in range(number_months)]
    count = [[], [], []]
    for j, item in enumerate(output):
        bin_indicies = np.digitize(item, months[1:], right=True).tolist()
        count[j] = [bin_indicies.count(i) for i in range(number_months-1)]
    data = [{'month': months[1:][j], 'fire':  count[0][j], 'mvi':  count[1][j], 'crime':  count[2][j]} for j in range(number_months-1)]

    return {'output': data,
            'percentages': output_percentages,
            'counts': output_count,
            'lat': lat, 'lon': lon}


@view_config(route_name='ajax', renderer='json')
def line_plot_lat_long_ajax(request):
    "Returns epoch datetime params as a list."
    lat = request.params.get('lat_cen', 47.623636)
    lon = request.params.get('lon_cen', -122.336072)
    print 'lat: {}'.format(lat)
    print 'lon: {}'.format(lon)
    radius = 0.01

    try:
        incident_types = ['Fire', 'MVI', 'Crime']
        output = []
        start_time = time.time()
        for inc_type in incident_types:
            output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, inc_type, radius)))
        print 'time to call db for initial query: {}'.format(time.time()-start_time)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    output_percentages = {}
    output_count = {}
    for i in range(3):
        temp = Incidents_Model.percentage(output[i])
        output_percentages[incident_types[i]] = temp['string']
        output_count[incident_types[i]] = temp['year_count']
        print '{} count: {}'.format(incident_types[i], temp['year_count'])

    try:
        min_date = min(min(output[0]), min(output[1]), min(output[2]))
        max_date = max(max(output[0]), max(output[1]), max(output[2]))
        number_months = int(math.ceil((max_date - min_date)/30))
        months = [min_date + 30*i for i in range(number_months)]
        count = [[], [], []]
        for j, item in enumerate(output):
            bin_indicies = np.digitize(item, months[1:], right=True).tolist()
            count[j] = [bin_indicies.count(i) for i in range(number_months-1)]
        data = [{'month': months[1:][j], 'fire':  count[0][j], 'mvi':  count[1][j], 'crime':  count[2][j]} for j in range(number_months-1)]

    except ValueError:
        months = []
        count = []
    return {'output': data,
            'percentages': output_percentages,
            'counts': output_count,
            'lat': lat, 'lon': lon}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_seattle_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
