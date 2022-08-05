from django.urls import path
from .views import *

app_name='accounts'

urlpatterns = [
    path('register/', register_user, name="register" ),
    path('login/', login_user, name="login" ),
    path('logout/', logout_user, name="logout" ),
    path('profile/', profile_page, name="profile" ),
    path('user_edit/', user_edit, name="user_edit" ),
    path('profile_edit/', profile_edit, name="profile_edit" ),
    path('edit-account/', edit_password, name="edit-account" ),
    path('call_us/', call_us, name="call" ),
    path('reset/<uidb64>/<token>/', Custom_PasswordResetConfirm.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/', Custom_PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', Custom_PasswordResetDone.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', Custom_PasswordResetCompelte.as_view(), name='password_reset_complete'),    

]
