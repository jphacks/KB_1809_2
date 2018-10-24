import os
import base64
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from django.conf import settings


from accounts.models import User
from .models import Plan

img_file = os.path.join(settings.MEDIA_ROOT, "icons", "user.png")
with open(img_file, 'rb') as fp:
    b64image = base64.encodebytes(fp.read())
plan_data = {
    "name": "嵐山コース",
    "price": 10000,
    "duration": 360,
    "note": "嵐山でぶらぶらしながら色んなお店を回るコースです",
    "spots": [
        {
            "name": "嵐山公園",
            "lat": 35.012072,
            "lon": 135.6791853,
            "note": "いい公園",
            "image": b64image
        }, {
            "name": "嵐山公園",
            "lat": 35.012072,
            "lon": 135.6791853,
            "note": "いい公園",
            "image": b64image
        }
    ]
}


class PlanListTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.user = User.objects.create_user(**self.user_data, is_active=True)
        self.post_data_set = plan_data

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
        new_data = self.post_data_set
        new_data['name'] = "新しいコース"
        self.client.post("/plan/plans/", data=new_data, format='json')
        res = self.client.get('/plan/plans/')
        self.assertEqual(res.data[0]['name'], new_data['name'])


class PlanTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.post_data_set = plan_data

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
