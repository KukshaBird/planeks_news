from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
									DetailView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.utils import timezone
# Celery
from tasks import new_comment_email
# Models
from .models import Post, Comment
# Forms
from .forms import CommentCreateForm, PostCreateForm

class PostListView(ListView):

    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-published_date')

class DraftListView(PermissionRequiredMixin, ListView):

    permission_required = 'news.can_moderate'
    model = Post
    template_name = 'news/drafts.html'

    def get_queryset(self):
        return Post.objects.filter(is_published=False, is_declined=False).order_by('-created_date')

class PostDetailView(DetailView):

    model = Post
    template_name = 'news/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'news/post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('news:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_published = False
        form.instance.is_declined = False
        if self.request.user.has_perm('news.can_publish'):
            form.instance.publish()
        form.instance.save()
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'news/comment_create.html'
    form_class = CommentCreateForm
    success_url = reverse_lazy('news:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.save()
        new_comment_email(post)
        return super().form_valid(form)

# function views:
@permission_required('news.can_moderate')
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('news/drafts')

@permission_required('news.can_moderate')
def post_decline(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.decline()
    return redirect('drafts')
