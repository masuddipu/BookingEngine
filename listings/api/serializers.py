from rest_framework import serializers
from listings.models import Listing

class ListingSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    class Meta:
        model = Listing
        fields = ('listing_type', 'title', 'country', 'city', 'price')