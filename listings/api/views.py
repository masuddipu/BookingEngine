from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, F, FloatField, Value
import datetime

from listings.models import Listing, BookingData
from .serializers import ListingSerializer

class SearchListingData(APIView):
    def get(self, request, format=None):
        max_price = float(request.GET['max_price'])
        check_in = datetime.datetime.strptime(request.GET['check_in'], '%Y-%m-%d').date()
        check_out = datetime.datetime.strptime(request.GET['check_out'], '%Y-%m-%d').date()

        item_list = []
        price_list = []

        listing_list = Listing.objects.all()
        booking_list = BookingData.objects.filter(Q(Q(check_in__lt=check_out) & Q(check_out__gt=check_in)))
        
        print(booking_list)
        booked_room_list = []

        for booking in booking_list:
            if booking.hotel_room:
                booked_room_list.append(booking.hotel_room)

        for listing in listing_list:
            if listing.listing_type == 'apartment':
                if listing.booking_info.price <= max_price:
                    available = True
                    for booking in booking_list:
                        if booking.listing == listing:
                            available = False
                            break
                    if available:
                        qs = Listing.objects.filter(listing_type='apartment').annotate(price=F('booking_info__price'))
                        item_list.append(qs.get(id=listing.id))
            else:
                room_type = listing.hotel_room_types.all().annotate(price=F('booking_info__price')).order_by('price')
                for type in room_type:
                    if type.price <= max_price:
                        available = False
                        for room in type.hotel_rooms.all():
                            if room not in booked_room_list:
                                available = True
                        if available:
                            # DO STAFF
                            qs = Listing.objects.filter(id=listing.id).annotate(price=Value(type.price, output_field=FloatField()))
                            item_list.append(qs.get(id=listing.id))
                            break

        
        serializer = ListingSerializer(item_list, many=True)

        return Response({'items' : serializer.data})