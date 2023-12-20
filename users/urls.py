from django.urls import path
from users.views import LoginView, RegisterView, Profile, LogoutView, ProfileUpdate

app_name = 'users'
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile_page'),
    path('profile-edit/', ProfileUpdate.as_view(), name='profile_edit_page'),
    path('register/', RegisterView.as_view(), name='register_page'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page')
]
