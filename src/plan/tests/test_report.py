import os
import base64
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from django.conf import settings

from accounts.models import User

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


class ReportTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials()
        res = self.client.post("/plan/plans/", data=plan_data, format='json')
        self.test_plan = res.data

    def _set_credentials(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_post(self):
        """POST /plan/reports/ レポート作成テスト"""
        res = self.client.post("/plan/reports/", data={
            "plan_id": self.test_plan['pk'],
            "text": "test report",
            "image": b64image
        }, format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual("test report", res.data['text'])
        self.assertEqual("test_user", res.data['user']['username'])
