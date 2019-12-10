from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
	# path('', views.SignUp.as_view(), name='signup'),
	path('', views.signup, name='signup'),
	path('activate/<uidb64>/<token>', views.activate, name='activate'),
	# path('logout', views.logout_view, name='logout'),
	# path('login', views.UserLoginView.as_view(), name='login'),
	# path('profile/update/<pk>', views.ProfileUpdateView.as_view(), name='profile_update'),
	# path('password_reset', views.UserPasswordResetView.as_view(), name='reset_pass'),
	# path('password_reset_confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='reset'),
	# path('password/reset/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('password_reset', views.UserAddressConfirmView.as_view(), name='reset_pass'),
]