import copy
from base64 import b64decode
from django.core.files import base
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from accounts.models import User
from plan.models import Comment, Plan, Fav, Spot, Location, Report
from plan.geo import LocationMeta
from .data import plan_data, comment_data, user_data, report_data, location_data, lat, lon, b64image


class V1TestCase(APITestCase):

    path_prefix = '/api/v1/'

    def __init__(self, *args, **kwargs):
        super(V1TestCase, self).__init__(*args, **kwargs)
        # Plan
        self.plan_path = self.path_prefix + 'plans/'
        self.plan_detail_path = self.plan_path + '{}/'
        # Fav
        self.fav_path = self.plan_detail_path + 'favs/'
        self.fav_detail_path = self.fav_path + '{}/'
        self.fav_me_path = self.fav_path + 'me/'
        # Comment
        self.comment_path = self.plan_detail_path + 'comments/'
        self.comment_detail_path = self.comment_path + '{}/'
        # Report
        self.report_path = self.plan_detail_path + 'reports/'
        self.report_detail_path = self.report_path + '{}/'
        self.report_patch_path = self.report_detail_path
        # Me
        self.me_path = self.path_prefix + 'me/'
        self.my_fav_path = self.me_path + 'favs/'
        self.my_plan_path = self.me_path + 'plans/'
        # Users
        self.user_path = self.path_prefix + 'users/'
        self.user_detail_path = self.user_path + '{}/'
        self.user_plan_path = self.user_detail_path + 'plans/'

    def setUp(self):
        self.user_data = copy.deepcopy(user_data)
        self.plan_data = copy.deepcopy(plan_data)
        self.comment_data = copy.deepcopy(comment_data)
        self.report_data = copy.deepcopy(report_data)
        self.location_data = copy.deepcopy(location_data)
        self.location_meta = LocationMeta(**self.location_data[0], lat=lat, lon=lon)
        self.user = User.objects.create_user(**self.user_data[0], is_active=True)
        self._set_credentials()
        self.plan = self.create_plan()
        self.plan_id = self.plan.pk

    def tearDown(self):
        super(V1TestCase, self).tearDown()
        Comment.objects.all().delete()
        Fav.objects.all().delete()
        Plan.objects.all().delete()
        User.objects.all().delete()
        Location.objects.all().delete()
        Report.objects.all().delete()

    def _set_credentials(self, user=None):
        if not user:
            user = self.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def create_plan(self, data=None, user=None, loc_data=None):
        if user is None:
            user = self.user
        if data is None:
            data = copy.deepcopy(self.plan_data)
        if loc_data is None:
            loc_data = self.location_data[0]
        spots_data = data.pop('spots')
        location, _ = Location.objects.get_or_create(**loc_data)
        plan = Plan.objects.create(**data, location=location, user=user)
        spots = []
        for i in range(len(spots_data)):
            spots_data[i]['image'] = self.get_test_image()
            spot = Spot.objects.create(**spots_data[i], plan_id=plan.id, order=i)
            spots.append(spot)
        return plan

    def get_test_image(self):
        return base.ContentFile(b64decode(b64image), 'icons/user.png')


class V2TestCase(V1TestCase):
    path_prefix = '/api/v2/'
