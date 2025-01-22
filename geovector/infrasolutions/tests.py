from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from .views import GroupViewSet, FeatureViewSet
from .serializers import GroupSerializer
from .models import Feature

# class GroupViewSetTest(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = User.objects.create_superuser(
#             username='admin',
#             email='admin@example.com',
#             password='password'
#         )
#         self.view = GroupViewSet.as_view({'get': 'list', 'post': 'create'})

#     def test_create_group(self):
#         # Create POST request
#         request = self.factory.post('/groups/', {'name': 'test_group'}, format='json')
#         force_authenticate(request, user=self.user)
#         response = self.view(request)

#         # Assert response
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Group.objects.count(), 1)
#         self.assertEqual(Group.objects.get().name, 'test_group')

#     def test_list_groups(self):
#         # Create test group
#         Group.objects.create(name='test_group')

#         # Create GET request
#         request = self.factory.get('/groups/')
#         force_authenticate(request, user=self.user)
#         response = self.view(request)

#         # Assert response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'], 1)


class FeatureTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.view = FeatureViewSet.as_view(
            {'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})
        self.test_geojson = {
            "type": "MultiPolygon",
            "coordinates": [[[[5.604309854600078, 52.683236913801949], [5.594550666422244, 52.68329995521097], [5.594311853211731, 52.676274497315148], [5.593319621139938, 52.676280556584395], [5.593114784182781, 52.669885405021276], [5.592727550483377, 52.663074713043351], [5.591471992819405, 52.660987277449507], [5.594804805689739, 52.659670638392242], [5.597550524841117, 52.656782488911588], [5.595640250652885, 52.660294825330183], [5.593210105763918, 52.660623133928929], [5.599233366392583, 52.660877433596276], [5.598337053813905, 52.66039446983217], [5.598399987996006, 52.659397999644959], [5.596626544473298, 52.659230421251088], [5.597353153498487, 52.658800404020567], [5.600177873099456, 52.658900900184115], [5.60012560884521, 52.660153048983275], [5.602063325883876, 52.660224168517722], [5.601515263317332, 52.656905870310489], [5.615913947495247, 52.650628952786278], [5.629891128034845, 52.637716695316037], [5.630442558626115, 52.638402743799134], [5.641100733501887, 52.64254774580678], [5.636278600585254, 52.647219662785581], [5.636130855283098, 52.64961182074132], [5.648865386437212, 52.649550911174259], [5.650015246501316, 52.654310822944424], [5.642831213000576, 52.660551130021872], [5.655379217018095, 52.665950428297755], [5.641588569059689, 52.678014821108221], [5.643716847267161, 52.682614451497074], [5.625802898482401, 52.682606810953942], [5.6126233416939, 52.681345986221935], [5.609528699884569, 52.680420144583586], [5.606929231156348, 52.682416489341136], [5.604310240198247, 52.682310114810207], [5.604309854600078, 52.683236913801949]]]]
        }

    def test_create_feature(self):
        request = self.factory.post('/features/', {
            'name': 'test_feature',
            'geometry': self.test_geojson
        }, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feature.objects.count(), 1)
        self.assertEqual(Feature.objects.get().name, 'test_feature')

    def test_list_features(self):
        Feature.objects.create(
            name='test_feature',
            geometry=GEOSGeometry(str(self.test_geojson))
        )

        request = self.factory.get('/features/')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_feature(self):
        # Create initial feature
        feature = Feature.objects.create(
            name='test_feature',
            geometry=GEOSGeometry(str(self.test_geojson))
        )

        # Prepare update data
        update_data = {
            'name': 'updated_feature',
            'geometry': self.test_geojson
        }

        # Create PUT request
        request = self.factory.put(
            f'/features/{feature.id}/',
            update_data,
            format='json'
        )
        force_authenticate(request, user=self.user)

        # Get detail view for update
        response = self.view(request, pk=feature.id)

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Feature.objects.get(
            id=feature.id).name, 'updated_feature')

    def test_delete_feature(self):
        # Create initial feature
        feature = Feature.objects.create(
            name='test_feature',
            geometry=GEOSGeometry(str(self.test_geojson))
        )

        # Create DELETE request
        request = self.factory.delete(f'/features/{feature.id}/')
        force_authenticate(request, user=self.user)

        # Get detail view for delete
        response = self.view(request, pk=feature.id)

        # Assert response and database state
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Feature.objects.count(), 0)


# class LiveFeatureAPITest(APITestCase):        
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
#         self.view = FeatureViewSet.as_view(
#             {'get': 'list'})
#         self.test_bbox = '6.309176,52.742611,6.990783,53.310857'

        
#     def test_get_features_in_bbox(self):
#         # Make GET request with bbox parameter        
#         url = f'/features/?in_bbox={self.test_bbox}'
#         request = self.factory.get(url)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'], 24)