from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import viewsets, mixins, permissions
from .forms import LoginForm
from . import serializers, models, permissions as custom_permissions


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
    permission_classes = (permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        return super(UserViewSets, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateUserSerializer
        return serializers.UserSerializer


class MeViewSets(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    """
    自分自身の情報を取得するエンドポイント

    retrieve:
        自分自身のプロフィールを取得するエンドポイント

    update:
        自分自身のプロフィールを更新するエンドポイント
    """
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly)

    def get_object(self):
        """ログインしているユーザを返す"""
        return self.request.user
