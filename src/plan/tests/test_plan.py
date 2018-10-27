import copy
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from accounts.models import User
from plan.models import Plan
from .data import plan_data


class PlanTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.post_data_set = copy.deepcopy(plan_data)

    def tearDown(self):
        super(PlanTest, self).tearDown()
        User.objects.all().delete()
        Plan.objects.all().delete()

    def _set_credentials(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_get(self):
        """GET /plan/plans/<id>/: Planの詳細を取得するテスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials(user)
        self.client.post('/plan/plans/', data=self.post_data_set, format='json')
        plan = Plan.objects.all()[0]
        res = self.client.get('/plan/plans/{}/'.format(plan.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(plan.name, res.data['name'])
        self.assertEqual(2, len(res.data['spots']))

    # TODO: Implement PlanSerializer.update()
    # def test_patch(self):
    #     """PATCH /plan/plans/<id>: 特定のPlanの更新テスト"""
    #     user = User.objects.create_user(**self.user_data, is_active=True)
    #     self._set_credentials(user)
    #     res = self.client.post('/plan/plans/', data=self.post_data_set, format='json')
    #     updated_data = self.post_data_set
    #     updated_data['name'] = 'hoge'
    #     res = self.client.patch('/plan/plans/{}/'.format(res.data['pk']), data=updated_data, format='json')
    #     self.assertEqual(200, res.status_code)
