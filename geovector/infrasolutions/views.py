from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import Feature
from rest_framework import permissions, viewsets
from rest_framework_gis.filters import InBBoxFilter
from rest_framework_gis.pagination import GeoJsonPagination

from geovector.infrasolutions.serializers import GroupSerializer, UserSerializer, FeatureSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeatureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows features to be viewed or edited.
    """
    queryset = Feature.objects.all().order_by('id')
    serializer_class = FeatureSerializer
    bbox_filter_field = 'geometry'
    filter_backends = (InBBoxFilter,)
    pagination_class = GeoJsonPagination
    bbox_filter_include_overlapping = True  # Optional
    permission_classes = [permissions.IsAuthenticated]
