"""CurrencyXchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^signup$', csrf_exempt(Signup.as_view()), name='signup'),
	url(r'^signin$', csrf_exempt(SignIn.as_view()), name='signin'),
    url(r'^create-wallet$', csrf_exempt(CreateWallet.as_view()), name='create_wallet'),
    url(r'^read-wallet$', csrf_exempt(ReadWallet.as_view()), name='read_balance'),
    url(r'^update-wallet$', csrf_exempt(UpdateWallet.as_view()), name='update_wallet'),   
    url(r'^convert-currency$', csrf_exempt(ConvertCurrency.as_view()), name='convert_currency'),    
    url(r'^upload$', csrf_exempt(UploadProfileImage.as_view()))
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# http://free.currencyconverterapi.com/api/v5/convert?q=USD_INR&compact=ultra&apiKey=698ea915b459fda1bc68