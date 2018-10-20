from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator


class UserManager(BaseUserManager):
    """
    カスタムユーザモデルのためのマネージャ
    """

    def create_user(self, username, password, **extra_fields):
        """
        ユーザ作成の関数
        :param username: 英数字と-_を用いるユーザ名 *必須*
        :param password: パスワード
        :param extra_fields: その他のパラメータ
        :return: 作成されたユーザのManagerインスタンス
        """
        if not username:
            return ValueError('User name is required')
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password, **kwargs):
        """
        /adminにログインできるスーパーユーザ作成用の関数
        :param username: 学生ID *必須*
        :param password: パスワード
        :return: 作成されたStudentのインスタンス
        """
        return self.create_user(username=username, password=password, is_staff=True,
                                is_superuser=True, is_active=True, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """
    学生のモデル
    """
    # ユーザ名をバリデーション
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(max_length=64, unique=True, verbose_name='ユーザ名',
                                help_text='小文字の英数字および数字のみ使用できます',
                                validators=[username_validator])
    email = models.EmailField(max_length=255, unique=True, default='')
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        """ユーザ名を返却"""
        return self.username

    class Meta:
        ordering = ['username']
        verbose_name = 'ユーザ'
        verbose_name_plural = 'ユーザ'
