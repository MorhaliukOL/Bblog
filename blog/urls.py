from django.urls import path
from .views import MyBlog, PostCreate, PostDetail, PostUpdate,\
    PostDelete, other_blogs, NewsFeed, mark_posts_read

urlpatterns = [
    path('my/', MyBlog.as_view(), name='my-blog'),
    path('post/create', PostCreate.as_view(), name='post-create'),
    path('post/detail/<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('post/update/<int:pk>', PostUpdate.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post-delete'),
    path('other/', other_blogs, name='blogs-other'),
    path('news/', NewsFeed.as_view(), name='news-feed'),
    path('mark_read/<int:pk>', mark_posts_read, name='mark-read'),
]
