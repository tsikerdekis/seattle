#from contextlib import closing
#import unittest
#import transaction

#from pyramid_sqlalchemy.testing import DatabaseTestCase
#from pyramid import testing

from models import DBSession, Incidents_Model
from views import line_plot, line_plot_lat_long_ajax

import pytest


TEST_DSN = 'dbname=seattle_test user=Joel'


def test_foo(sql_session):
    import pdb; pdb.set_trace()
    model = Incidents_Model.by_gid(123, sql_session)
    assert False

#class ViewIntegrationTests(DatabaseTestCase):
#    def setUp(self):
#        super(ViewIntegrationTests, self).setUp()
#        self.config = testing.setUp()
#
#    def test_cat_circle(sql_session):
#        lat = 47.623636
#        lon = -122.336072
#        radius = 0.1
#        result = Incidents_Model.cat_circle(lat, lon, 'Fire', radius, limit=5)
#        print result
#
#    def tearDown(self):
#        testing.tearDown()
#        super(ViewIntegrationTests, self).tearDown()
#
#
#@pytest.fixture
#def pyramid_req():
#    return testing.DummyRequest()



#def test_line_plot_lat_long_returns_correctly(request):
#    response = line_plot(pyramid_req)
#    print response



#class TestMyViewSuccessCondition(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#        from sqlalchemy import create_engine
#        engine = create_engine('sqlite://')
#        from .models import (
#            Base,
#            MyModel,
#            )
#        DBSession.configure(bind=engine)
#        Base.metadata.create_all(engine)
#        with transaction.manager:
#            model = MyModel(name='one', value=55)
#            DBSession.add(model)
#
#    def tearDown(self):
#        DBSession.remove()
#        testing.tearDown()
#
#    def test_passing_view(self):
#        from .views import my_view
#        request = testing.DummyRequest()
#        info = my_view(request)
#        self.assertEqual(info['one'].name, 'one')
#        self.assertEqual(info['project'], 'seattle')
#
#
#class TestMyViewFailureCondition(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#        from sqlalchemy import create_engine
#        engine = create_engine('sqlite://')
#        from .models import (
#            Base,
#            MyModel,
#            )
#        DBSession.configure(bind=engine)
#
#    def tearDown(self):
#        DBSession.remove()
#        testing.tearDown()
#
#    def test_failing_view(self):
#        from .views import my_view
#        request = testing.DummyRequest()
#        info = my_view(request)
#        self.assertEqual(info.status_int, 500)
