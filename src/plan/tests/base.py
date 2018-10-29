import copy
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from accounts.models import User
from plan.models import Comment, Plan, Fav
from .data import plan_data, comment_data, user_data, report_data


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
        # Me
        self.me_path = self.path_prefix + 'me/'
        self.my_fav_path = self.me_path + 'favs/'
        self.my_plan_path = self.me_path + 'plans/'
        # Users
        self.user_path = self.path_prefix + 'users/'
        self.user_detail_path = self.user_path + '{}/'
        self.user_fav_path = self.user_detail_path + 'favs/'
        self.user_plan_path = self.user_detail_path + 'plans/'

    def setUp(self):
        self.user_data = copy.deepcopy(user_data)
        self.plan_data = copy.deepcopy(plan_data)
        self.comment_data = copy.deepcopy(comment_data)
        self.report_data = copy.deepcopy(report_data)
        self.user = User.objects.create_user(**self.user_data[0], is_active=True)
        self._set_credentials()
        self.plan_res = self.client.post(self.plan_path, data=self.plan_data, format='json')
        self.plan_id = self.plan_res.data['pk']

    def tearDown(self):
        super(V1TestCase, self).tearDown()
        Comment.objects.all().delete()
        Fav.objects.all().delete()
        Plan.objects.all().delete()
        User.objects.all().delete()

    def _set_credentials(self, user=None):
        if not user:
            user = self.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)


class V2TestCase(V1TestCase):
    path_prefix = '/api/v2/'
