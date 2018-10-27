import os
import base64

from django.conf import settings


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

comment_data = [
    {
        'text': 'This is a first comment message.'
    },
    {
        'text': 'This is a second comment message'
    }
]

user_data = [
    {
        "username": "test_user",
        "password": "hogefugapiyo"
    },
    {
        "username": "second_user",
        "password": "hogefugapiyo"
    }
]

report_data = [
    {
        "text": "This is a test report.",
        "image": b64image
    },
    {
        "text": "This is a test report 2.",
        "image": b64image
    }
]


