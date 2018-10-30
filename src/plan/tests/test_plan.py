from plan.models import Plan
from .base import V1TestCase
import os
import base64

from django.conf import settings


class PlanTest(V1TestCase):

    def test_get(self):
        """GET /plans/<id>/: Planの詳細を取得するテスト"""
        self.client.post(self.plan_path, data=self.plan_data, format='json')
        plan = Plan.objects.all()[0]
        res = self.client.get(self.plan_detail_path.format(plan.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(plan.name, res.data['name'])
        self.assertEqual(2, len(res.data['spots']))

    def test_patch(self):
        """PATCH /plans/<plan_id>/: Planの変更テスト"""
        res = self.client.post(self.plan_path, data=self.plan_data, format="json")
        self.assertEqual(201, res.status_code)

        self.plan_data['name'] = "hoge"
        self.plan_data['spots'][0]['lat'] = 37.000
        self.plan_data['spots'][0]['lon'] = 137.000
        self.plan_data['spots'].append({
            "name": "spot2",
            "lat": 37.012072,
            "lon": 137.6791853,
            "note": "test note",
            "image": self.plan_data['spots'][0]['image']
        })

        res = self.client.patch('/api/v1/plans/{}/'.format(res.data['pk']), data=self.plan_data, format="json")
        # check StatusCode, Plan Name, Num of Spots, and Spot order
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.plan_data['name'], res.data['name'])
        self.assertEqual(len(self.plan_data['spots']), len(res.data['spots']))
        for i, s in enumerate(res.data['spots']):
            self.assertEqual(i, s['order'])
