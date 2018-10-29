from .base import V1TestCase


class UsersTest(V1TestCase):

    def test_create(self):
        """POST /users/: ユーザ作成のテスト"""
        test_user_data = {'username': 'test', 'password': 'hogefuga'}
        res = self.client.post(self.user_path, data=test_user_data, format='json')
        self.assertEqual(201, res.status_code)

    def test_get(self):
        """GET /users/<id>/: ユーザプロフィール取得テスト"""
        res = self.client.get(self.user_detail_path.format(self.user.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.user_data[0]['username'], res.data['username'])
