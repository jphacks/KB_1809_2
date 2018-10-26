import os
import base64
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from django.conf import settings

from accounts.models import User
from plan.models import Fav, Plan

# TODO: まとめたい
img_file = os.path.join(settings.MEDIA_ROOT, "icons", "user.png")
with open(img_file, 'rb') as fp:
    b64image = base64.encodebytes(fp.read())
plan_data = {
    "name": "嵐山コース",
    "price": 10000,
    "duration": 360,
    "note": "嵐山でぶらぶらしながら色んなお店を回るコースです",
    "spots": [
        {
            "name": "嵐山公園",
            "lat": 35.012072,
            "lon": 135.6791853,
            "note": "いい公園",
            "image": b64image
        }, {
            "name": "嵐山公園",
            "lat": 35.012072,
            "lon": 135.6791853,
            "note": "いい公園",
            "image": b64image
        }
    ]
}

post_data = {
    "plan_id": 1
}


class FavTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "test_user", "password": "hogefugapiyo"}
        self.user = User.objects.create_user(**self.user_data, is_active=True)
        self.post_data_set = post_data
        self._set_credentials()

    def tearDown(self):
        super(FavTest, self).tearDown()
        Fav.objects.all().delete()
        Plan.objects.all().delete()

    def _set_credentials(self, user=None):
        if not user:
            user = self.user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_post(self):
        """POST /plan/plans/<id>/favs/: いいね作成テスト"""
        plan_res = self.client.post("/plan/plans/", data=plan_data, format='json')
        for path in ['/plan/plans/{}/favs/me/', '/plan/plans/{}/favs/']:
            res = self.client.post(path.format(plan_res.data['pk']), data={}, format="json")
            self.assertEqual(201, res.status_code)
            Fav.objects.get(pk=res.data['pk']).delete()

    def test_get_list(self):
        """GET /plan/plans/<id>/favs/: いいね一覧取得テスト"""
        res = self.client.post("/plan/plans/", data=plan_data, format='json')
        plan_id = res.data['pk']
        fav = Fav.objects.create(user=self.user, plan_id=res.data['pk'])
        res = self.client.get("/plan/plans/{}/favs/".format(res.data['pk']), data={}, format="json")
        self.assertEqual(200, res.status_code)
        actual_favs = Fav.objects.filter(plan_id=plan_id).count()
        # 全てそのplanのfavであることを確認
        self.assertEqual(actual_favs, len(res.data))
        for f in res.data:
            self.assertEqual(plan_id, f['plan_id'])
        fav_list = [f['pk'] for f in res.data]
        self.assertTrue(fav.pk in fav_list)

    def test_destroy(self):
        """DELETE /plan/plans/<id>/favs/: いいね削除テスト"""
        plan_res = self.client.post("/plan/plans/", data=plan_data, format='json')
        for path in ['/plan/plans/{}/favs/me/']:
            fav = Fav.objects.create(user=self.user, plan_id=plan_res.data['pk'])
            res = self.client.delete(path.format(plan_res.data['pk']))
            self.assertEqual(204, res.status_code)
            with self.assertRaises(Fav.DoesNotExist):
                Fav.objects.get(pk=fav.pk)

    def test_get_detail(self):
        """GET /plan/plans/<id>/favs/<id>/: いいねの詳細取得テスト"""
        plan_res = self.client.post("/plan/plans/", data=plan_data, format='json')
        fav = Fav.objects.create(user=self.user, plan_id=plan_res.data['pk'])
        res = self.client.get("/plan/plans/{}/favs/{}/".format(plan_res.data['pk'], fav.pk), data={}, format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.user.username, res.data['user']['username'])

    def test_get_detail_404(self):
        """GET /plan/plans/<id>/favs/<id>/: いいねの詳細取得404テスト"""
        plan_res = self.client.post("/plan/plans/", data=plan_data, format='json')
        res = self.client.get("/plan/plans/{}/favs/{}/".format(plan_res.data['pk'], 9999), data={}, format="json")
        self.assertEqual(404, res.status_code)
        new_plan_res = self.client.post("/plan/plans/", data=plan_data, format='json')
        fav = Fav.objects.create(user=self.user, plan_id=new_plan_res.data['pk'])
        res = self.client.get("/plan/plans/{}/favs/{}/".format(9999, fav.pk), data={}, format="json")
        self.assertEqual(404, res.status_code)
