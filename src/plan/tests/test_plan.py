from plan.models import Plan
from .base import V1TestCase


class PlanTest(V1TestCase):

    def test_get(self):
        """GET /plans/<id>/: Planの詳細を取得するテスト"""
        self.client.post(self.plan_path, data=self.plan_data, format='json')
        plan = Plan.objects.all()[0]
        res = self.client.get(self.plan_detail_path.format(plan.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(plan.name, res.data['name'])
        self.assertEqual(2, len(res.data['spots']))

    # TODO: Implement PlanSerializer.update()
    # def test_patch(self):
    #     """PATCH /plan/plans/<id>: 特定のPlanの更新テスト"""
    #     user = User.objects.create_user(**self.user_data, is_active=True)
    #     self._set_credentials(user)
    #     res = self.client.post('/plan/plans/', data=self.post_data_set, format='json')
    #     updated_data = self.post_data_set
    #     updated_data['name'] = 'hoge'
    #     res = self.client.patch('/plan/plans/{}/'.format(res.data['pk']), data=updated_data, format='json')
    #     self.assertEqual(200, res.status_code)
