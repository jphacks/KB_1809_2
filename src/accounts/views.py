from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import viewsets, mixins, permissions
from .forms import LoginForm
from . import serializers, models


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/top.html'


class UserViewSets(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    """
    retrieve:
        指定したユーザのプロフィールを取得するエンドポイント

    create:
        ユーザを作成するエンドポイント．未認証のユーザでも叩ける．

    update:
        ユーザのプロフィールを更新するエンドポイント．
    """
    queryset = models.User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        return super(UserViewSets, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateUserSerializer
        return serializers.UserSerializer
