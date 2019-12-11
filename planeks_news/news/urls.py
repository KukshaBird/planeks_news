from django.urls import path, include
from . import views

app_name = 'news'

urlpatterns = [
	path('', views.PostListView.as_view(), name='post_list'),
	path('drafts/', views.DraftListView.as_view(), name='drafts'),
	path('post_detail/<pk>/', views.PostDetailView.as_view(), name='post_detail'),
	path('post_detail/create_comment', views.PostCreateView.as_view(), name='post_create'),
	path('post_approve/<pk>', views.post_publish, name='post_approve'),
	path('post_decline/<pk>', views.post_decline, name='post_decline'),
	path('post_detail/<pk>/create_comment', views.CommentCreateView.as_view(), name='comment_create'),
]