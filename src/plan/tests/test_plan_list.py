import copy
from unittest.mock import patch
from plan.models import Plan, Fav
from accounts.models import User
from .base import V1TestCase


class PlanListTest(V1TestCase):

    def test_post(self):
        """POST /plans/: プラン作成テスト"""
        with patch('plan.serializers.plan.convert_geo_to_location') as mocked:
            mocked.return_value = self.location_meta
            res = self.client.post(self.plan_path, data=self.plan_data, format='json')
            self.assertTrue(1, mocked.call_count)
        self.assertEqual(201, res.status_code)

    def test_get(self):
        """GET /plans/: プラン取得テスト"""
        res = self.client.get(self.plan_path)
        self.assertEqual(self.plan_id, res.data[0]['pk'])
        self.assertEqual(self.plan.name, res.data[0]['name'])

    def test_fail_post(self):
        """POST /plans/: 正しくない情報ではPlanが作成されないことを確認するテスト"""
        invalid_data = copy.deepcopy(self.plan_data)
        invalid_data['spots'] = []
        with patch('plan.serializers.plan.convert_geo_to_location') as mocked:
            mocked.return_value = self.location_meta
            res = self.client.post(self.plan_path, data=invalid_data, format='json')
            self.assertEqual(0, mocked.call_count)
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

    def test_get_specific_user_plans(self):
        """GET /users/<id>/plans/: 特定のユーザの投稿したPlan一覧取得テスト"""
        new_user = User.objects.create(**self.user_data[1], is_active=True)
        self._set_credentials(new_user)
        res = self.client.get(self.user_plan_path.format(new_user.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(res.data))
        self._set_credentials(self.user)
        res = self.client.get(self.user_plan_path.format(self.user.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.data))
        self.assertEqual(self.plan_id, res.data[0]['pk'])
