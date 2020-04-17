from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
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
        return Post.objects.filter(author=
                                   self.request.user).order_by('-date')


class NewsFeed(LoginRequiredMixin, ListView):
    """
    Display list of posts created by users that current user
    is subscribed on, ordered by creation date in reversed order.
    """
    context_object_name = 'new_posts'
    template_name = 'blog/news_feed.html'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        blog = Blog.objects.get(owner=self.request.user)
        return Post.objects.filter(author__in=
                                   blog.subscribed_to.all()).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blog = Blog.objects.get(owner=self.request.user)
        already_read = blog.read_posts.all()
        context['already_read'] = already_read
        return context


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


def alter_user_status(request):
    """
    Subscribe 'blog' to user that gets past in the POST request
    if POST request's 'subscribe' parameter is True,
    and unsubscribe otherwise
    """
    if request.method == 'POST':
        blog = Blog.objects.get(owner=request.user)
        user_pk = request.POST.get('user_pk')
        if request.POST.get('subscribe') == 'True':
            blog.subscribed_to.add(User.objects.get(pk=user_pk))
            blog.save()
        else:
            blog.subscribed_to.remove(User.objects.get(pk=user_pk))
            blog.save()
        return redirect('other-blogs')


class OtherBlogs(LoginRequiredMixin, ListView):
    context_object_name = 'users'
    template_name = 'blog/other_blogs.html'

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_blog = Blog.objects.get(owner=self.request.user)
        context['subscribed_to'] = current_blog.subscribed_to.all()
        return context


def other_blogs(request):
    """
    Display list of other users
    """
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


def mark_posts_read(request, pk):
    blog = Blog.objects.get(owner=request.user)
    blog.read_posts.add(Post.objects.get(pk=pk))
    return redirect('news-feed')
