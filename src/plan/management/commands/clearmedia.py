from django.core.management.base import BaseCommand

from accounts.models import User
from plan.models import Spot, Report
from django.conf import settings

import pathlib


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete all no use image files in medir directory.'
        )

    def handle(self, *args, **options):
        used_imgs = list()
        used_imgs.extend([u.icon.path for u in User.objects.all()])
        used_imgs.extend([s.image.path for s in Spot.objects.all()])
        used_imgs.extend([r.image.path for r in Report.objects.all()])

        p = pathlib.Path(settings.MEDIA_ROOT)
        for f in p.glob("**/*"):
            if f.is_dir() or f.name == "user.png":
                continue

            if f.as_posix() not in used_imgs:
                if options['delete']:
                    print("remove", f.as_posix())
                    f.unlink()
                else:
                    print(f.as_posix())
