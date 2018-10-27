import copy
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from accounts.models import User
from plan.models import Plan
from .data import plan_data


class PlanListTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.user = User.objects.create_user(**self.user_data, is_active=True)
        self.post_data_set = copy.deepcopy(plan_data)

    def tearDown(self):
        super(PlanListTest, self).tearDown()
        Plan.objects.all().delete()

    def _set_credentials(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_post(self):
        """POST /plan/plans/: プラン作成テスト"""
        self._set_credentials()
        res = self.client.post("/plan/plans/", data=self.post_data_set, format='json')
        self.assertEqual(201, res.status_code)

    def test_get(self):
        """GET /plan/plans/: プラン取得テスト"""
        self._set_credentials()
        self.client.post("/plan/plans/", data=self.post_data_set, format='json')
        new_data = copy.deepcopy(self.post_data_set)
        new_data['name'] = "新しいコース"
        res = self.client.post("/plan/plans/", data=new_data, format='json')
        self.assertEqual(201, res.status_code)
        res = self.client.get('/plan/plans/')
        self.assertEqual(res.data[0]['name'], new_data['name'])

    def test_fail_post(self):
        """POST /plan/plans/: 正しくない情報ではPlanが作成されないことを確認するテスト"""
        self._set_credentials()
        invalid_data = copy.deepcopy(self.post_data_set)
        invalid_data['spots'] = []
        res = self.client.post('/plan/plans/', data=invalid_data, format='json')
        self.assertEqual(400, res.status_code)
        plans = Plan.objects.all()
        self.assertEqual(False, plans.exists())
