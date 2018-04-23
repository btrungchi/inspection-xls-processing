from django.urls import path

from mainapp.views import InspectionView

urlpatterns = [
    path('', InspectionView.as_view(), name='index'),
    path('drop-all', InspectionView.drop_all),
]