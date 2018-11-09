import copy
from unittest.mock import patch
from django.conf import settings
from plan.models import Plan, Fav
from accounts.models import User
from .base import V1TestCase, V2TestCase
from .data import plan_data


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


class PlanListV2TestCase(V2TestCase):

    def test_pagination(self):
        """GET /plans/: プランがページネーションするかの確認テスト"""
        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        for _ in range(page_size):
            self.create_plan()
        res = self.client.get(self.plan_path)
        self.assertEqual(200, res.status_code)
        self.assertEqual(page_size, len(res.data['results']))
        self.assertNotEqual(None, res.data['next'])
        self.assertEqual(None, res.data['previous'])
        query = self.plan_path + '?cursor=' + res.data['next']
        next_res = self.client.get(query)
        self.assertEqual(200, next_res.status_code)
        self.assertEqual(1, len(next_res.data['results']))
        self.assertEqual(None, next_res.data['next'])
        self.assertNotEqual(None, next_res.data['previous'])
        self.create_plan()
        re_res = self.client.get(self.plan_path + '?cursor=' + res.data['next'])
        self.assertEqual(200, re_res.status_code)
        self.assertEqual(next_res.data, re_res.data)

    def test_filter(self):
        """GET /plans/?words=hogehoge Plan検索のテスト"""
        data = copy.deepcopy(plan_data)
        data['name'] = 'foo'
        data['spots'][0]['name'] = 'kyoto'
        data['spots'][1]['name'] = 'tokyo'
        self.create_plan(data=data)

        data = copy.deepcopy(plan_data)
        data['name'] = 'bar'
        data['spots'][0]['name'] = 'kobe'
        data['spots'][1]['name'] = 'nara'
        self.create_plan(data=data)

        res = self.client.get(self.plan_path, data={"location": "kyoto kobe"})
        self.assertEqual(200, res.status_code)
        self.assertEqual(2, len(res.data['results']))

        res = self.client.get(self.plan_path, data={"location": "foo kyoto"})
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.data['results']))
