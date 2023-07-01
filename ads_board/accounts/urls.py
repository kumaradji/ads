from django.urls import path
from .views import SignUp, LoginView, ProfileView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
