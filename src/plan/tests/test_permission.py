from unittest.mock import patch
from accounts.models import User
from .base import V1TestCase


class PermissionTest(V1TestCase):

    def test_plan_permission(self):
        """POST /plans/<id>/: 他人のPlanは更新不可であるかどうかのテスト"""
        self._set_credentials(self.user)
        with patch('plan.serializers.plan.convert_geo_to_location') as mocked:
            mocked.return_value = self.location_meta
            res = self.client.post(self.plan_path, data=self.plan_data, format='json')
            self.assertEqual(1, mocked.call_count)
        self.assertEqual(201, res.status_code)
        user2 = User.objects.create(**self.user_data[1], is_active=True)
        self._set_credentials(user2)
        with patch('plan.serializers.plan.convert_geo_to_location') as mocked:
            mocked.return_value = self.location_meta
            res = self.client.patch(self.plan_detail_path.format(res.data['pk']), data=self.plan_data, format='json')
            self.assertEqual(0, mocked.call_count)
        self.assertEqual(403, res.status_code)
