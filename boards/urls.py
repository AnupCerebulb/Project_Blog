from django.urls import path
from boards import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('company/', views.about_company, name='about_company'),
    path('author/', views.about_author, name='about_author'),
    path('author/vitor/', views.about_vitor, name='about_vitor'),
    path('author/erica/', views.about_erica, name='about_erica'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('board_topics/<int:pk>/', views.board_topics, name='board_topics'),
    path('board_topics/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('board_topics/<int:pk>/new/',views.new_topic,name='new_topic'),
    path('board_topics/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('home', views.home, name='home'),
    path('profile/', views.myaccounts, name='profile'),

]