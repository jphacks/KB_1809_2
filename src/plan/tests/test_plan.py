import copy
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
        # TODO: mock
        res = self.client.patch('/api/v1/plans/{}/'.format(self.plan_id), data=plan_data, format="json")
        # check StatusCode, Plan Name, Num of Spots, and Spot order
        self.assertEqual(200, res.status_code)
        self.assertEqual(plan_data['name'], res.data['name'])
        self.assertEqual(len(plan_data['spots']), len(res.data['spots']))
        for i, s in enumerate(res.data['spots']):
            self.assertEqual(i, s['order'])
