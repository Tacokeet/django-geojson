from django.contrib.auth.models import Group, User
from .models import Feature
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FeatureSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Feature
        geo_field = 'geometry'
        auto_bbox = True
        fields = ['id', 'name', 'geometry']
