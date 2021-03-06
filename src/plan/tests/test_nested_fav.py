from plan.models import Fav
from .base import V1TestCase


class FavTest(V1TestCase):

    def test_post(self):
        """POST /plans/<id>/favs/: いいね作成テスト"""
        res = self.client.post(self.fav_path.format(self.plan_id), data={}, format="json")
        self.assertEqual(201, res.status_code)

    def test_get_list(self):
        """GET /plans/<id>/favs/: いいね一覧取得テスト"""
        plan_id = self.plan_id
        fav = Fav.objects.create(user=self.user, plan_id=plan_id)
        res = self.client.get(self.fav_path.format(plan_id), data={}, format="json")
        self.assertEqual(200, res.status_code)
        actual_favs = Fav.objects.filter(plan_id=plan_id).count()
        # 全てそのplanのfavであることを確認
        self.assertEqual(actual_favs, len(res.data))
        for f in res.data:
            self.assertEqual(plan_id, f['plan_id'])
        fav_list = [f['pk'] for f in res.data]
        self.assertTrue(fav.pk in fav_list)

    def test_destroy(self):
        """DELETE /plans/<id>/favs/: いいね削除テスト"""
        fav = Fav.objects.create(user=self.user, plan_id=self.plan_id)
        res = self.client.delete(self.fav_me_path.format(self.plan_id))
        self.assertEqual(204, res.status_code)
        with self.assertRaises(Fav.DoesNotExist):
            Fav.objects.get(pk=fav.pk)

    def test_destroy_fail(self):
        """DELETE /plans/<id>/favs/: 存在しないいいねの削除テスト"""
        res = self.client.delete(self.fav_me_path.format(self.plan_id))
        self.assertEqual(404, res.status_code)

    def test_get_detail(self):
        """GET /plans/<id>/favs/<id>/: いいねの詳細取得テスト"""
        fav = Fav.objects.create(user=self.user, plan_id=self.plan_id)
        res = self.client.get(self.fav_detail_path.format(self.plan_id, fav.pk), data={}, format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.user.username, res.data['user']['username'])

    def test_get_detail_404(self):
        """GET /plans/<id>/favs/<id>/: いいねの詳細取得404テスト"""
        res = self.client.get(self.fav_detail_path.format(self.plan_id, 9999), data={}, format="json")
        self.assertEqual(404, res.status_code)
        new_plan = self.create_plan()
        fav = Fav.objects.create(user=self.user, plan_id=new_plan.pk)
        res = self.client.get(self.fav_detail_path.format(9999, fav.pk), data={}, format="json")
        self.assertEqual(404, res.status_code)
