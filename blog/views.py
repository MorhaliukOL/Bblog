from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Post, Blog

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
        post = Post.objects.filter(pk=self.kwargs['pk'],
                                   author=self.request.user)
        if post:
            return post
        else:
            raise Http404()


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('my-blog')
    template_name = 'blog/post_delete.html'

    def get_queryset(self):
        post = Post.objects.filter(pk=self.kwargs['pk'],
                                   author=self.request.user)
        if post:
            return post
        else:
            raise Http404()


def alter_user_status(request, blog):
    user_pk = request.POST.get('user_pk')
    if request.POST.get('subscribe') == 'True':
        blog.subscribed_to.add(User.objects.get(pk=user_pk))
    else:
        blog.subscribed_to.remove(User.objects.get(pk=user_pk))


def other_blogs(request):
    blog = Blog.objects.get(owner=request.user)
    if request.method == 'POST':
        alter_user_status(request, blog)

    users = User.objects.all()
    subscribed_to = blog.subscribed_to.all()
    context = {
        'users': users,
        'subscribed_to': subscribed_to,
    }
    return render(request, 'blog/other_blogs.html', context)
