from django.urls import path, include
from . import views

app_name = 'news'

urlpatterns = [
	path('', views.PostListView.as_view(), name='post_list'),
	path('post_detail/<pk>/', views.PostDetailView.as_view(), name='post_detail'),
	path('post_detail/create_comment', views.PostCreateView.as_view(), name='post_create'),
	path('post_detail/<pk>/create_comment', views.CommentCreateView.as_view(), name='comment_create'),
]