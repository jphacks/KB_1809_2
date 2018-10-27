from accounts.models import User
from .base import BaseTestCase


class PermissionTest(BaseTestCase):

    def test_plan_permission(self):
        """POST /plan/plans/<id>/: 他人のPlanは更新不可であるかどうかのテスト"""
        self._set_credentials(self.user)
        res = self.client.post(self.plan_path, data=self.plan_data, format='json')
        self.assertEqual(201, res.status_code)
        user2 = User.objects.create(**self.user_data[1], is_active=True)
        self._set_credentials(user2)
        res = self.client.patch(self.plan_detail_path.format(res.data['pk']), data=self.plan_data, format='json')
        self.assertEqual(403, res.status_code)
