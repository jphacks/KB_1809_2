import copy
from unittest.mock import patch
from plan.models import Plan
from .base import V1TestCase


class PlanTest(V1TestCase):

    def test_get(self):
        """GET /plans/<id>/: Planの詳細を取得するテスト"""
        plan = Plan.objects.all()[0]
        res = self.client.get(self.plan_detail_path.format(plan.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(plan.name, res.data['name'])
        self.assertEqual(2, len(res.data['spots']))

    def test_patch(self):
        """PATCH /plans/<plan_id>/: Planの変更テスト"""
        plan_data = copy.deepcopy(self.plan_data)
        plan_data['name'] = "hoge"
        plan_data['spots'][0]['lat'] = 37.000
        plan_data['spots'][0]['lon'] = 137.000
        plan_data['spots'].append({
            "name": "spot2",
            "lat": 37.012072,
            "lon": 137.6791853,
            "note": "test note",
            "image": plan_data['spots'][0]['image']
        })
        with patch('plan.serializers.plan.convert_geo_to_location') as mocked:
            mocked.return_value = self.location_meta
            res = self.client.patch(self.plan_detail_path.format(self.plan_id), data=plan_data, format="json")
            self.assertEqual(1, mocked.call_count)
        # check StatusCode, Plan Name, Num of Spots, and Spot order
        self.assertEqual(200, res.status_code)
        self.assertEqual(plan_data['name'], res.data['name'])
        self.assertEqual(len(plan_data['spots']), len(res.data['spots']))
        for i, s in enumerate(res.data['spots']):
            self.assertEqual(i, s['order'])

    def test_construct_map_url(self):
        """URLの作成テスト"""
        plan_data = copy.deepcopy(self.plan_data)
        plan_data['name'] = "hoge"
        plan_data['spots'][0]['lat'] = 1.0
        plan_data['spots'][0]['lon'] = 2.0
        plan_data['spots'][1]['lat'] = 3.0
        plan_data['spots'][1]['lon'] = 4.0
        plan_data['spots'].append({
            "name": "spot2",
            "lat": 5.0,
            "lon": 6.0,
            "note": "test note",
            "image": plan_data['spots'][0]['image']
        })
        plan_data['spots'].append({
            "name": "spot2",
            "lat": 7.0,
            "lon": 8.0,
            "note": "test note",
            "image": plan_data['spots'][0]['image']
        })
        multi_spot_plan = self.create_plan(data=plan_data)
        url = multi_spot_plan.construct_map_url()
        base = 'https://www.google.com/maps/dir/?'
        valid_query = 'api=1&travelmode=walking&origin=1.0%2C2.0&destination=7.0%2C8.0&waypoints=3.0%2C4.0%7C5.0%2C6.0'
        self.assertEqual(base+valid_query, url)
