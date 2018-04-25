from django.conf.urls import url
from .views import EbayAPI, EbayWebHook

urlpatterns = [
    url(r'^api/$', EbayAPI.as_view(), name='api'),
    url(r'^notification/$', EbayWebHook.as_view(), name='webhook'),
]
