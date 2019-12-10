from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
									DetailView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Celery
from tasks import new_comment_email

from .models import Post, Comment

from .forms import CommentCreateForm, PostCreateForm

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

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


# Function views

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('news:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'news/comment_create.html', {'form': form})