from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Widok posta.
    #path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<int:minute>/<int:second>/<slug:post>/',
        views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',
        views.post_share, name='post_share'),
    path('podsumowanie',
        views.post_suma, name='post_suma'),
    path('new_post/',
         views.new_post, name='new_post'),
    path('<int:post_id>/edit_post/',
         views.edit_post, name='edit_post')
]