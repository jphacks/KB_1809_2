import os
import base64
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from django.conf import settings


from accounts.models import User
from plan.models import Spot


class PlanTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.user = User.objects.create(**self.user_data, is_active=True)

    def test_post(self):
        self.assertEqual(1, User.objects.count())
        img_file = os.path.join(settings.MEDIA_ROOT, "icons", "user.png")
        with open(img_file, 'rb') as fp:
            b64image = base64.encodebytes(fp.read())
        post_data_set = {
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
                    "image": "".format(b64image.decode("utf-8"))
                }, {
                    "name": "嵐山公園",
                    "lat": 35.012072,
                    "lon": 135.6791853,
                    "note": "いい公園",
                    "image": "".format(b64image.decode("utf-8"))
                }
            ]
        }

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        self.assertEqual(0, Spot.objects.count())
        post_resp = self.client.post("/plan/plans/", data=post_data_set, format='json')
        self.assertEqual(201, post_resp.status_code)
