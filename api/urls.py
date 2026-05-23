from django.urls import path
from .views import DatasetUploadView
from .views import test_api
from .views import get_cycles

urlpatterns = [
    path('upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('test/', test_api, name='test-api'),
    path('cycles/', get_cycles, name='get-cycles'),
]

# superuser neptunetrash 1234
# superuser darshan 1234