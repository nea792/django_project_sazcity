from django.urls import path
from .views import register_user, login_user, logout_user, profile_user, edit_account

app_name='accounts'

urlpatterns = [
    path('register/', register_user, name="register" ),
    path('login/', login_user, name="login" ),
    path('logout/', logout_user, name="logout" ),
    path('profile/', profile_user, name="profile" ),
    path('edit-account/', edit_account, name="edit-account" ),
]
