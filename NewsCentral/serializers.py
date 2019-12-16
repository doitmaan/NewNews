# NewsCentral/serializers.py
from rest_framework import serializers
from .models import STOCK, LINK


class LinkTableSearlizer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'auto_increment_id',

            'stcok',
            'linkUrl',
            'publish_date',
            'added_date',
            'imageLinkUrl',
            'title',
        )
        model = LINK


class NewsCentralSerializer(serializers.ModelSerializer):
    LinksUrls = LinkTableSearlizer(many=True)

    class Meta:
        model = STOCK
        fields = (
            'stockId',
            'LastSearched',
            'LinksUrls',

        )





