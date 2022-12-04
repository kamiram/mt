import json
from datetime import datetime
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from cp.models import EMail, Constants
from price.models import Price, UserPrice, PriceFeature


@csrf_exempt
def link(request: HttpRequest) -> HttpResponse:
    data = json.loads(request.body.decode())

    uid = uuid4().hex
    host_utl = settings.HOST_URL
    email = EMail()
    email.uid = uid
    email.sent = datetime.now()
    email.readcount = -1
    email.mail_from = data['mail_from']
    email.mail_to = data['mail_to']
    email.topic = data['topic']
    email.save()

    show_mailtracking = True
    mt_const = Constants.objects.filter(name='show_mailtracking').first()

    if mt_const and mt_const.value == 0:
        show_mailtracking = False

    user = get_user_model().objects.filter(email=data['mail_from']).first()
    if user:
        userprice = UserPrice.objects.filter(user=user).last()
        pricefeatures = [feature.code for feature in PriceFeature.objects.filter(pricefeatureprice__price=userprice.price).all()]
        print('pricefeatures ', pricefeatures)
        show_mailtracking = 'nosignature' not in pricefeatures
        show_banner = 'noads' not in pricefeatures
        data = {
            'url': f'{host_utl}{uid}' if show_mailtracking else '',
            'banner': show_banner
        }
    else:
        data = '{}'

    resp = HttpResponse(
        content=json.dumps(data),
        content_type='application/json',
    )

    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = '*'

    return resp


def touch(request: HttpRequest, uid: str) -> HttpResponse:
    email = EMail.objects.filter(uid=uid).first()
    print('Referer: ', request.headers.get('Referer'))
    if email:
        if email.readcount >= 0:
            email.readcount = email.readcount + 1
            email.read = datetime.now()
        else:
            email.readcount = 0
        email.save()
    return HttpResponse()
