from django.shortcuts import render


def my_blog(request):
    return render(request, 'blog/my_blog.html')
