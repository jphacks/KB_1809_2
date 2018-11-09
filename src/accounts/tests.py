from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from .models import User


class BaseTestCase(APITestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.user_data = {"username": "test_user", "password": "hogefugapiyo", "email": "hoge@fuga.com"}

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        User.objects.all().delete()

    def _set_credentials(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)


class UserTest(BaseTestCase):

    def test_create_user(self):
        """POST /users/: Userの作成テスト"""
        res = self.client.post('/api/v2/users/', data=self.user_data, format='json')
        self.assertEqual(201, res.status_code)
        user = User.objects.all()
        self.assertEqual(1, len(user))
        self.assertEqual(self.user_data['username'], user[0].username)

    def test_create_invalid_user(self):
        """POST /users/: 情報が欠落したデータでのユーザ作成が失敗するかどうかのテスト"""
        self.user_data['email'] = 'invalid'
        res = self.client.post('/api/v2/users/', data=self.user_data, format='json')
        self.assertEqual(400, res.status_code)

    def test_get_user(self):
        """GET /users/<id>/: 特定のユーザ情報の取得テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        new_user_data = {'username': 'new_user', 'password': 'new_password'}
        new_user = User.objects.create_user(**new_user_data, is_active=True)
        self._set_credentials(user)
        res = self.client.get('/api/v2/users/{}/'.format(new_user.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(new_user.username, res.data['username'])


class MeTestCase(BaseTestCase):

    def test_delete_user(self):
        """DELETE /users/me/: 自身のアカウントの削除テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials(user)
        res = self.client.delete('/api/v2/me/', data={'current_password': self.user_data['password']})
        self.assertEqual(204, res.status_code)
        self.assertFalse(User.objects.filter(pk=user.pk).exists())

    def test_update_user(self):
        """PATCH /me/: 自身の情報の更新テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials(user)
        email = 'hoge@fuga.com'
        res = self.client.patch('/api/v2/me/', data={'email': email}, format='json')
        self.assertEqual(200, res.status_code)
        user = User.objects.get(pk=user.pk)
        self.assertEqual(email, user.email)

    def test_get_me(self):
        """GET /me/: 自身の情報の取得テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials(user)
        res = self.client.get('/api/v2/me/')
        self.assertEqual(200, res.status_code)
        self.assertEqual(user.username, res.data['username'])
