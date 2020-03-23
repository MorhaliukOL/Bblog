from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from .models import Post

POSTS_PER_PAGE = 5


class MyBlog(LoginRequiredMixin, ListView):
    """
    Display list of posts created by the current user,
    ordered by creation date in reversed order.
    """
    context_object_name = 'my_posts'
    template_name = 'blog/my_blog.html'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'body']

    def get_queryset(self):
        post = Post.objects.filter(pk=self.kwargs['pk'])
        if post and post[0].author == self.request.user:
            return post
        else:
            raise Http404()


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('my-blog')
    template_name = 'blog/post_delete.html'

    def get_queryset(self):
        post = Post.objects.filter(pk=self.kwargs['pk'])
        if post and post[0].author == self.request.user:
            return post
        else:
            raise Http404()
