from mainApp.models import Image, Profile, Ticker, TickerWatcher
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class TickerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticker
        fields = [
            "id",
            "symbol",
            "name",
            "price",
            "created_at",
            "updated_at",
        ]


class TickerWatcherSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    ticker = TickerSerializer(many=False, read_only=True)

    class Meta:
        model = TickerWatcher
        fields = [
            "id",
            "user",
            "ticker",
            "min_price",
            "max_price",
            "created_at",
            "updated_at",
        ]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "as_url", "as_file"]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    avatar_url = ImageSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "display_name",
            "avatar_url",
            "phone",
            "created_at",
            "updated_at",
        ]
