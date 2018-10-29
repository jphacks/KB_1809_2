import copy
from plan.models import Plan, Fav
from .base import V1TestCase


class PlanListTest(V1TestCase):

    def test_post(self):
        """POST /plans/: プラン作成テスト"""
        res = self.client.post(self.plan_path, data=self.plan_data, format='json')
        self.assertEqual(201, res.status_code)

    def test_get(self):
        """GET /plans/: プラン取得テスト"""
        self.client.post(self.plan_path, data=self.plan_data, format='json')
        new_data = copy.deepcopy(self.plan_data)
        new_data['name'] = "新しいコース"
        res = self.client.post(self.plan_path, data=new_data, format='json')
        self.assertEqual(201, res.status_code)
        res = self.client.get(self.plan_path)
        self.assertEqual(res.data[0]['name'], new_data['name'])

    def test_fail_post(self):
        """POST /plans/: 正しくない情報ではPlanが作成されないことを確認するテスト"""
        invalid_data = copy.deepcopy(self.plan_data)
        invalid_data['spots'] = []
        res = self.client.post(self.plan_path, data=invalid_data, format='json')
        self.assertEqual(400, res.status_code)
        plans = Plan.objects.all()
        self.assertEqual(1, plans.count())

    def test_get_my_fav_plans(self):
        """GET /me/favs/: 自分がふぁぼったPlan一覧が返されることを確認するテスト"""
        Fav.objects.create(user=self.user, plan_id=self.plan_id)
        res = self.client.get(self.my_fav_path)
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.data))
        self.assertEqual(self.plan_id, res.data[0]['pk'])
