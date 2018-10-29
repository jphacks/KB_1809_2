import copy
from plan.models import Report
from .data import img_file
from .base import V1TestCase


class ReportTest(V1TestCase):

    def test_post(self):
        """POST /plans/<plan_id>/reports/ レポート作成テスト"""
        data = copy.deepcopy(self.report_data[0])
        data["plan_id"] = self.plan_id
        res = self.client.post(self.report_path.format(self.plan_id), data=data, format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual(data['text'], res.data['text'])
        self.assertEqual(self.user.username, res.data['user']['username'])

    def test_multi_post(self):
        """POST /plans/<plan_id>/reports/ レポートを重複して作成するテスト"""
        for i in range(2):
            data = copy.deepcopy(self.report_data[i])
            data["plan_id"] = self.plan_id
            res = self.client.post(self.report_path.format(self.plan_id), data=data, format="json")
            self.assertEqual(201, res.status_code)
        reports = Report.objects.filter(user=self.user)
        self.assertEqual(2, len(reports))

    def test_get(self):
        """GET /plans/<plan_id>/reports/ レポートを取得するテスト"""
        Report.objects.create(user=self.user, plan_id=self.plan_id, image=img_file)
        res = self.client.get(self.report_path.format(self.plan_id), format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.data))

    def test_get_detail(self):
        """GET /plans/<plan_id>/reports/<report_id>/ レポート詳細を取得するテスト"""
        rep = Report.objects.create(user=self.user, plan_id=self.plan_id, image=img_file)
        res = self.client.get(self.report_detail_path.format(self.plan_id, rep.pk), format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.user.username, res.data['user']['username'])

    def test_not_image(self):
        """POST /plans/<plan_id>/reports/ 画像情報無しでレポートをPOSTするとエラーが返ってくる"""
        res = self.client.post(self.report_path.format(self.plan_id), data={
            "plan_id": self.plan_id,
            "text": "test report",
            "image": ""
        }, format="json")
        self.assertEqual(400, res.status_code)
