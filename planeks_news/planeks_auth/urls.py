from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
	path('', views.signup, name='signup'),
	path('activate/<uidb64>/<token>', views.activate, name='activate'),
	path('logout', views.logout_view, name='logout'),
	path('login', views.UserLoginView.as_view(), name='login'),
]