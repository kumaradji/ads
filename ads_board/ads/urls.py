from django.urls import path
from .views import AdvertCreateView, AdvertDetailView, ResponseCreateView, ResponseDetailView, AdvertListView

app_name = 'ads'

urlpatterns = [
    path('', AdvertListView.as_view(), name='advert-list'),

    path('advert/create/', AdvertCreateView.as_view(), name='advert-create'),
    path('advert/<int:pk>/', AdvertDetailView.as_view(), name='advert-detail'),
    path('advert/<int:pk>/response/create/', ResponseCreateView.as_view(), name='response-create'),
    path('response/<int:pk>/', ResponseDetailView.as_view(), name='response-detail'),
]
