from django.urls import path
from .views import SignUp, LoginView, ProfileView, LogoutView, ResponseListView, ResponseDeleteView, ConfirmationView, \
    become_author

app_name = 'users'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('become-author/', become_author, name='become-author'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('profile/responses/', ResponseListView.as_view(), name='response_list'),
    path('profile/response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='delete_response'),
]
