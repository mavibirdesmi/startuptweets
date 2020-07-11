from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'tweet-home'),
    path('download/', views.returnCSV, name = 'tweetData-download'),
    path('display/', views.printTweets, name = 'printTweets'),
]