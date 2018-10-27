import copy
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from accounts.models import User
from plan.models import Comment, Plan, Fav
from .data import plan_data, comment_data, user_data, report_data


class BaseTestCase(APITestCase):

    path_prefix = '/plan/'
    # Plan
    plan_path = path_prefix + 'plans/'
    plan_detail_path = plan_path + '{}/'
    # Fav
    fav_path = plan_detail_path + 'favs/'
    fav_detail_path = fav_path + '{}/'
    fav_me_path = fav_path + 'me/'
    # Comment
    comment_path = plan_detail_path + 'comments/'
    comment_detail_path = comment_path + '{}/'
    # Report
    report_path = plan_detail_path + 'reports/'
    report_detail_path = report_path + '{}/'

    def setUp(self):
        self.user_data = copy.deepcopy(user_data)
        self.plan_data = copy.deepcopy(plan_data)
        self.comment_data = copy.deepcopy(comment_data)
        self.report_data = copy.deepcopy(report_data)
        self.user = User.objects.create_user(**self.user_data[0], is_active=True)
        self._set_credentials()
        self.plan_res = self.client.post("/plan/plans/", data=self.plan_data, format='json')
        self.plan_id = self.plan_res.data['pk']

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
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
