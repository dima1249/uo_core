from rest_framework import serializers, fields

from sales.models import VideoModel

TRIP_TYPES = [
    ("OW", 'OW'),
    ("RT", 'RT'),
]
CABIN_CODE_TYPES = [
    ('Y', "PremiumEconomy"),
    ('S', "Economy"),
    ('C', "Business"),
    ('J', "PremiumBusiness"),
    ('F', "First"),
    ('P', "PremiumFirst"),
]


class GetPointSerializer(serializers.Serializer):
    video_id = serializers.IntegerField(required=True)


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = '__all__'
        read_only_fields = ['dial_code', 'phone', 'email']
