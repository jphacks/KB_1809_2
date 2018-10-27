from django.core.management.base import BaseCommand

from accounts.models import User
from plan.models import Spot, Report
from django.conf import settings

import pathlib


class Command(BaseCommand):
    def handle(self, *args, **options):
        used_imgs = list()
        users = User.objects.all()
        for u in users:
            used_imgs.append(u.icon.path)
        spots = Spot.objects.all()
        for s in spots:
            used_imgs.append(s.image.path)
        reports = Report.objects.all()
        for r in reports:
            used_imgs.append(r.image.path)

        p = pathlib.Path(settings.MEDIA_ROOT)
        for f in p.glob("**/*"):
            if f.is_dir():
                continue

            if f.name == "user.png":
                continue

            if f.as_posix() not in used_imgs:
                print("remove", f.as_posix())
                f.unlink()
