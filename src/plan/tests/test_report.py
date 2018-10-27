import os
import base64
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from django.conf import settings

from accounts.models import User
from plan.models import Report, Plan

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

    def tearDown(self):
        super(ReportTest, self).tearDown()
        Plan.objects.all().delete()
        Report.objects.all().delete()

    def _set_credentials(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_post(self):
        """POST /plan/plans/<plan_id>/reports/ レポート作成テスト"""
        res = self.client.post("/plan/plans/{}/reports/".format(self.test_plan['pk']), data={
            "plan_id": self.test_plan['pk'],
            "text": "test report",
            "image": b64image
        }, format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual("test report", res.data['text'])
        self.assertEqual("test_user", res.data['user']['username'])

    def test_multi_post(self):
        """POST /plan/plans/<plan_id>/reports/ レポートを重複して作成するテスト"""
        res = self.client.post("/plan/plans/{}/reports/".format(self.test_plan['pk']), data={
            "plan_id": self.test_plan['pk'],
            "text": "test report",
            "image": b64image
        }, format="json")
        self.assertEqual(201, res.status_code)
        res = self.client.post("/plan/plans/{}/reports/".format(self.test_plan['pk']), data={
            "plan_id": self.test_plan['pk'],
            "text": "test report",
            "image": b64image
        }, format="json")
        self.assertEqual(201, res.status_code)

        reports = Report.objects.filter(user=self.user)
        self.assertEqual(2, len(reports))

    def test_get(self):
        """GET /plan/plans/<plan_id>/reports/ レポートを取得するテスト"""
        Report.objects.create(user=self.user, plan_id=self.test_plan['pk'], image=img_file)
        res = self.client.get("/plan/plans/{}/reports/".format(self.test_plan['pk']), format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.data))

    def test_get_detail(self):
        """GET /plan/plans/<plan_id>/reports/<report_id>/ レポート詳細を取得するテスト"""
        rep = Report.objects.create(user=self.user, plan_id=self.test_plan['pk'], image=img_file)
        res = self.client.get("/plan/plans/{}/reports/{}/".format(self.test_plan['pk'], rep.pk), format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual("test_user", res.data['user']['username'])

    def test_not_image(self):
        """POST /plan/plans/<plan_id>/reports/ 画像情報無しでレポートをPOSTするとエラーが返ってくる"""
        res = self.client.post("/plan/plans/{}/reports/".format(self.test_plan['pk']), data={
            "plan_id": self.test_plan['pk'],
            "text": "test report",
            "image": ""
        }, format="json")
        self.assertEqual(400, res.status_code)