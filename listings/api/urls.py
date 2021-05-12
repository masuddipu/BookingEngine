from django.urls import path

from .views import SearchListingData

urlpatterns = [
    path('v1/units/', SearchListingData.as_view(), name='listing_search'),
]
