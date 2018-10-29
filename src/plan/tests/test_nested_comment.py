from plan.models import Comment
from .base import V1TestCase


class CommentTestCase(V1TestCase):

    def test_post(self):
        """POST /plan/plans/<id>/comments/: コメント作成テスト"""
        res = self.client.post(self.comment_path.format(self.plan_id), data=self.comment_data[0], format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual(self.comment_data[0]['text'], res.data['text'])
        self.assertEqual(self.plan_id, res.data['plan_id'])
        self.assertEqual(self.user.username, res.data['user']['username'])

    def test_get_list(self):
        """GET /plan/plans/<id>/comments/: コメント一覧取得テスト"""
        comment = Comment.objects.create(user=self.user, plan_id=self.plan_id, **self.comment_data[0])
        res = self.client.get(self.comment_path.format(self.plan_id), data={}, format="json")
        self.assertEqual(200, res.status_code)
        actual_comments = Comment.objects.filter(plan_id=self.plan_id).count()
        # 全てそのplanのfavであることを確認
        self.assertEqual(actual_comments, len(res.data))
        for f in res.data:
            self.assertEqual(self.plan_id, f['plan_id'])
        comments_list = [f['pk'] for f in res.data]
        self.assertTrue(comment.pk in comments_list)

    def test_destroy(self):
        """DELETE /plan/plans/<id>/comments/<id>/: コメント削除テスト"""
        comment = Comment.objects.create(user=self.user, plan_id=self.plan_id, **self.comment_data[0])
        res = self.client.delete(self.comment_detail_path.format(self.plan_id, comment.pk))
        self.assertEqual(204, res.status_code)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment.pk)

    def test_destroy_fail(self):
        """DELETE /plan/plans/<id>/comments/<id>/: 存在しないコメントの削除テスト"""
        res = self.client.delete(self.comment_detail_path.format(self.plan_id, 9999))
        self.assertEqual(404, res.status_code)

    def test_get_detail(self):
        """GET /plan/plans/<id>/comments/<id>/: コメントの詳細取得テスト"""
        comment = Comment.objects.create(user=self.user, plan_id=self.plan_id, **self.comment_data[0])
        res = self.client.get(self.comment_detail_path.format(self.plan_id, comment.pk), format="json")
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.comment_data[0]['text'], res.data['text'])
        self.assertEqual(self.user.username, res.data['user']['username'])

    def test_get_detail_404(self):
        """GET /plan/plans/<id>/comments/<id>/: コメントの詳細取得404テスト"""
        res = self.client.get(self.comment_detail_path.format(self.plan_id, 9999), data={}, format="json")
        self.assertEqual(404, res.status_code)
        new_plan_res = self.client.post(self.plan_path, data=self.plan_data, format='json')
        fav = Comment.objects.create(user=self.user, plan_id=new_plan_res.data['pk'])
        res = self.client.get(self.comment_detail_path.format(9999, fav.pk), data={}, format="json")
        self.assertEqual(404, res.status_code)
