from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from cp.models import EMail
from price.models import Price, PriceFeature, PriceFeaturePrice, UserPrice


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'cp/index.html', {})


def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, 'cp/contacts.html', {})


def prices(request: HttpRequest) -> HttpResponse:
    prices = Price.objects.all()
    features = PriceFeature.objects.all()
    features_prices = PriceFeaturePrice.objects.all()

    for feature in features:
        feature.prices = list()
        for price in prices:
            val = False
            for fp in features_prices:
                if fp.price_feature_id == feature.id and fp.price_id == price.id:
                    val = True
            feature.prices.append(val)

    return render(request, 'cp/prices.html', {'prices': prices, 'features': features})


def emaillog(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        emaillist = EMail.objects.filter(mail_from=request.user.email).order_by('-sent').all()
        return render(request, 'cp/emaillog.html', {'emaillist': emaillist, })
    else:
        return HttpResponseRedirect('/')
