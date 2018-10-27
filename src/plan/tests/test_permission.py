import os
import base64
import copy
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from django.conf import settings


from accounts.models import User
from plan.models import Plan

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


class PermissionTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.post_data_set = copy.deepcopy(plan_data)
        self.user1 = User.objects.create(**self.user_data, is_active=True)
        self.user2 = User.objects.create(username='hoge', password='fugafuga', is_active=True)

    def tearDown(self):
        super(PermissionTest, self).tearDown()
        User.objects.all().delete()
        Plan.objects.all().delete()

    def _set_credentials(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_plan_permission(self):
        """POST /plan/plans/<id>/: 他人のPlanは更新不可であるかどうかのテスト"""
        self._set_credentials(self.user1)
        res = self.client.post('/plan/plans/', data=self.post_data_set, format='json')
        self.assertEqual(201, res.status_code)
        self._set_credentials(self.user2)
        res = self.client.patch('/plan/plans/{}/'.format(res.data['pk']), data=self.post_data_set, format='json')
        self.assertEqual(403, res.status_code)
