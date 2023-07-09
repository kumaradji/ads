from django.urls import path
from .views import (
    AdvertListView,
    AdvertCreateView,
    AdvertDetailView,
    ResponseCreateView,
    ResponseDetailView,
    PrivatePageView,
    AcceptResponseView,
    DeleteResponseView,
    LikeView,
    DislikeView,
    AdvertDeleteView,
    AdvertUpdateView,
)

app_name = 'ads'

urlpatterns = [
    path('', AdvertListView.as_view(), name='advert-list'),
    path('advert/create/', AdvertCreateView.as_view(), name='advert-create'),
    path('advert/<int:pk>/', AdvertDetailView.as_view(), name='advert-detail'),
    path('advert/<int:pk>/response/create/', ResponseCreateView.as_view(), name='response-create'),
    path('response/<int:pk>/', ResponseDetailView.as_view(), name='response-detail'),
    path('private/', PrivatePageView.as_view(), name='private'),
    path('response/accept/<int:response_id>/', AcceptResponseView.as_view(), name='accept-response'),
    path('response/delete/<int:response_id>/', DeleteResponseView.as_view(), name='delete-response'),
    path('response/<int:pk>/like/', LikeView.as_view(), name='like'),
    path('response/<int:pk>/dislike/', DislikeView.as_view(), name='dislike'),
    path('advert/<int:pk>/delete/', AdvertDeleteView.as_view(), name='delete-advert'),
    path('advert/<int:pk>/update/', AdvertUpdateView.as_view(), name='update-advert'),
]
