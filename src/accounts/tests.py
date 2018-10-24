from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from .models import User


class UserTest(APITestCase):

    def setUp(self):
        super(UserTest, self).setUp()
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}

    def tearDown(self):
        super(UserTest, self).tearDown()
        User.objects.all().delete()

    def _set_credentials(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_create_user(self):
        """POST /users/create/: Userの作成テスト"""
        res = self.client.post('/users/create/', data=self.user_data, format='json')
        self.assertEqual(201, res.status_code)
        user = User.objects.all()
        self.assertEqual(1, len(user))
        self.assertEqual(self.user_data['username'], user[0].username)

    def test_update_user(self):
        """PATCH /me/: 自身の情報の更新テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials(user)
        res = self.client.patch('/me/', data={'email': 'hoge@fuga.com'}, format='json')
        self.assertEqual(200, res.status_code)

    def test_get_me(self):
        """GET /me/: 自身の情報の取得テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials(user)
        res = self.client.get('/me/')
        self.assertEqual(200, res.status_code)
        self.assertEqual(user.username, res.data['username'])

    def test_get_user(self):
        """GET /users/<id>/: 特定のユーザ情報の取得テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        new_user_data = {'username': 'new_user', 'password': 'new_password'}
        new_user = User.objects.create_user(**new_user_data, is_active=True)
        self._set_credentials(user)
        res = self.client.get('/users/{}/'.format(new_user.pk))
        self.assertEqual(200, res.status_code)
        self.assertEqual(new_user.username, res.data['username'])

    def test_get_user_list(self):
        """GET /users/: ユーザ全体の情報取得テスト"""
        user = User.objects.create_user(**self.user_data, is_active=True)
        self._set_credentials(user)
        res = self.client.get('/users/')
        self.assertEqual(403, res.status_code)

    # Delete user fail. issue: https://github.com/sunscrapers/djoser/issues/257
    # def test_delete_user(self):
    #     """DELETE /users/me/: 自身のアカウントの削除テスト"""
    #     user = User.objects.create_user(**self.user_data, is_active=True)
    #     self._set_credentials(user)
    #     res = self.client.delete('/users/me/', data={'current_password': self.user_data['password']})
    #     self.assertEqual(204, res.status_code)
    #     self.assertFalse(User.objects.filter(username=user.username).exists())
